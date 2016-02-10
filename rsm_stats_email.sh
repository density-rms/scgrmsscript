#!/bin/sh
rec="anney.morris@ruckuswireless.com prem.kanumuri@ruckuswireless.com koti.mellachervu@ruckuswireless.com,venkat.chirreddy@ruckuswireless.com, amrit.lamba@ruckuswireless.com tlin@ruckuswireless.com"
mfile=$1
yest=$(date --date="yesterday" +"%m/%d/%Y")
subject="Daily_report_for_rsm_process_restart_info_for_$yest"
mutt -s $subject -x  -a $mfile -- $rec < /home/rms/video54_rms/rsmmessage 

