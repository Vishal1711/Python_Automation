from datetime import datetime
import psutil
from sys import *
import time
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_emails(email_list,path,pswd):

    # Setup port number and server name

    smtp_port = 587                     # standard secure SMTP port
    smtp_server = "smtp.gmail.com"      # Google SMTP server

    email_from = "jadhavvishal669@gmail.com"

    # Define the password (better to reference externally)


    # name the email subject
    subject = "Assignment 12: Send Gmail Using Python"

    for person in email_list:

        # Make the body of the email
        body = f"""
        Hello Sir,

        Attached is the log file of all running process. 

        Thanks,
        Vishal
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = path

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()

def ProcessDisplay(log_dir='log'):
    listprocess = []
    print(log_dir)

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "-"*80
    log_path = os.path.join(log_dir, "ProcessLog%s.log"%(datetime.now().strftime("%H_%M_%d_%m_%Y")))

    f = open(log_path, 'w')
    f.write(separator + "\n")
    f.write("Process Logger: "+ time.ctime() + "\n")
    f.write(separator + "\n")
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid','name','username'])
            vms = proc.memory_info().vms/(1024*1024)
            pinfo['vms'] = vms
            listprocess.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for element in listprocess:
        f.write("%s\n" %element)

    return log_path


def main():
    print("Python Automation: Accept Directory Name and Create Log of all running process")

    print('Application Name: '+ argv[0])

    if (len(argv) != 3):
        print("Error: Invalid number of arguments")
        exit()

    if (argv[1]=="-h") or (argv[1]=='=H'):
        print("Script is used log recoed of all running process")
        exit()
    
    if (argv[1]=='-u') or (argv[1]=='-U'):
        print("Usage: Application_Name AbsolutePathof_Directory")
        exit()
    
    try:
        path = ProcessDisplay(argv[1])
        email_list = ["vjadhav@clemson.edu","vishal.jadhav@vimaan.ai"]

        send_emails(email_list,path, argv[2])
    
    except ValueError:
        print("Error: Invalid datatype of input")

    except Exception:
        print("Error: Invalid Input")


if __name__ == "__main__":
    main()
