#!/bin/sh
#TS=`date +%m%d_%H%M`
APLIST=/tmp/apmaclist

for ap in `cut -d',' -f1 $APLIST`; do
    echo "$ap ..."
    aap=${ap//:/_}
    b=`rclient -d $ap -s -c "top -n 1"> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "uptime">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "date">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "nodestats">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "nodestats wifi1">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "athstats -i wifi0 | grep 'Busy' ">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "athstats -i wifi1 | grep 'Busy' ">> /tmp/datafile.$aap` 
    b=`rclient -d $ap -s -c "athstats -i wifi1 | grep 'beacons transmitted' "` 
    b_no=`echo $b | awk '{print $1}'`
    sleep 10
    b_new=`rclient -d $ap -s -c "athstats -i wifi1 |grep 'beacons transmitted'"` 
    b_no_new=`echo $b_new | awk '{print $1}'`
    if [ $b_no -eq $b_no_new ]
    then
      
        if [ "$b_no" != "" ]
            then
               echo "$b_no ..."
               echo 'beacon stuck found collecting all logs' >> /tmp/datafile.$aap
        fi
    fi
    b=`rclient -d $ap -s -c "athstats -i wifi0  "> /tmp/athstats_wifi0.$aap` 
    b=`rclient -d $ap -s -c "athstats -i wifi1  "> /tmp/athstats_wifi1.$aap` 
    rclient -d $ap -s -c "cat /dev/v54rb0" >> /tmp/datafile.$aap
    rclient -d $ap -s -c "cat /dev/v54rb1" >> /tmp/datafile.$aap
    rclient -d $ap -s -c "cat /dev/v54rb2" >> /tmp/datafile.$aap
    b=`rclient -d $ap -s -c "logread"> /tmp/logread.$aap` 

    echo "$aap ..." > /tmp/stats80211.$aap
    b=`rclient -d $ap  -c "get wlanlist" > wlanlist`
    awk '{ if ( $2 == "up" ) print $1 }' > wlist wlanlist
    for wlan in `cat wlist`; do
        echo "$wlan ..." >> /tmp/stats80211.$aap
        b=`rclient -d $ap  -s -c "80211stats -i  $wlan " >> /tmp/stats80211.$aap`

         done

done
    tar -czf /tmp/datafileall.tgz /tmp/datafile.*
    tar -czf /tmp/logreadall.tgz /tmp/logread.*
    tar -czf /tmp/athstatswifi0all.tgz /tmp/athstats_wifi0.*
    tar -czf /tmp/athstatswifi1all.tgz /tmp/athstats_wifi1.*
    tar -czf /tmp/stats80211all.tgz /tmp/stats80211.*
    tar -czf /tmp/eventall.tgz /data/log/system/event.log
    su admin -c 'scp /tmp/datafileall.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    su admin -c 'scp /tmp/logreadall.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    su admin -c 'scp /tmp/athstatswifi0all.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    su admin -c 'scp /tmp/athstatswifi1all.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    su admin -c 'scp /tmp/stats80211all.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    su admin -c 'scp /tmp/eventall.tgz wspbackup@10.150.13.7:/home/wspbackup/scg_rms/.'
    rm -rf /tmp/datafile*
    rm -rf /tmp/logread*
    rm -rf /tmp/athstats*
    rm -rf /tmp/stats80211*
    rm -rf /tmp/eventall.tgz
