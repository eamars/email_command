### Email Command Auto Response System
#### Author: Ran Bao

HOWTO:

1. Fillin your config.ini
2. Send the your command email to your imap account
3. Run check_email.py by Python3 or later


Email format:

You need to specify your subject of your command email to "COMMAND\_EMAIL\_SUBJECT". Then you can insert any of your command enclosed by [command] and [/command]. The format of email can either be 'text/plain'(untested) or 'text/html'.

