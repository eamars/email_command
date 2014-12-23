from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_reply(server, message, reply):
    text = ""
    for item in reply:
        text += ">> " + item + "\n" + reply[item] + '\n'

    msg = MIMEText(text)
    msg["Subject"] = "COMMAND_EMAIL_REPLY_AT_" + str(datetime.now())
    msg["From"] = "AUTO_RESPONSE_BOT"
    msg["To"] = message.sender[1]



    server.send_message(msg)

if __name__ == "__main__":
    pass