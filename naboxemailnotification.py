import smtplib
from email.message import EmailMessage
import errormessages
from datetime import datetime, time
import sys
sys.setrecursionlimit(100)


def notify(message,affectedsystems="",subject="NABox Notification"):
    server = smtplib.SMTP('mailingurl')
    msg = EmailMessage()
    fullmessage = message + "\n\n One or more systems are not collecting data. \n\n\nSystems' datacollection affected are:\n" + affectedsystems
    msg.set_content(message) if affectedsystems == "" else msg.set_content(fullmessage)
    msg['Subject'] = subject
    msg['From'] = "address.company.com"
    msg['To'] = "naboxalerts@company.com"
    server.send_message(msg)
    server.quit()

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


if __name__ == '__main__':
   notify(message,affectedsystems)
   eventnotify(message,affectedsystems,subject)