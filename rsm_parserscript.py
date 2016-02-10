#!/usr/bin/python2.7

import re, csv
import sys, os
import  time 
import datetime
import calendar
import pandas as pd

TIME_FORMAT = '%Y-%m-%d-%H:%M:%S'
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
def get_year():
    cmd = 'date -d "yesterday 13:00" \'+%Y %b %d\''
    mydate = os.popen(cmd).read()
    current_year = mydate.split()[0]

    return current_year  
def scgutc_localtime_conversion(ts,todaydate):
    timestamp = calendar.timegm(datetime.datetime.strptime(ts,TIME_FORMAT).timetuple())
    local = datetime.datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
    if todaydate in local:
                #local_time = ' '.join(s for s in local.split('-'))
                return local
    else:
                return False
def get_todaydate_clientfile():
    ### get today's date and filter the log
    cmd = 'date -d "today" \'+%b %d\''
    mydate = os.popen(cmd).read()
    print mydate
    if mydate[4] == '0':
        todaydate = (mydate[:3]+' '+mydate[5]).rstrip()
    else:
        todaydate = mydate.rstrip()
    print todaydate
    
    return(todaydate)
def get_todaydate_aplog():
    ### get today's date and filter the log
    cmd = 'date -d "today" \'+%b %d\''
    #cmd = 'date -d " days ago" \'+%b %d\''
    mydate = os.popen(cmd).read()
    #print mydate
    if mydate[4] == '0':
        todaydate = (mydate[:4]+' '+mydate[5]).rstrip()
    else:
        todaydate = mydate.rstrip()
    print todaydate
    return(todaydate)

def get_todaydate_scglog():
    ### get today's date and filter the log
    cmd = 'date -d "today" \'+%Y-%m-%d\''
    #cmd = 'date -d "1 days ago" \'+%b %d\''
    mydate = os.popen(cmd).read()
    print mydate
    todaydate = mydate.rstrip()
    print todaydate
    return(todaydate)

def get_ydate_scglog():
    ### get today's date and filter the log
    cmd = 'date -d "1 days ago" \'+%Y-%m-%d\''
    #cmd = 'date -d "one days ago" \'+%b %d\''
    mydate = os.popen(cmd).read()
    print mydate
    todaydate = mydate.rstrip()
    print todaydate
    return(todaydate)

