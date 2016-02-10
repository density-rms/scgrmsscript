#!/usr/bin/python
import time
import re, csv
import os, sys
import rsm_parserscript
import scgCLI
from datetime import datetime
from threading import Timer
import subprocess

months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
#working_dir = "/home/wspbackup/newdir/latestscript"
#report_dir = "/var/www/densitystatus/dailystatus"

def scg_aps(zdip, zduser, zdpass):
    scg = zdcli.ZDCLI(zdip)
    scg.connect(zduser, zdpass, timeout=3600,sesame_key="!v54!")
    scg.to_shell()
    iplist = scg.get_aplist()
    scg.close()
    return iplist

def scg_macs(zdip, zduser, zdpass):
    scg = zdcli.ZDCLI(zdip)
    scg.connect(zduser, zdpass, timeout=3600,sesame_key="!v54!")
    scg.to_shell()
    maclist = scg.get_apmaclist()
    scg.close()
    return maclist

apDict = {}
iplist = []

def create_apDict(maclist):
    for m in maclist:
        apDict[m[0].upper()] = m[1]
        iplist.append(m[1]) 
    return (apDict, iplist)

def macs(s):
    return "".join([i for i in s if i != ":" and i !="-"])

def newping(target_ip):
    pingable = 0
    buff = os.popen(r'ping %s -c 4' % target_ip.rstrip()).read()
    #print buff
    res = re.search('.*?transmitted,\s+(\d+)\s+received,',buff)
    if res:
        if int(res.group(1)) >1:
            pingable = 1
    return pingable

def client_process_logs(ts):
        flist = []
        os.system('mkdir clientstats-%s' % ts)
        savedir = 'clientstats-%s' % ts
        #tftp_dir = '/opt/tftpboot/'
        current_dir = os.getcwd()
        s_files = tftp_dir+"clientdata*.tgz"
        d_files = current_dir+"/."
        cmd = 'cp %s %s' % (s_files, d_files)
        ok = os.system(cmd)
        f = "clientdataall.tgz"
        os.system('tar -xzvf %s' % f)

        os.system('mv  clientdata*.tgz %s/.' % savedir)
        os.system('mv  %s /var/www/densitystatus/clientcapability/.' % savedir)



def process_logs(ts,clientstats_dir):
        print clientstats_dir
        flist = []
        os.system('mkdir stats-%s' % ts)
        savedir = 'stats-%s' % ts
        current_dir = os.getcwd()
        print current_dir
        ok = 0
        if ok == 0:
            filelist = os.listdir('.')
            for f in filelist:
                if f.startswith('datafile'):
                    flist.append(f)
            for f in filelist:
                if f.startswith('logread'):
                    flist.append(f)
            for f in filelist:
                if f.startswith('athstats'):
                    flist.append(f)  
            #for f in filelist:
                #if f.startswith('stats80211all'):
                    #flist.append(f)             
            for f in filelist:
                if f.startswith('eventall'):
                    flist.append(f)  
            for f in filelist:
                if f.startswith('rsmfileall'):
                    flist.append(f)                
            if flist:
                for f in flist:
                    os.system('tar -xzvf %s' % f)   
        ok = 1           
        os.system('rm -r writable')
        os.system('mv tmp writable')
        os.system('mv  datafileall* %s/.' % savedir)
        os.system('mv  rsmfileall* %s/.' % savedir)
        os.system('mv  logreadall* %s/.' % savedir)
        os.system('mv  athstatswifi0all* %s/.' % savedir)
        os.system('mv  athstatswifi1all* %s/.' % savedir)
        os.system('mv  eventall*  %s/.' % savedir)
        #os.system('mv  stats80211all.tgz %s/.' % savedir)
        os.system('mv  %s %s/.' % (savedir, clientstats_dir))     

def get_ap_support(aplist,scgip):
    scg = scgCLI.SCGCLI(scgip,scguser,scgpass,enablepass)
    scg.connect(scguser, scgpass,enablepass, timeout=3600,sesame_key="!v54!")
    #scg.to_shell()
    logs_ok = scg.get_supportfile(aplist)
    scg.close()     
def get_rsm_data(ap,crashlist,scgip):
    scg = scgCLI.SCGCLI(scgip,scguser,scgpass,enablepass)
    scg.connect(scguser, scgpass,enablepass, timeout=3600,sesame_key="!v54!")
    #scg.to_shell()
    logs_ok = scg.get_crashfile(ap,crashlist)
    scg.close()     
    
   
def get_scg_details(working_dir):
    iniDict = {}
    with open('%s/initialize_file' % working_dir,'r') as ini_fp:
        for line in ini_fp:
            ini_list = line.split()
            iniDict["%s" % ini_list[0]] = ini_list[1].rstrip()
    return iniDict
def gen_crash(count):
    count += 1
    yield count


