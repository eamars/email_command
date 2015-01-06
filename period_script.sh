#!/bin/bash
LOG="check_email.log"
echo "---$(date)---" >> $LOG
python3 check_email.py >> $LOG
echo "---end---" >> $LOG
