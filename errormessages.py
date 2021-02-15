sub1 = "NABox data collection not working for one or more hosts. Hostname:something.company.com"
sub2 = "Connection to NAbox has failed"
sub3 = "Connection to sqlite database failed"
sub4 = "The NABoxMon database table is missing or has been deleted or modified"
sub5 = "Error! cannot create the database connection"
sub7 = "NABox data collection not working for one or more hosts. Unable to register a ticket"
msg1 = "NABox data collection not working for one or more hosts\n\n There seems to be a problem with harvest services.\\n\n Contact Netapp Administrator for questions"
msg2 = "Connection to NAbox has failed.\n It could be the credentials.\n Check scripts config.py file if it has been modified. You can check the credentials against pwrepo to validtate if the contents are wrong."
msg3 = "Connection to sqlite database failed.\n\n The records might not be saved in the NABoxMon database.\n But the NABox itself could be working fine.\n You can login on the NABox webconsole to double check this or check if grafana has its graphs up to date in the past few hours. "
msg4 = "The NABoxMon database table is missing or has been deleted or modified.\n The script is unable to create new Database table with the same name. \n. But the NABox itself could be working fine.\n You can login on the NABox webconsole to double check this or check if grafana has its graphs up to date in the past few hours. "
msg5 = "Error! cannot create the database connection. \nOnly if the database creation happens, the records of NABox datacollection status can be saved in the NABoxMon db. \n But the NABox itself could be working fine.\n You can login on the NABox webconsole to double check this or check if grafana has its graphs up to date in the past few hours. "
msg6 = "Everythin looks good!\n NABox Harvest collection works fine. \n\nThe sqlite db table has been updated with the records.\n\n\n Have a wonderful day wizard! :-)"
msg7 = "NABox  data collection not working for one or more hosts. Unable to register a ticket in Marvel\n Follow instructions on how to login and check if something isn't working as expected"
msg8 = "Deletion of records older than 30 days failed in the SQlite database. \n\n Contact Netapp Administrator(Storage team) for questions"