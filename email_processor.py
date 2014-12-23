import email
from email.parser import HeaderParser
from debug import *

email_processor_debug = Debugger(DEBUG)

# Get text part of email address
def get_text_block(raw_msg):
    msg = email.message_from_string(raw_msg)
    text = ""

    if msg.is_multipart():
        for part in msg.get_payload():

            # if charset is unknown
            if part.get_content_charset() is None:
                text = part.get_payload(decode=True)
                continue

            charset = part.get_content_charset()

            if part.get_content_type() == "text/plain":
                text = part.get_payload(decode=True).decode(str(charset))
            if part.get_content_type() == "text/html":
                email_processor_debug.log(DEBUG, "html part wrote to a.html")
                buf = part.get_payload(decode=True).decode(str(charset))
                f = open("a.html", "w")
                f.write(buf)
                f.close()
    else:
        email_processor_debug.log(DEBUG, "unknown part wrote to a.txt")
        buf = msg.get_payload(decode=True).decode(str(msg.get_content_charset()))
        f = open("a.txt", "w")
        f.write(buf)
        f.close()

    return text

class Message:
    def __init__(self, raw_message):
        self.raw_message = raw_message;
        self.sender = None
        self.receiver = None
        self.subject = None
        self.text = None


        # Process
        message = HeaderParser().parsestr(raw_message)
        self.sender = email.utils.parseaddr(message["From"])
        self.receiver = email.utils.parseaddr(message["To"])
        self.subject = message["Subject"]
        self.text = get_text_block(raw_message)