def walcsv_writer(ap_walDict,tstamp):
    csvfile1 = 'wal_stats_%s.csv' % tstamp 
    csvPtr1 = open(csvfile1,"w") 
    fieldnames1 = ['ap','ts','action']
    dwriter1= csv.DictWriter(csvPtr1,fieldnames1, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    csvPtr1.write(','.join(fieldnames1)+'\r\n')
    for ap in ap_walDict.keys():
        for ts in sorted(ap_walDict[ap].keys()):
            dwriter1.writerow(ap_walDict[ap][ts])
    csvPtr1.close()
    print "WAL stats are saved in file %s\n" % (csvfile1)
    return (csvfile1) 

def switchcsv_writer(ap_switchDict,tstamp):
    csvfile1 = 'switching_stats_%s.csv' % tstamp 
    csvPtr1 = open(csvfile1,"w") 
    fieldnames1 = ['ap','ts','action']
    dwriter1= csv.DictWriter(csvPtr1,fieldnames1, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    csvPtr1.write(','.join(fieldnames1)+'\r\n')
    for ap in ap_switchDict.keys():
        for ts in sorted(ap_switchDict[ap].keys()):
            dwriter1.writerow(ap_switchDict[ap][ts])
    csvPtr1.close()
    print "AP channel switching stats are saved in file %s\n" % (csvfile1)
    #file2 ="switching_stats.csv"
    #cmd = 'cp %s /var/www/densitystatus/dailystaus/%s' % (csvfile1,file2)
    #os.system(cmd)
    return (csvfile1) 

def statscsv_writer(statsDict,tstamp):
    csvfile1 = 'stats80211_%s.csv' % tstamp 
    csvPtr1 = open(csvfile1,"w") 
    fieldnames1 = ['ap','wlan','max_data_retries','max_BAR_retries','send_disassoc','rx_data_from_non','idle_timeout']
    dwriter1= csv.DictWriter(csvPtr1,fieldnames1, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    csvPtr1.write(','.join(fieldnames1)+'\r\n')
    for ap in statsDict.keys():
        for wlan in sorted(statsDict[ap].keys()):
            #print statsDict[ap][wlan]
            dwriter1.writerow(statsDict[ap][wlan])
    csvPtr1.close()
    print "Client disassoc stats for all APs from 80211stats is saved in file %s\n" % (csvfile1)
    #file2 ="switching_stats.csv"
    #cmd = 'cp %s /var/www/densitystatus/dailystaus/%s' % (csvfile1,file2)
    #os.system(cmd)
    return (csvfile1) 

def statslogcsv_writer(statslogDict,tstamp):
    # this writes the dictionary from logread for disassoc
    csvfile1 = 'statslog_%s.csv' % tstamp 
    csvPtr1 = open(csvfile1,"w") 
    fieldnames1 = ['ap','ts','hint']
    dwriter1= csv.DictWriter(csvPtr1,fieldnames1, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    csvPtr1.write(','.join(fieldnames1)+'\r\n')
    for ap in statslogDict.keys():
        for ts in sorted(statslogDict[ap].keys()):
            dwriter1.writerow(statslogDict[ap][ts])
    csvPtr1.close()
    print "Client disassoc stats for APs from logread is saved in file %s\n" % (csvfile1)
    #file2 ="switching_stats.csv"
    #cmd = 'cp %s /var/www/densitystatus/dailystaus/%s' % (csvfile1,file2)
    #os.system(cmd)
    return (csvfile1) 
def rsm_summary_writer(newprocDict,dDict,newDict,tstamp):
    
    csvfile1 = "rsm_summary.csv" 

    try:
        staCsvPtr= open('%s' % csvfile1,"wb")
    except IOError:
        print "cannot open CSV file, exiting\n"

    fieldnames = ['ap name','ap ip','List of restarted process and count)']
    dwriter= csv.writer(staCsvPtr, delimiter= ',')

    staCsvPtr.write(','.join(fieldnames)+'\r\n')  
    #for k,v in sorted(cntDict.iteritems()):
    #for k,v in (cntDict.iteritems(), key = lambda(k,v):int(v), reverse=True):
        #dwriter.writerow((k,v))
    #staCsvPtr.close()
    dwriter.writerow(" ")
    for ap in newDict:
        staCsvPtr.write(','.join(newDict[ap])+'\r\n') 

    dwriter.writerow(" ")
    dwriter.writerow(" ")
    dwriter.writerow(('process','Total count for all APs'))
    dwriter.writerow(" ")
    for k,v in (newprocDict.items()):
        dwriter.writerow((k,v)) 
    dwriter.writerow(" ")
    dwriter.writerow(" ")
    dwriter.writerow(('process','List of APs for each process'))
    dwriter.writerow(" ")
    for k,v in (dDict.items()):
        dwriter.writerow((k,v))    
    staCsvPtr.close() 
    return csvfile1
def get_client_count(csv1,timestamp):
    ## this adds a row to the moving_client.csv file 
    ## Add the current value for client sum and channel change
    report_dir = '/var/www/densitystatus/dailystatus/'
    df = pd.read_csv('%s' % (csv1))
    g_sum = df['g_client_count'].sum() 
    a_sum = df['a_client_count'].sum() 
    g_ch_switch_sum = df['2g_ch_switch_count'].sum() 
    a_ch_switch_sum = df['5g_ch_switch_count'].sum()     
    df1 = pd.read_csv('%s/moving_client.csv' % (report_dir))
    tt= df1.drop(df1.index[0])  ## remving the first row
    t = time.strftime('%H:%M', time.localtime(timestamp))
    df2 = pd.DataFrame({'eventtime':t,
                        'sum_gclient':g_sum,
                        'sum_aclient':a_sum,
                        'sum_a_ch_switch':g_ch_switch_sum,
                        'sum_g_ch_switch':a_ch_switch_sum}, index=[0])
    tt1 = tt.append(df2)   ## adding a new row
    tt1.to_csv('%s/moving_client.csv' % report_dir,index=False,header=True)
def csvfile_writer(apDict,ap_clientDict,tstamp):
    csvfile1 = 'ap_stats_%s.csv' % tstamp 
    csvfile2 = 'client_stats_%s.csv' % tstamp 
    csvPtr1 = open(csvfile1,"w")
    csvPtr2 = open(csvfile2,"w")
    fieldnames1 = ['ap','ip','ap_name','model','uptime','g_client_count','a_client_count','cpuUse','per_memoryUsage', '2g_ch_switch_count','5g_ch_switch_count','heartbeatlost_count','heartbeatlost_time','reboot_count','upgrade_reboot_count','reboot_reason','target_assert_count','target_assert_times','tx_desc_stuck_count','tx_desc_stuck_times','wmi_stuck_count','wmi_lasttime_reported','target_inactive_count','target_inactive_times','beacon_stuck','2g_ch_util_Busy','2g_ch_util_RX','2g_ch_util_TX','2g_ch_util_Total','5g_ch_util_Busy','5g_ch_util_RX','5g_ch_util_TX','5g_ch_util_Total']
    fieldnames2 = ['station','ts','action','name','radio','auth_difficult_wlan','hint','rx_rssi','ack_rssi','reason','receivedSS','freq','chan','stats','ap','ip','total_bytes','elapsed_time_sec']    
    dwriter1= csv.DictWriter(csvPtr1,fieldnames1, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    dwriter2= csv.DictWriter(csvPtr2,fieldnames2, dialect = 'excel', delimiter= ',', extrasaction='ignore')
    csvPtr1.write(','.join(fieldnames1)+'\r\n')
    for key in apDict.keys():
        #print key
        if 'ip' not in apDict[key].keys() or apDict[key]['ip'] == 'unknown':
            continue
        dwriter1.writerow(apDict[key])
    csvPtr1.close()
    csvPtr2.write(','.join(fieldnames2)+'\r\n')
    for mac in ap_clientDict.keys():
        for ts in sorted(ap_clientDict[mac].keys()):
            dwriter2.writerow(ap_clientDict[mac][ts])
    csvPtr2.close()
    print "Network stats are saved in files %s  and %s \n" % (csvfile1,csvfile2)
    return (csvfile1, csvfile2)
    
def utc_localtime_conversion(year,ts,todaydate):
    (m,d,t) = ts.split()
    if m in months:
        m_index = months.index(m) 
    utc_str ='-'.join([year,str(m_index+1),d,t])  
    #print utc_str
    timestamp = calendar.timegm(datetime.datetime.strptime(utc_str,TIME_FORMAT).timetuple())
    local = datetime.datetime.fromtimestamp(timestamp).strftime(TIME_FORMAT)
    #print local
    (a,b,c,e) = local.split('-')
    if b[0] == '0':
        nb = b[1]
    else:
        nb = b
    if nb == str(m_index+1) or nb == str(m_index) :
            if c[0] == '0':
                nd = c[1]
            else:
                nd = c
            #if nd == d:

            ts_new = ' '.join([months[int(nb)- 1],nd,e])  
            if todaydate in ts_new:
                #local_time = ' '.join(s for s in local.split('-'))
                return ts_new
            else:
                return False

def ap_reboot_dict(timestamp,email_flag,apDict,ap_clientDict,apmacDict,apipDict,apmodelDict,message_fp,heartbeat_ap_list):
 
    #heartbeat_ap_list = []
    start_time = timestamp 
    rebootDict = apDict 
    todaydate = get_todaydate_scglog()
    yesterdaydate = get_ydate_scglog()
    print todaydate
    ### reading the ap.log file and grep only reboot and heartbeat
    c_dir = os.getcwd() 
    print c_dir
    os.system('cat %s/writable/event_sz1.log | grep %s > eventlog' % (c_dir,yesterdaydate))
    os.system('cat %s/writable/event_sz1.log | grep %s >> eventlog' % (c_dir,todaydate))
    os.system('cat %s/writable/event_sz2.log | grep %s >> eventlog' % (c_dir,yesterdaydate))
    os.system('cat %s/writable/event_sz2.log | grep %s >> eventlog' % (c_dir,todaydate))    
    os.system('cat %s/eventlog |grep -i "clientRoaming" >clientroaming' % (c_dir))
    os.system('cat %s/eventlog |grep -i "clientDisconnect" >clientdisconnect' % (c_dir))
    os.system('cat %s/eventlog |grep -i "clientInactivityTimeout" >> clientdisconnect' % (c_dir))
    os.system('cat %s/eventlog |grep -i "apHeartbeatLost" > apheartbeatlost' % (c_dir))
    os.system('cat %s/eventlog |grep -i "apRebootBy" > apreboot' % (c_dir))
    os.system('cat %s/eventlog |grep -i "apChannelCh" > apchannelchange' % (c_dir))
    pattern22 = "([0-9T:\s\-]+).*?clientRoaming.*?clientMac=(.*?),.*?toRadio=(.*?),.*?receivedSignalStrength=(-\d+),"
    pattern23 = '([0-9T:\s\-]+).*?clientDisconnect.*?clientMac=(.*?),.*?hostname=(.*?),.*?sessionDuration=(\d+),disconnectReason=(\d+),.*?rxBytes=(\d+),.*?txBytes=(\d+),.*?receivedSignalStrength=(-\d+)'
    #pattern23 = '([0-9T:\s\-]+).*?clientDisconnect.*?clientMac=(.*?),.*?hostname=(.*?),.*?sessionDuration=(\d+),'
    pattern24 = '([0-9T:\s\-]+).*?clientInactivityTimeout.*?clientMac=(.*?),.*?hostname=(.*?),.*?sessionDuration=(\d+),disconnectReason=(\d+),.*?rxBytes=(\d+),.*?txBytes=(\d+),.*?receivedSignalStrength=(-\d+)'
    pattern25 = "([0-9T:\s\-]+).*?apHeartbeatLost,apMac=(.*?),.*?timestamp=(\d+),"
    pattern26 = "([0-9T:\s\-]+).*?apChannelCha.*?,apMac=(.*?),radio=(.*?),fromChannel=(\d+),toChannel=(\d+),"
    #pattern26 = "([0-9T:\s\-]+).*?channel-wifi(\d):.*?apChannelChange,apMac=(.*?),radio"   
    pattern27 = "([0-9T:\s\-]+).*?apRebootBy.*?,apMac=(.*?),reason=([\w\s]+),"

    fp_input = open("apreboot" , "r")

    for line in fp_input.readlines():
        line = line.replace('"','')
        res27 = re.search(pattern27,line)
        if res27:
            AP = res27.group(2)   
            ap = AP.replace(':','_' )           
            ts = res27.group(1).replace('T','-')
            ts_new = scgutc_localtime_conversion(ts,todaydate)
            if ts_new:
                    (y,m,d,t) = ts_new.split('-')
                    slist = [int(x) for x in t.split(':')]
                    tlist = [int(y), int(m), int(d)]
                    tlist.extend(slist)
                    tlist.extend([1,1,1])
                    time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                    #print start_time-time_insec
                    if (start_time - time_insec) < 2500:
                        #print line
                        email_flag = 'yes'
                        heartbeat_ap_list.append(ap)
                        message_fp.write("ap %s (%s)  rebooted.\n" % (rebootDict[ap]['ap_name'],rebootDict[ap]['ip']))
                    reason = res27.group(3)
                    if ap not in rebootDict.keys():
                        rebootDict[ap] = {}
                        rebootDict[ap]['ap'] = ap
                        if AP in apmacDict.keys():
                            ip = apmacDict[AP]
                            ap_name = apipDict[ip] 
                            ap_model = apmodelDict[AP]
                            rebootDict[ap]['ip'] = ip
                            rebootDict[ap]['ap_name'] = ap_name
                            rebootDict[ap]['model'] = ap_model
                
                    if 'reboot_count' not in rebootDict[ap].keys():
                        rebootDict[ap]['reboot_count'] = 0 
                    if 'reboot_reason' not in rebootDict[ap].keys():
                        rebootDict[ap]['reboot_reason'] = [] 
                    rebootDict[ap]['reboot_count'] += 1
                    rebootDict[ap]['reboot_reason'].append((ts_new,reason))
            
                
    fp_input = open("apheartbeatlost" , "r")
    for line in fp_input.readlines():
        line = line.replace('"','')
        res25 = re.search(pattern25,line)
        if res25:
            AP = res25.group(2)
            ap = AP.replace(':','_')
            
            ts = res25.group(1).replace('T','-')
            ts_new = scgutc_localtime_conversion(ts,todaydate)
            if ts_new:
                    (y,m,d,t) = ts_new.split('-')
                    slist = [int(x) for x in t.split(':')]
                    tlist = [int(y), int(m), int(d)]
                    tlist.extend(slist)
                    tlist.extend([1,1,1])
                    time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                    #print start_time-time_insec
                    if (start_time - time_insec) < 2500:
                        #print line
                        email_flag = 'yes'
                        heartbeat_ap_list.append(ap)
                        message_fp.write("Heartbeat Loss for ap %s (%s)  \n" % (rebootDict[ap]['ap_name'],rebootDict[ap]['ip']))
                    reason = res25.group(3)
                    if ap not in rebootDict.keys():
                        rebootDict[ap] = {}
                        rebootDict[ap]['ap'] = ap
                        if AP in apmacDict.keys():
                            ip = apmacDict[AP]
                            ap_name = apipDict[ip] 
                            ap_model = apmodelDict[AP]
                            rebootDict[ap]['ip'] = ip
                            rebootDict[ap]['ap_name'] = ap_name
                            rebootDict[ap]['model'] = ap_model
                    if 'heartbeatlost_count' not in rebootDict[ap].keys():
                        rebootDict[ap]['heartbeatlost_count'] = 0 
                    rebootDict[ap]['heartbeatlost_count'] += 1
                    if 'heartbeatlost_time' not in rebootDict[ap].keys():
                        rebootDict[ap]['heartbeatlost_time'] = [] 
                    rebootDict[ap]['heartbeatlost_time'].append(ts)

    fp_input = open("apchannelchange" , "r")

    for line in fp_input.readlines():
        line = line.replace('"','')
        res26 = re.search(pattern26,line)
        if res26:
            AP = res26.group(2)
            ap = AP.replace(':','_')
                      
                
            ts = res26.group(1).replace('T','-')
            ts_new = scgutc_localtime_conversion(ts,todaydate)
            if ts_new:
                    if ap not in rebootDict.keys():
                        rebootDict[ap] = {}
                        rebootDict[ap]['ap'] = ap
                        if AP in apmacDict.keys():
                            ip = apmacDict[AP]
                            ap_name = apipDict[ip] 
                            ap_model = apmodelDict[AP]
                            rebootDict[ap]['ip'] = ip
                            rebootDict[ap]['ap_name'] = ap_name
                            rebootDict[ap]['model'] = ap_model
                    
                    if '5g_ch_switch_count' not in apDict[ap].keys():
                        apDict[ap]['5g_ch_switch_count'] = 0
                    if '2g_ch_switch_count' not in apDict[ap].keys():
                        apDict[ap]['2g_ch_switch_count'] = 0
                    radio = res26.group(3)
                    if radio == '11g/n' or radio == '11b/g/n':
                        apDict[ap]['2g_ch_switch_count'] += 1
                    else:
                        apDict[ap]['5g_ch_switch_count'] += 1
     

    fp_input = open("clientroaming" , "r")
    for line in fp_input.readlines():
        line = line.replace('"','')
        res22 = re.search(pattern22,line)
        if res22:
            
                ts = res22.group(1).replace('T','-')
                ts_new = scgutc_localtime_conversion(ts,todaydate)
                if ts_new:
    
                    ts = ts_new
                    radio = res22.group(3)
                    station_mac = res22.group(2)
                    RSSI = res22.group(4)
            
                    if station_mac not in ap_clientDict.keys():
                        ap_clientDict[station_mac] = {}
                    if ts not in ap_clientDict[station_mac].keys():
                        ap_clientDict[station_mac][ts] = {}                            
                    ap_clientDict[station_mac][ts]['ts'] = ts 
                    ap_clientDict[station_mac][ts]['action'] = 'roaming'
                    ap_clientDict[station_mac][ts]['station'] = station_mac 
                    ap_clientDict[station_mac][ts]['rssi'] = RSSI 
                    ap_clientDict[station_mac][ts]['radio'] = radio
                    
    fp_input = open("clientdisconnect" , "r")
    for line in fp_input.readlines():
        line = line.replace('"','')
        res23 = re.search(pattern23,line)    
        
        if res23: 
            ts = res23.group(1).replace('T','-')
            ts_new = scgutc_localtime_conversion(ts,todaydate)
            if ts_new:            
                ts = ts_new
                elapsed_time = res23.group(4)
                station_mac = res23.group(2) 
                station_name = res23.group(3)
                reason = res23.group(5)
                rx_bytes = res23.group(6)
                tx_bytes = res23.group(7)
                RSSI = res23.group(8)
                total_bytes = int(rx_bytes)+ int(tx_bytes)
                if not station_mac:
                    continue            
            
                if station_mac not in ap_clientDict.keys():
                    ap_clientDict[station_mac] = {}
                if ts not in ap_clientDict[station_mac].keys():
                    ap_clientDict[station_mac][ts] = {}                            
                ap_clientDict[station_mac][ts]['ts'] = ts                 
                ap_clientDict[station_mac][ts]['action'] = 'disConnect'
                ap_clientDict[station_mac][ts]['station'] = station_mac 
                ap_clientDict[station_mac][ts]['name'] = station_name 
                ap_clientDict[station_mac][ts]['elapsed_time_sec'] = elapsed_time
                ap_clientDict[station_mac][ts]['total_bytes'] = total_bytes
                ap_clientDict[station_mac][ts]['receivedSS'] = RSSI
                ap_clientDict[station_mac][ts]['reason'] = reason

    fp_input = open("clientdisconnect" , "r")
    for line in fp_input.readlines():
        line = line.replace('"','')
        res24 = re.search(pattern24,line)    
        
        if res24: 
            ts = res24.group(1).replace('T','-')
            ts_new = scgutc_localtime_conversion(ts,todaydate)
            if ts_new:           
                ts = ts_new
                elapsed_time = res24.group(4)
                station_mac = res24.group(2) 
                station_name = res24.group(3)
                reason = res24.group(5)
                rx_bytes = res24.group(6)
                tx_bytes = res24.group(7)
                RSSI = res24.group(8)
                total_bytes = int(rx_bytes)+ int(tx_bytes)
                if not station_mac:
                    continue            
            
                if station_mac not in ap_clientDict.keys():
                    ap_clientDict[station_mac] = {}
                if ts not in ap_clientDict[station_mac].keys():
                    ap_clientDict[station_mac][ts] = {}                            
                ap_clientDict[station_mac][ts]['ts'] = ts                 
                ap_clientDict[station_mac][ts]['action'] = 'clientInactive'
                ap_clientDict[station_mac][ts]['station'] = station_mac 
                ap_clientDict[station_mac][ts]['name'] = station_name 
                ap_clientDict[station_mac][ts]['elapsed_time_sec'] = elapsed_time
                ap_clientDict[station_mac][ts]['total_bytes'] = total_bytes
                ap_clientDict[station_mac][ts]['receivedSS'] = RSSI
                ap_clientDict[station_mac][ts]['reason'] = reason
                 
    message_fp.close()
    return(rebootDict,email_flag,heartbeat_ap_list)


def file_parser(timestamp,email_flag):
    todaydate = get_todaydate_clientfile()
    year = get_year()
    heartbeat_ap_list = []
    rsmcrash_ap_list = []
    message_fp = open('mymessage','w')
    message_fp.write('The following events happened on VIDEO54 SZ100 NETWORK in the last half hour\n\n')
    apDict = {} 
    logfilelist,datafilelist,rsmfilelist = [],[],[]
    start_time = timestamp
    pattern1 = '.*?Mem:\s+(\d+)K.*?(\d+)K.*?CPU:\s+(\d+).*?Load.*?up\s+(.*?)load'
    
    #pattern2 = '\s+(\d+)\s+(\d+)\s+(([a-zA-Z0-9:]+){5}[A-Za-z0-9]+)(\s+\d+){9}'
    pattern2 = '\s+(\d+)\s+(\d+)\s+[a-zA-Z0-9]+:[a-zA-Z0-9]+:'
    pattern21 =  'Dev:wifi(\d)\s+has\s+(\d+)\s+nodes' 
    pattern10 = 'beacon\s+stuck\s+found'
    pattern11 = '.*\[(.*?)\]\s+\[.*?\].*?stuck count:\s+(\d+).*?WMI:\s+halted:\s+(\d+)'
    pattern12 = '.*\[(.*?)\]\s+\[.*\].*?XXX\s+TARGET\s+ASSERTED\s+XXX'
    pattern14 = '.*\[(.*?)\]\s+\[Uptime.*?\]\s+(Wifi\d)\s+No Activity from target\s+\['
    pattern24 = '.*\[(.*?)\]\s+\[Uptime.*?\]\s+(Wifi\d)\s+Tx Desc Stuck:'
    pattern13 = '.*?Busy:\s+(\d+)\s+RX:\s+(\d+)\s+TX:\s+(\d+)\s+Total:\s+(\d+)'
    pattern3 = '\n([a-zA-Z]+\s+\d+\s+[\d:]+)\s+.*?channel-wifi(\d): channelfly'
    pattern4 = 'Command \'uptime \' executed.*?\n(.*?)\n.*?Command \'hostname \' executed'
    pattern6 ='\n([a-zA-Z]+\s+\d+\s+[\d:]+)\s+.*?Eved:\s+STA-DISASSOC-REASON\s+\[(.*?)\]\s+(.*?)\s+rx_rssi=(\d+),ack_rssi=(\d+),reason=(\d+),freq=(\d+),chan=(\d+),(.*?)\n'
    pattern7 ='\n([a-zA-Z]+\s+\d+\s+[\d:]+)\s+.*?(wlan\d+)\s+(.*?\s+):\s+Authentication Difficulty'

    filelist = os.listdir('writable/.')
    for f in filelist:
        if f.startswith('datafile'):
            datafilelist.append(f)
        elif f.startswith('logread'):
            logfilelist.append(f)
        elif f.startswith('rsmfile'):
            rsmfilelist.append(f)        
    # Creating the AP dictionary for name, ip, mac        
    names = pd.read_csv('apdetails.csv')
    aps = names[['apmac','apip','apname','model']]
    ap_ip_list = [] 
    apipDict = {}
    apmacDict = {}
    apmodelDict = {}
    for i in range (0,len(aps)):
        ap_ip_list.append(aps['apip'][i])
        apipDict[aps['apip'][i]] = aps['apname'][i]
        #print aps['apmac'][i]
        apmacDict[aps['apmac'][i].upper()] = aps['apip'][i]
        apmodelDict[aps['apmac'][i].upper()] = aps['model'][i]
        #apClientDict[aps['apmac'][i].upper()] = aps['clientCount'][i]
    #################################################################
    #################################################################
    ## for parsing rsm files
    pattern81 = '([a-zA-Z\-\_]+)\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+)\s+\d+\s+[a-zA-Z]+\s+'
    #pattern81 = '([a-zA-Z\-\_]+\s+\d+\s+)'
    #sys_init         10  0      0          0          0      0   0   0   ena  started
    #The list of processes with act feeds greater than 0 and the total count across all Aps connected to a specific SZ.
    #Per-AP distribution: Drill down to AP level
    #Per-process distribution: Drill down to process level 

    statsDict = {}
    for f in rsmfilelist:
        ap = f.split('.')[-1]
        if ap =='py' or ap == 'swp':
            continue
        ap_mac = ap.replace('_',':').upper()
        if ap_mac in apmacDict.keys():
            ip = apmacDict[ap_mac]
            if ap not in apDict.keys():
                ap_name = apipDict[ip]
                ap_model = apmodelDict[ap_mac]
        else:
            ip = 'unknown'
            continue
        ap = ap_name
        if ap not in statsDict.keys():
            statsDict[ap] = {}
        fp = open('writable/%s' % f, 'r')
        lines = fp.readlines()
        rsm_ap_list = []
        for l in lines:
            rsm_ap_list.append(l)
        rsmcrash_ap_list = (ap,rsm_ap_list)
        email_flag = 'yes'
        message_fp.write("process crash in  ap %s  ( %s ).\n" % (ap_name,ip)) 
         
        res81 = re.findall(pattern81, buff)
        if res81:
            #print res81
            for item in res81:
                if int(item[1]) > 0:
                    proc = item[0] 
                    count = int(item[1])
                    if count == 1:
                        rsm_flag = 'yes'
                        rsmcrash_ap_list.append(ap)
                    if proc not in statsDict[ap].keys():
                        statsDict[ap][proc] = {} 
                    statsDict[ap][proc]['count'] = count
                    statsDict[ap][proc]['ap'] = ap_name
                    statsDict[ap][proc]['ip'] = ip
                    statsDict[ap][proc]['proc'] = proc 
        #print statsDict
        procDict = {}
        distDict = {}
        apdistDict = {}
        dDict = {}
        newDict = {}
        newprocDict = {}
    for ap in statsDict:
        
        for proc in statsDict[ap]:
            if proc not in procDict.keys():
                procDict[proc] = {}
                procDict[proc]['sum'] = 0
                procDict[proc]['process'] = proc  
            procDict[proc]['sum'] += int(statsDict[ap][proc]['count'])
    for proc in procDict:
        newprocDict[proc] = procDict[proc]['sum']
   
    for ap in statsDict:
        for proc in statsDict[ap]:
            if proc not in distDict.keys():                
                distDict[proc] = {}
                distDict[proc]['aplist'] = []
            distDict[proc]['aplist'].append(ap)
    
    for proc in distDict.keys():
        x = "".join(str(distDict[proc]['aplist'])).strip('[]')
        dDict[proc] = x
        
    for ap in statsDict:
        apdistDict[ap] = {}
        apdistDict[ap]['proclist'] = []
        
        for proc in statsDict[ap]:
            p = statsDict[ap][proc]['proc']
            c = statsDict[ap][proc]['count']
            d = statsDict[ap][proc]['ip']
            apdistDict[ap]['proclist'].append((p,c))
            apdistDict[ap]['ap'] = ap
            apdistDict[ap]['ip'] = ip
        #print apdistDict[ap]['proclist']
        x = "".join(str(apdistDict[ap]['proclist'])).strip('[]')
        if x:
            xx = []
            xx.append(ap)
            xx.append(d)
            xx.append(x)
            newDict[ap] =  xx

    csv3 = rsm_summary_writer(newprocDict,dDict,newDict,timestamp)
    
#################################################################
    for f in datafilelist:
        ap = f.split('.')[-1]
        if ap =='py' or ap == 'swp':
            continue
        ap_mac = ap.replace('_',':').upper()
        if ap_mac in apmacDict.keys():
            ip = apmacDict[ap_mac]
            ap_name = apipDict[ip]
            ap_model = apmodelDict[ap_mac]
        else:
            ip = 'unknown'
            continue
        if ap not in apDict.keys():
            apDict[ap] = {}
        fp = open('writable/%s' % f, 'r')
        buff = fp.read()
        #print buff
        res1 = re.search(pattern1,buff,re.DOTALL)
        if res1:
            apDict[ap]['ap'] = ap 
            apDict[ap]['ip'] = ip 
            apDict[ap]['ap_name'] = ap_name
            apDict[ap]['model'] = ap_model
            apDict[ap]['uptime'] = res1.group(4).replace(',', ' ') 
            freemem = int(res1.group(2))
            usedmem = int(res1.group(1))
            cpuuse = int(res1.group(3))            
            apDict[ap]['FreeMem'] = freemem
            apDict[ap]['UsedMem'] = usedmem
            apDict[ap]['cpuUse'] = cpuuse
            
            if  cpuuse > 75:
                email_flag = 'yes'
                message_fp.write("CPU use  in ap %s  ( %s ) is %s%s .\n" % (ap_name,ip,cpuuse,'%'))
                heartbeat_ap_list.append(ap)
            x = (freemem + usedmem)
            memory_per = float(usedmem) /(freemem + usedmem) * 100
            new_mem = int(memory_per)
            apDict[ap]['per_memoryUsage'] = new_mem
            if memory_per > 75:
                #email_flag = 'yes'
                email_flag = 'no'
                heartbeat_ap_list.append(ap)
                message_fp.write("Used memory  in ap %s  ( %s ) is %s%s of total memory\n" % (ap_name,ip,new_mem,'%')) 
                message_fp.write("\n")

        ## new client count

        res21 = re.findall(pattern21,buff)
        res2 = re.findall(pattern2,buff)
        g_client_ct = 0
        a_client_ct = 0
        
        if res21:
                if len(res21) == 2:
                    g_count = int(res21[0][1])               
                    a_count = int(res21[1][1])
                elif len(res21) == 1:
                    if res21[0][0] == '0':
                        g_count = int(res21[0][1])
                        a_count = 0
                    else:
                        a_count = int(res21[0][1]) 
                        g_count = 0            
                #g_count = int(res21[0][1])
                #a_count = int(res21[1][1])
        if res2:
            g_list = res2[:g_count]
            a_list = res2[g_count:]
          
            for t in g_list:
             
                if int(t[1]) > 0:
                    #client = t[2]
                    g_client_ct += 1
                    
            for t in a_list:
                if int(t[1]) > 0:
                    #client = t[2]
                    a_client_ct += 1
            apDict[ap]['g_client_count'] = g_client_ct
            apDict[ap]['a_client_count'] = a_client_ct


        res10 = re.search(pattern10,buff)
        if res10:
            if ap not in apDict.keys():
                apDict[ap] = {}
                apDict[ap]['ap'] = ap
                apDict[ap]['ip'] = ip
                apDict[ap]['ap_name'] = ap_name
                apDict[ap]['model'] = ap_model
            apDict[ap]['beacon_stuck'] = 'yes' 
            email_flag = 'yes'
            message_fp.write("beacon stuck in ap %s  ( %s ).\n" % (ap_name,ip))
            heartbeat_ap_list.append(ap)

        res11 = re.search(pattern11,buff)
        if res11:
            
            ts = res11.group(1)
            wmi_count = res11.group(3)
            (y,m,d,t) = ts.replace('/',' ').split()
            month = months[int(m)-1]
            adate = " ".join([month,d,t])
            ts_new = utc_localtime_conversion(y,adate,todaydate)
            if ts_new:
                (m,d,t) = ts_new.split()
                slist = [int(x) for x in t.split(':')]
                tlist = [int(y), int(months.index(m))+1, int(d)]
                tlist.extend(slist)
                tlist.extend([1,1,1])
                time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                #print start_time, time_insec
                if (start_time - time_insec) < 2500:
                    email_flag = 'yes'
                    message_fp.write("wmi stuck in ap %s  ( %s ).\n" % (ap_name,ip)) 
                    heartbeat_ap_list.append(ap)
                if ap not in apDict.keys():
                    apDict[ap] = {}
                    apDict[ap]['ap'] = ap
                    apDict[ap]['ip'] = ip
                    apDict[ap]['ap_name'] = ap_name
                    apDict[ap]['model'] = ap_model
                apDict[ap]['wmi_stuck_count'] = wmi_count
                apDict[ap]['wmi_lasttime_reported'] = ts_new


        res12 =  re.findall(pattern12,buff)

        if res12:
            target_assert_time = []
            for ts in res12:
             
                (y,m,d,t) = ts.replace('/',' ').split()
                month = months[int(m)-1]
                adate = " ".join([month,d,t])
                ts_new = utc_localtime_conversion(y,adate,todaydate)
                if ts_new:
                    (m,d,t) = ts_new.split()
                    slist = [int(x) for x in t.split(':')]
                    tlist = [int(y), int(months.index(m))+1, int(d)]
                    tlist.extend(slist)
                    tlist.extend([1,1,1])
                    time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                    #print start_time, time_insec
                    target_assert_time.append(ts_new)
                    if (start_time - time_insec) < 2500:
                        email_flag = 'yes'
                        message_fp.write("target assert in ap %s  ( %s ).\n" % (ap_name,ip))
                        heartbeat_ap_list.append(ap)

                    if ap not in apDict.keys():
                        apDict[ap] = {}
                        apDict[ap]['ap'] = ap
                        apDict[ap]['ip'] = ip
                        apDict[ap]['ap_name'] = ap_name
                        apDict[ap]['model'] = ap_model
                    apDict[ap]['target_assert_times'] = target_assert_time             
                    apDict[ap]['target_assert_count'] = len(target_assert_time) 
   
        res14 =  re.findall(pattern14,buff)
        if res14:
            target_inactive_time = []
            for t in res14:
                ts = t[0] 
                interface = t[1]
                (y,m,d,t) = ts.replace('/',' ').split()
                month = months[int(m)-1]
                adate = " ".join([month,d,t])
                ts_new = utc_localtime_conversion(y,adate,todaydate)
                if ts_new:
                    (m,d,t) = ts_new.split()                
                    slist = [int(x) for x in t.split(':')]
                    tlist = [int(y), int(months.index(m))+1, int(d)]
                    tlist.extend(slist)
                    tlist.extend([1,1,1])
                    time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                    #print start_time, time_insec
                    if (start_time - time_insec) < 2500:
                        email_flag = 'yes'    
                        message_fp.write("target inactivity in ap %s  ( %s ).\n" % (ap_name,ip))
                        heartbeat_ap_list.append(ap)
                    
                    if ap not in apDict.keys():
                        apDict[ap] = {}
                        apDict[ap]['ap'] = ap
                        apDict[ap]['ip'] = ip
                        apDict[ap]['ap_name'] = ap_name
                        apDict[ap]['model'] = ap_model
                    target_inactive_time.append(ts_new)
                    apDict[ap]['target_inactive_times'] = target_inactive_time 
                    apDict[ap]['target_inactive_count'] = len(target_inactive_time)             
##Tx Descr stuck
        res24 =  re.findall(pattern24,buff)
        #print ap
        if res24:
            tx_desc_stuck_time = []
            for t in res24:
                ts = t[0] 
                interface = t[1]
                (y,m,d,t) = ts.replace('/',' ').split()
                month = months[int(m)-1]if res81:
            #print res81
            for item in res81:
                if int(item[1]) > 0:
                    proc = item[0] 
                    count = int(item[1])
                    if count == 1:
                        rsm_flag = 'yes'
                        rsmcrash_ap_list.append(ap)
                    if proc not in statsDict[ap].keys():
                        statsDict[ap][proc] = {} 
                    statsDict[ap][proc]['count'] = count
                    statsDict[ap][proc]['ap'] = ap_name
                    statsDict[ap][proc]['ip'] = ip
                    statsDict[ap][proc]['proc'] = proc 
        #print statsDict
        procDict = {}
        distDict = {}
        apdistDict = {}
        dDict = {}
        newDict = {}
        newprocDict = {}
    for ap in statsDict:
        
        for proc in statsDict[ap]:
            if proc not in procDict.keys():
                procDict[proc] = {}
                procDict[proc]['sum'] = 0if res81:
            #print res81
            for item in res81:
                if int(item[1]) > 0:
                    proc = item[0] 
                    count = int(item[1])
                    if count == 1:
                        rsm_flag = 'yes'
                        rsmcrash_ap_list.append(ap)
                    if proc not in statsDict[ap].keys():
                        statsDict[ap][proc] = {} 
                    statsDict[ap][proc]['count'] = count
                    statsDict[ap][proc]['ap'] = ap_name
                    statsDict[ap][proc]['ip'] = ip
                    statsDict[ap][proc]['proc'] = proc 
        #print statsDict
        procDict = {}
        distDict = {}
        apdistDict = {}
        dDict = {}
        newDict = {}
        newprocDict = {}
    for ap in statsDict:
        
        for proc in statsDict[ap]:
            if proc not in procDict.keys():
                procDict[proc] = {}
                procDict[proc]['sum'] = 0
                procDict[proc]['process'] = proc  
            procDict[proc]['sum'] += int(statsDict[ap][proc]['count'])
    for proc in procDict:
        newprocDict[proc] = procDict[proc]['sum']
   
    for ap in statsDict:
        for proc in statsDict[ap]:
            if proc not in distDict.keys():                
                distDict[proc] = {}
                distDict[proc]['aplist'] = []
            distDict[proc]['aplist'].append(ap)
    
    for proc in distDict.keys():
        x = "".join(str(distDict[proc]['aplist'])).strip('[]')
        dDict[proc] = x
        
    for ap in statsDict:
        apdistDict[ap] = {}
        apdistDict[ap]['proclist'] = []
        
        for proc in statsDict[ap]:
            p = statsDict[ap][proc]['proc']
            c = statsDict[ap][proc]['count']
            d = statsDict[ap][proc]['ip']
            apdistDict[ap]['proclist'].append((p,c))
            apdistDict[ap]['ap'] = ap
            apdistDict[ap]['ip'] = ip
        #print apdistDict[ap]['proclist']
        x = "".join(str(apdistDict[ap]['proclist'])).strip('[]')
        if x:
            xx = []
            xx.append(ap)
                procDict[proc]['process'] = proc  
            procDict[proc]['sum'] += int(statsDict[ap][proc]['count'])
    for proc in procDict:
        newprocDict[proc] = procDict[proc]['sum']
   
    for ap in statsDict:
        for proc in statsDict[ap]:
            if proc not in distDict.keys():                
                distDict[proc] = {}
                distDict[proc]['aplist'] = []
            distDict[proc]['aplist'].append(ap)
    
    for proc in distDict.keys():
        x = "".join(str(distDict[proc]['aplist'])).strip('[]')
        dDict[proc] = x
        
    for ap in statsDict:
        apdistDict[ap] = {}
        apdistDict[ap]['proclist'] = []
        
        for proc in statsDict[ap]:
            p = statsDict[ap][proc]['proc']
            c = statsDict[ap][proc]['count']
            d = statsDict[ap][proc]['ip']
            apdistDict[ap]['proclist'].append((p,c))
            apdistDict[ap]['ap'] = ap
            apdistDict[ap]['ip'] = ip
        #print apdistDict[ap]['proclist']
        x = "".join(str(apdistDict[ap]['proclist'])).strip('[]')
        if x:
            xx = []
            xx.append(ap)
                adate = " ".join([month,d,t])
                ts_new = utc_localtime_conversion(y,adate,todaydate)
                if ts_new:
                    (m,d,t) = ts_new.split()
                    slist = [int(x) for x in t.split(':')]
                    tlist = [int(y), int(months.index(m))+1, int(d)]
                    tlist.extend(slist)
                    tlist.extend([1,1,1])
                    time_insec = int(time.mktime(tuple(tlist)))+3600 ## when time zone is PST, need to add 3600
                    #print start_time, time_insec
                    if (start_time - time_insec) < 2500:
                        email_flag = 'yes'
                        message_fp.write("TX descriptor stuck in ap %s  ( %s ) interface %s.\n" % (ap_name,ip,interface))
                        heartbeat_ap_list.append(ap)

                    if ap not in apDict.keys():
                        apDict[ap] = {}
                        apDict[ap]['ap'] = ap
                        apDict[ap]['ip'] = ip
                        apDict[ap]['ap_name'] = ap_name
                        apDict[ap]['model'] = ap_model
                    tx_desc_stuck_time.append(ts_new)
                    apDict[ap]['tx_desc_stuck_times'] = tx_desc_stuck_time
                    apDict[ap]['tx_desc_stuck_count'] = len(tx_desc_stuck_time)
            
    
        if re.search('Busy',buff):     
            res13 =  re.findall(pattern13,buff)
        
            if res13: 
                if ap not in apDict.keys():
                    apDict[ap] = {}
                    apDict[ap]['ap'] = ap
                    apDict[ap]['ip'] = ip
                    apDict[ap]['ap_name'] = ap_name
                    apDict[ap]['model'] = ap_model
                
                apDict[ap]['2g_ch_util_Busy'] = int(res13[0][0])
                apDict[ap]['2g_ch_util_RX'] = int(res13[0][1])
                apDict[ap]['2g_ch_util_TX'] = int(res13[0][2])
                apDict[ap]['2g_ch_util_Total'] = int(res13[0][3])
                if len(res13) > 1:
                    apDict[ap]['5g_ch_util_Busy'] = int(res13[1][0])
                    apDict[ap]['5g_ch_util_RX'] = int(res13[1][1])
                    apDict[ap]['5g_ch_util_TX'] = int(res13[1][2])
                    apDict[ap]['5g_ch_util_Total'] = int(res13[1][3])

    ap_clientDict = {}    ### This is for saving client details for each AP
    
    statslogDict = {}
    
    for f in logfilelist:
        
        ap = f.split('.')[-1]
        ap_mac = ap.replace('_',':').upper()
        if ap_mac in apmacDict.keys():
            ip = apmacDict[ap_mac]
            ap_name = apipDict[ip]
        else:
            ip = 'unknown'        

        ap_clientDict[ap] = {}
        #ap_walDict[ap] = {}
        fp = open('writable/%s' % f,'r')
        buff = fp.read()
        res6 = re.findall(pattern6,buff)
        res7 = re.findall(pattern7,buff)

        if res7:
            for t in res7:
                ts_utc = t[0]
                ts = utc_localtime_conversion(year,ts_utc,todaydate)
                if ts:              
                    wlan = t[1]
                    station = t[2]
                    if station:
                        if station not in ap_clientDict.keys():
                            ap_clientDict[station] = {}
                        if ts not in ap_clientDict[station].keys():
                            ap_clientDict[station][ts] = {}    
                        #ap_clientDict[station][ts] = {}
                        ap_clientDict[station][ts]['ap'] = ap
                        ap_clientDict[station][ts]['ip'] = ip
                        ap_clientDict[station][ts]['ts'] = ts
                        ap_clientDict[station][ts]['action'] = 'Authentication Difficulty'
                        ap_clientDict[station][ts]['station'] = station
                        ap_clientDict[station][ts]['auth_difficult_wlan'] = wlan 


        if res6:
                print "\nParsing disassoc details "

                for t in res6:
                    ts_utc = t[0]
                    ts = utc_localtime_conversion(year,ts_utc,todaydate)
                    if ts:  
                        station = t[2]
                        if not station:
                            continue
                        if station not in ap_clientDict.keys():
                            ap_clientDict[station] = {}
                        if ts not in ap_clientDict[station].keys():
                            ap_clientDict[station][ts] = {}                            
                        #ap_clientDict[ap][ts] = {}
                        ap_clientDict[station][ts]['ap'] = ap 
                        ap_clientDict[station][ts]['ip'] = ip 
                        ap_clientDict[station][ts]['ts'] = ts 
                        ap_clientDict[station][ts]['ap_name'] = ap_name
                        ap_clientDict[station][ts]['action'] = 'disassoc'
                        ap_clientDict[station][ts]['station'] = t[2] 
                        ap_clientDict[station][ts]['hint'] = t[1] 
                        ap_clientDict[station][ts]['rx_rssi'] = t[3] 
                        ap_clientDict[station][ts]['ack_rssi'] = t[4] 
                        ap_clientDict[station][ts]['reason'] = t[5] 
                        ap_clientDict[station][ts]['freq'] = t[6] 
                        ap_clientDict[station][ts]['chan'] = t[7] 
                        ap_clientDict[station][ts]['stats'] = t[8] 
                        if ap not in statslogDict.keys():
                            statslogDict[ap] = {}
                        statslogDict[ap][ts] = {}    
                        statslogDict[ap][ts]['hint'] = t[2]
                        statslogDict[ap][ts]['ap'] = ap
                        statslogDict[ap][ts]['ap_name'] = ap_name
                        statslogDict[ap][ts]['ts'] = ts  
                                                

    ap_clientDict = {}        
    (apDict,email_flag,heartbeat_ap_list) = ap_reboot_dict(timestamp,email_flag,apDict,ap_clientDict,apmacDict,apipDict,apmodelDict,message_fp,heartbeat_ap_list) 
     
    #os.system('rm writable/datafile*')
    #os.system('rm -r writable')

    (csv1,csv2) = csvfile_writer(apDict,ap_clientDict,timestamp) 
    #csv3 = statscsv_writer(statsDict,timestamp)
    #csv4 = statslogcsv_writer(statslogDict,timestamp)
    #get_client_count(csv1,timestamp)
    return(csv1,csv2,csv3,email_flag,heartbeat_ap_list,rsmcrash_ap_list)
    #return(csv1,csv2,email_flag,heartbeat_ap_list)
             
if  __name__ =='__main__':
    '''get_todaydate_scglog()
    timestamp = int(time.time())
    email_flag = 'no'
    ap = '84_18_3A_00_4E_10'
    apDict = {}
    apDict[ap] = {}
    apDict[ap]['ap'] = ap
    apDict[ap]['ip'] = '10.10.10.10' 
    apDict[ap]['ap_name'] = 'ap_name'
    message_fp = open('test.txt','w')
    heartbeat_ap_list = []
    ap_reboot_dict(timestamp,email'''
    timestamp = int(time.time())
    email_flag = 'no'
    file_parser(timestamp,email_flag)