if __name__ =='__main__': 
    current_dir = os.getcwd()  
    scgDict = get_scg_details(current_dir)
    if scgDict:
        
        scgip1 = scgDict['scg_ip1']
        scgip2 = scgDict['scg_ip2']
        scguser = scgDict['scguser']
        scgpass = scgDict['scgpass']
        enablepass = scgDict['scg_enablepass']
        #frequency = scgDict['monitor_interval']
        frequency = 10
        scp_addr = scgDict['scp_addr']
        scp_dir = scgDict['scp_dir']
        working_dir = scgDict['working_dir']
        report_dir  = scgDict['report_dir']
        apstats_dir = scgDict['apstats_dir']
        clientstats_dir = scgDict['clientstats_dir']
        html_dir =scgDict['html_dir']
        http_addr = scgDict['http_addr']
    else:
        print "Not able to get SCG details, make sure to update details in  initilize_file, exiting"
        sys.exit(1)
    count = 0 
    rsmcrash = gen_crash(count)
    while True:
        ## The following gets the list of APs under each SZ node
        '''scg = scgCLI.SCGCLI(scgip1,scguser,scgpass,enablepass)
        scg.connect(scguser, scgpass,enablepass, timeout=3600,sesame_key="!v54!")
        scg.get_scg_ap_details()
        scg.get_scg_ap_list()
        scg.close()
        sz2_list = []
        fp = open('%s/sz2' % current_dir, 'r')
        for line in fp:
            sz2_list.append(line.rstrip())
        fp.close()
        x = ';'.join(sz2_list)
        print x
        sz1_ap = "sz1"  
        ## The following collects the stats from both szs   '''
        #########

        timestamp = int(time.time())
        #timestamp = int(1437891033)
        print timestamp
        print "\nCollecting AP logs from sz1 starts:\n"
        '''scg = scgCLI.SCGCLI(scgip1,scguser,scgpass,enablepass)
        scg.connect(scguser, scgpass,enablepass, timeout=600,sesame_key="!v54!")
        #scg.to_shell()
        logs_ok = scg.get_sz1_allmonitor(sz1_ap)
        scg.close()
        
        print "\nCollecting AP logs from sz2 starts:\n"
        scg = scgCLI.SCGCLI(scgip2,scguser,scgpass,enablepass)
        scg.connect(scguser, scgpass,enablepass, timeout=600,sesame_key="!v54!")
        #scg.to_shell()
        logs_ok = scg.get_sz2_allmonitor(x)
        scg.close() 
     
        #### the following process the AP logs collected
        print "All collected files are being processed........"   
        process_logs(timestamp,clientstats_dir)  
        
        #client_process_logs(timestamp, tftp_dir)      
        print "Parsing is taking place .... it takes more than 30 sec for each AP"   '''
        
        email_flag = 'no'  
        (csv1,csv2, csv3, email_flag,heartbeat_ap_list,rsmcrash_ap_list) = rsm_parserscript.file_parser(timestamp, email_flag) 
        #(csv1,csv2,csv4, email_flag,heartbeat_ap_list) = parserscript_tx_desc_06_24.file_parser(timestamp, email_flag) 
        #csv3 = client_capability.client_file_parser(apDict,timestamp) 
        #(csv1,csv2, email_flag,heartbeat_ap_list) = parserscript_tx_desc_upgrade_count.file_parser(timestamp, email_flag)
                
        '''ap_sz1_list,ap_sz2_list = [], []
        print "email_flag", email_flag     
        if email_flag == 'yes' and heartbeat_ap_list:process crash in
            for ap in heartbeat_ap_list:
                if ap in sz2_list:
                    ap_sz2_list.append(ap)
                else:
                    ap_sz1_list.append(ap)
            if  ap_sz1_list:
                print "get the sz1 ap support file"
                get_ap_support(ap_sz1_list,scgip1)
            if ap_sz2_list:
                print "get the sz2 ap support file"
                get_ap_support(ap_sz2_list,scgip2) '''
        if  rsmcrash_ap_list:
            for s in rsmcrash_ap_list:
                ap = s[0]
                crashlist = s[1]
                if ap in sz2_list:
                    get_rsm_data(ap,crashlist,scgip2) 
                elif ap in sz1_list:

                    get_rsm_data(ap,crashlist,scgip1)                     
            print rsmcrash.next()
            '''for ap in rsmcrash_ap_list:
                if ap in sz2_list:
                    rsm_sz2_list.append(ap)
                else:
                    rsm_sz1_list.append(ap)
            if  rsm_sz1_list:
                print "get the sz1 ap support file"
                get_rsm_data(rsm_sz1_list,scgip1)
            if rsm_sz2_list:
                print "get the sz2 ap support file"
                get_rsm_data(rsm_sz2_list,scgip2)        
            
            current_dir = os.getcwd()
            if len(heartbeat_ap_list) > 1 :
                os.system('tar -czvf supportall.tgz support*.txt')
                time.sleep(5)
                filename = "supportall.tgz"
            else:
                filename = "support%s.txt" % heartbeat_ap_list[0]
            subprocess.call(['%s/monitor_email.sh' % current_dir, "%s" % csv1, "%s" % filename])
            cmd = "rm -f support*"
            os.system(cmd)
        elif email_flag == 'yes':
        
            subprocess.call(['%s/monitor_email.sh' % current_dir, "%s" % csv1])          
        cmd1 = 'mv %s/%s %s/%s' % (current_dir, csv1,apstats_dir,csv1)
        cmd2 = 'mv %s/%s %s/%s' % (current_dir,csv2,clientstats_dir,csv2)
        cmd3 = 'mv %s/%s %s/%s' % (current_dir,csv3,report_dir,csv3)
        #cmd4 = 'mv %s/%s %s/%s' % (current_dir,csv4,stats80211_dir,csv4)  

        os.system(cmd1)
        os.system(cmd2)  
        os.system(cmd3) 
        #os.system(cmd4)   

        print " Waiting for %s sec to start the next Monitoring ..." % frequency   '''
        time.sleep(int(frequency))   
        
