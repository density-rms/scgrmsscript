#!/bin/sh
cd /tmp
ap=$1 
aap=${ap//:/_}
echo "$ap ..."
rclient -d $ap -c  "support"
#sleep 10
rclient -d $ap -s -c "cat /tmp/support" > /tmp/support$ap.txt
su admin -c "scp /tmp/support$ap.txt wspbackup@10.150.13.7:/home/wspbackup/scg_rms/."
rm -f /tmp/support*.txt

