import re
import paramiko
import pandas as pd
import re
import json
from datetime import datetime,time
import sqlite3
from sqlite3 import Error
import requests
import config
import errormessages
from naboxemailnotification import notify,is_time_between
now = datetime.now()
requests.packages.urllib3.disable_warnings()
firsttime = None

##########################################################################################
##############################  All Interaction with NABox  ##############################
##########################################################################################

def naboxconnect():
   ########## NABox connection Parameter definition#########
   host = config.host
   port = config.port
   username = config.username
   password = config.password
   command = config.command
   ########## Session creation and Data collection #########
   try:
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(host, port, username, password)
      stdin, stdout, stderr = ssh.exec_command(command)
      msg = stdout.readlines()
      ssh.close()
   except:
      msg = "Unable to connect to nabox"
   return msg

##########################################################################################
##############################  Data Cleaning Section  ###################################
##########################################################################################

def listheaderremover(str_list):
   ########## Remove the line that contains the header of the ourput#########
   str_list = [x for x in str_list if '#' not in x]
   str_list = [x for x in str_list if 'STATUS' not in x]
   str_list = [x for x in str_list if 'POLLER' not in x]
   str_list = [x for x in str_list if 'GROUP' not in x]
   return str_list

def listcleaner():
   ########## Clean up contents of list to make ready for a dataframe #########
   lines = naboxconnect()
   cleanlist = []
   if lines == "Unable to connect to nabox":
      msg = errormessages.msg2
      notify(msg)
   else:
      for line in lines:
         line = line.replace("[NOT RUNNING]","[NOTRUNNING]")
         line = line.split('  ')
         str_list = list(filter(None, line))
         str_list = list(filter(bool, str_list))
         str_list = list(filter(len, str_list))
         str_list = list(filter(lambda item: item, str_list))
         str_list = listheaderremover(str_list)
         str_list = [x.strip(' ') for x in str_list]
         str_list.remove('\n')
         cleanlist.append(str_list)
      return cleanlist

##########################################################################################
########################  All Interaction with ticketsystem ####################################
##########################################################################################

def ticketsystem(description,note,affectedsystems,requesttype,tprefnum):
   url = config.ticketsystemurl
   headers = config.token
   notes = note + "\n\nSystems' datacollection affected are:\n" +affectedsystems
   payload = {
               "description": description,
               "note": notes,
               "requesttype": requesttype,
               "priority" : 2,
               "thirdparty": tprefnum
             }
   response = requests.post(url,headers=headers,json=payload,verify=False)
   if json.loads(response.text.replace('\n',''))['success'] == True :
      ticketcreation = 'success'
   else:
      ticketcreation = 'failure'
   return ticketcreation

def ticketsystemtimecheck(ft):
   global firsttime
   if firsttime == None:
      firsttime = datetime.now()
      replymessage = 'True'
   elif ((datetime.now() - firsttime).total_seconds()/60) > 1440:
      firsttime = None
      replymessage = 'True'
   elif ((datetime.now() - firsttime).total_seconds()/60) < 1440:
      replymessage = 'False'
   return replymessage

##########################################################################################
################  Error Notification via email and ticket creation  ######################
##########################################################################################

def errorstatuschecker(df):
   affectednetapp = list(df.loc[df['Status'] != '[RUNNING]', 'Netapp Name'].to_numpy())
   if len(affectednetapp) == 0:
      msg = errormessages.msg6
      notify(msg) if is_time_between(time(5, 00),time(5, 5)) else None
   else:
      affectedsystems = '\n'.join(map(str, affectednetapp))
      msg = errormessages.msg1
      subject = errormessages.sub1
      ticketsystemticket = ticketsystem(subject,msg,affectedsystems,"EVT","BFSTORAGE-ALERT-14-1-2-15-24") if ticketsystemtimecheck(firsttime) == 'True' else None
      notify(msg,affectedsystems) if is_time_between(time(8, 00),time(8, 5)) else notify(msg,affectedsystems) if is_time_between(time(13, 30),time(13, 35)) else None #Note that time is in UTC format
      notify(errormessages.msg7,affectedsystems,errormessages.sub7) if ticketsystemticket != 'success' else None
      
##########################################################################################
############################## All Interaction with Database #############################
##########################################################################################

def execution(db_file):
   ############## Take the clean list of the command contents. Dump it into a dataframe and send that into SQLite3 DB############################
   cleanlist = listcleaner()
   cleanlist = list(filter(None, cleanlist))
   columnnames = ['Status', 'Netapp Name', 'Location']
   df = pd.DataFrame(cleanlist, columns=columnnames)
   df['DateTime'] = now
   conn = sqlite3.connect(db_file)
   c = conn.cursor()
   df['DateTime'] = df['DateTime'].astype('str')
   c.executemany('insert into NABoxMon (Status,NetappName,Location, Datettime) values (?,?,?,?);',df.to_records(index=False))
   conn.commit()
   errorstatuschecker(df)

def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except:
       msg = errormessages.msg3
       notify(msg)
   return conn

def create_table(conn, create_table_sql):
   try:
       c = conn.cursor()
       c.execute(create_table_sql)
   except:
       msg = errormessages.msg4
       notify(msg)

def del_tablerows(db_file):
   sql_delete_oldrows_naboxmon = "DELETE from NABoxMon WHERE Datettime < date('now','-30 day');"
   conn = create_connection(db_file)
   try:
      c = conn.cursor()
      c.execute(sql_delete_oldrows_naboxmon)
      conn.commit()
   except:
       msg = errormessages.msg8
       notify(msg)

def DBCreate(db_file):
   #database = r"C:\sqlite\db\NABoxMon.db"
   sql_create_naboxmon_table = """ CREATE TABLE IF NOT EXISTS NABoxMon (
                                       id integer PRIMARY KEY,
                                       Status text NOT NULL,
                                       NetappName text,
                                       Location text,
                                       Datettime text
                                   ); """
   
   # create a database connection
   conn = create_connection(db_file)

   # create tables
   if conn is not None:
       # create naboxmon table
       create_table(conn, sql_create_naboxmon_table)
   else:
       msg = "Error! cannot create the database connection."
       notify(msg)


######### This is verification function. To be used only for script troubleshooting #############
def dbread(db_file):
   conn = None;
   try:
      conn = sqlite3.connect(db_file)
      print(pd.read_sql('select * from NABoxMon;',conn))
   except Error as e:
      print(e)
   finally:
      if conn:
         conn.close()

##########################################################################################
#################################### Main function  ######################################
##########################################################################################

if __name__ == '__main__':
   ########## Database location is defined here ####################
   database = r"C:\sqlite\db\NABoxMon.db"
   DBCreate(database)
   execution(database)
   del_tablerows(database)
   dbread(database)