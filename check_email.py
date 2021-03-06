import imaplib
import smtplib
import sys

from email_processor import Message
from command_processor import process_command
from send_email import send_reply
from configparser import ConfigParser

# Load configuration from config.ini
print("Loading config", end='')
config = ConfigParser()
config.read("config.ini")

imap_addr = config["default"]["imap_addr"]
smtp_addr = config["default"]["smtp_addr"]
imap_usr = config["default"]["imap_usr"]
imap_pwd = config["default"]["imap_pwd"]
smtp_usr = config["default"]["smtp_usr"]
smtp_pwd = config["default"]["smtp_pwd"]

use_proxy = config["proxy"]["enable"]
proxy_addr = config["proxy"]["proxy_addr"]
proxy_port = config["proxy"]["proxy_port"]
proxy_usr = config["proxy"]["proxy_usr"]
proxy_pwd = config["proxy"]["proxy_pwd"]
proxy_type = config["proxy"]["proxy_type"]

print(" -- done")

# use proxy
if use_proxy == "true":
    print("Configurating proxy", end='')
    sys.stdout.flush()

    import socks
    import socket

    if proxy_type == "PROXY_TYPE_SOCKS4":
        s = socks.PROXY_TYPE_SOCKS4
    else:
        s = socks.PROXY_TYPE_SOCKS5

    if proxy_usr != '' or proxy_pwd != '':
        proxy_full_addr = "{}:{}@{}".format(proxy_usr, proxy_pwd, proxy_addr)
    else:
        proxy_full_addr = proxy_addr

    # Override default socket settings
    socks.setdefaultproxy(
        s,
        proxy_full_addr,
        int(proxy_port),
        True)

    socket.socket = socks.socksocket
    print(" -- done")

# Connect to IMAP server
print("Connecting to Gmail IMAP4", end='')
sys.stdout.flush()
mailbox = imaplib.IMAP4_SSL(imap_addr)
print(" -- done")

# Login to IMAP server
print("Authorizing IMAP", end='')
sys.stdout.flush()
mailbox.login(imap_usr, imap_pwd)
print(" -- done")

# Connect to SMTP server
print("Connecting to Gmail SMTP", end='')
sys.stdout.flush()
sendbox = smtplib.SMTP_SSL(smtp_addr)
print(" -- done")

# Login to SMTP server
print("Authorizing SMTP", end='')
sys.stdout.flush()
sendbox.ehlo()
sendbox.login(smtp_usr, smtp_pwd)
print(" -- done")


# List all folders in mailbox
mailbox.list()
mailbox.select(readonly=0) # default to inbox

# Search for any of unread
criterion = "(UNSEEN)"
print("Fetching messages with criterion:", criterion, end='')
sys.stdout.flush()
(retcode, messages) = mailbox.search(None, criterion)
print(" --", retcode)

# Fetch email_id from server
ids = messages[0].decode().split() # Ids is the space sparated byte

# Fetch corresponding email with their id
for id in ids:
    (retcode, data) = mailbox.fetch(id, "(RFC822)")

    # Fetch email string for parser
    raw_email = data[0][1].decode()

    # Construct Message object from raw_message
    m = Message(raw_email)

    # Process command email
    if m.subject == "COMMAND_EMAIL_SUBJECT":
        # process command
        print("Subject:", m.subject)
        print("Sender:", "{} <{}>".format(m.sender[0], m.sender[1]))
        print("Executing commands", end='')
        sys.stdout.flush()
        reply = process_command(m.text)
        print(" -- done")
        print(reply)

        # reply message
        print("Sending reply", end='')
        sys.stdout.flush()
        send_reply(sendbox, m, reply)
        print(" -- done")

        # Mark as read
        print("Set command email as SEEN", end='')
        sys.stdout.flush()
        (retcode, data) = mailbox.uid("STORE", id, "+FLAGS", "(\\Seen)")
        print(" --", retcode, [d.decode() for d in data])
        print()





print("Logging out", end='')
sys.stdout.flush()

mailbox.close()
sendbox.close()

mailbox.logout()

print(" -- done")
