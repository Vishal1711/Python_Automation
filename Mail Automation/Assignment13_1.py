import os
from sys import *
import hashlib
import schedule
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import schedule

# Function for mail sending
def send_emails(email_list,path,pswd):

    # Setup port number and server name

    smtp_port = 587                     # standard secure SMTP port
    smtp_server = "smtp.gmail.com"      # Google SMTP server

    email_from = "jadhavvishal669@gmail.com"

    # Define the password (better to reference externally)


    # name the email subject
    subject = "Duplicate log files from given directory"

    for person in email_list:

        # Make the body of the email
        body = f"""
        Hello,

        Attached is the log file of all deleted log files. 

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

def DeleteFiles(dict):
    results = list(filter(lambda x:len(x) > 1, dict.values()))

    icnt = 0
    if len(results) > 0:
        for result in results:
            for subresult in result:
                icnt += 1
                if icnt >=2:
                    os.remove(subresult)
            icnt = 0
    else:
        print("No duplication found")


def hashfile(path, blocksize = 1024):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf)>0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()

    return hasher.hexdigest()

def FileDuplicate(path):

    flags = os.path.isabs(path)
    if flags == False:
        path = os.path.abspath(path)

    exists = os.path.isdir(path)

    dups = {}
    if exists:
        for folderpath,subfolder,filename in os.walk(path):
            for filen in filename:
                path = os.path.join(folderpath, filen)
                file_hash = hashfile(path)

                if file_hash in dups:
                    dups[file_hash].append(path)
                else:
                    dups[file_hash] = [path]
        return dups
            
    else:
        print("Invalid Path")

def LogDuplicate(dict):
    results = list(filter(lambda X:len(X)>1, dict.values()))
    log_dir = 'marvellous'
    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    if len(results) > 0:
        print('Duplicates found')
        log_path = os.path.join(log_dir, "DuplicateFileLog%s.log"%(datetime.now().strftime("%H_%M_%d_%m_%Y")))
        fd = open(log_path,'w')
        fd.write('-'*100 +'\n')
        fd.write("Following files are duplicate:\n")
        fd.write('-'*100 +'\n')
        for result in results:
            for subresult in result:
                fd.write(subresult+'\n')
        fd.close()
    else:
        print("No duplication found")
    
    return log_path

def main():
    print("This application delete all duplicate files from given directory and mail the log of all deleted files")
    print(60*'-')

    if (len(argv)<3):
        print("Insufficient arguments")
        exit()

    if (argv[1] == '-H' or argv[1] == '-h'):
        print("This scripts is use to mail log of all duplicate files from given directory")
        exit()

    if (argv[1] == '-U' or argv[1] == '-u'):
        print("Usage: [File.py] [Directory] [Time (min)] [pswd]")
        exit()

    try:
        Duplicate = {}
        Duplicate = FileDuplicate(argv[1])
        path = LogDuplicate(Duplicate)
        DeleteFiles(Duplicate)
        email_list = ["vjadhav@clemson.edu","vishal.jaadhav@viman.ai"]

        send_emails(email_list,path, argv[3])

    
    except ValueError:
        print("Error: Invalid Data Type")

    except Exception:
        print("Error: Invalid Input")

if __name__ == "__main__":
    main()
    t = int(argv[2])
    schedule.every(t).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
