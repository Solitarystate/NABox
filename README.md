# NABox
A simple monitoring script for NABox using python paramiko and sqlite db


#NABox Monitoring Script


##Context

NABox is an opensource based solution for monitoring netapp performance 
and capacity metrics(https://nabox.org). This python script is intended to 
send email notifications everyday about status of the harvest data 
collection service. The service that determines if NABox is useful or not.


##Script Overview

1. Fetch netapp-manager service status from NABox Harvest using SSH
1. Perform data manipulation and convert them to pandas dataframe
1. Discharge the contents of the dataframe into a sqlite3 db for retention
1. In parallel send notification to admin mailboxes about the status
1. Create a marvel ticket incase a harvest service is not running
1. Updates the marvel ticket with a new failure entry once every 60 mins
1. Notifies the admins if the ticket could not be created
1. Notifies via email twice a day if something is wrong and once if all ok
1. Email will contain link to KB and also the list of systems affected
1. The database content retention is set to 30 days


###Note about Script(In times of troubleshooting)

1. Use the dbread function only for troubleshooting purposes
1. Every steps failure is expected to be reported through email to the 
   admins
