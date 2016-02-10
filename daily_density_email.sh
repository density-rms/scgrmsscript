#!/bin/sh
#rec="anney.morris@ruckuswireless.com"
rec="posen.hung@ruckuswireless.com,andy.lim@ruckuswireless.com,robert.hobson@ruckuswireless.com,DL-R710-QA@ruckuswireless.com,anney.morris@ruckuswireless.com sang.le@ruckuswireless.com prem.kanumuri@ruckuswireless.com amrit.lamba@ruckuswireless.com,rhudnut@ruckuswireless.com"
#rec="dkaiser@ruckuswireless.com ming.tsang@ruckuswireless.com harkirat.singh@ruckuswireless.com abhishek.rawat@ruckuswireless.com anney.morris@ruckuswireless.com amrit.lamba@ruckuswireless.com rhudnut@ruckuswireless.com awang@ruckuswireless.com bruce.himebauch@ruckuswireless.com prem.kanumuri@ruckuswireless.com"
mfile=$1
yest=$(date --date="yesterday" +"%m/%d/%Y")
subject="Daily_report_for_Video54(IT)_SZ100_network_for_$yest"
mutt -s $subject -x  -a $mfile -- $rec < /home/rms/video54_rms/dailymessage 

