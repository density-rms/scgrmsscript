#!/bin/sh
rec="anney.morris@ruckuswireless.com,prem.sagar@ruckuswireless.com, amrit.lamba@ruckuswireless.com,posen.hung@ruckuswireless.com,phong.ngo@ruckuswireless.com"
#rec="koti.mellachervu@ruckuswireless.com,ilango@ruckuswireless.com,david.jea@ruckuswireless.com,venkat.chirreddy@ruckuswireless.com,henry.zeng@ruckuswireless.com,wchen@ruckuswireless.com,anney.morris@ruckuswireless.com sang.le@ruckuswireless.com prem.kanumuri@ruckuswireless.com amrit.lamba@ruckuswireless.com,vandana.singh@ruckuswireless.com"
#rec="dkaiser@ruckuswireless.com ming.tsang@ruckuswireless.com harkirat.singh@ruckuswireless.com abhishek.rawat@ruckuswireless.com anney.morris@ruckuswireless.com amrit.lamba@ruckuswireless.com rhudnut@ruckuswireless.com awang@ruckuswireless.com bruce.himebauch@ruckuswireless.com prem.kanumuri@ruckuswireless.com"
subject="Video54-sz100-network-AP-status"
if [ $# -eq 2 ]
  then 
     mfile1=$1
     mfile2=$2
    mutt -s $subject -x  -a $mfile1 -a $mfile2 -- $rec < mymessage 
 else
    mfile1=$1
    mutt -s $subject -x  -a $mfile1 -- $rec < mymessage 
fi

