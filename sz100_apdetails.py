#!/usr/bin/python
import json,urllib
import sys,os,io
import re,ast,csv
import time
import scgwebaccess2

def apPing(ip):
    buff = os.popen(r'ping %s -c 4' % ip).read()
    #print buff
    res = re.search('.*?transmitted,\s+(\d+)\s+received,', buff)
    if res:
        if int(res.group(1)) > 1:
            print "AP pinging"
            return "pinging"
    else:
        print "ping to AP failed"
        return "failed"

def main():
    #### This includes the parallel processing for getting CM serial which otherwise takes too long
    #### Also ping the AP before trying to apply the rclient command to avoid getting stuck 

    ## creating a temp directory to save all temp files
    try:
        macfp = open("/tmp/apmaclist", "wb")
    except IOError:
        print "could not create maclist file, exiting\n"
        sys.exit(0) 

    current_ts = int(time.time())
    scg = scgwebaccess2.scgAccess('admin')
    scg_ip = scg.getScgManagementIp()
    scg_passwd = scg.getScgPassphrase()
    scg.scgLogin()
    #(ftp_ip,ftp_user,ftp_passwd,ftp_port) = scg.getScgFtpDetails()
    #(staging_zone_uuid,zoneDict) = scg.createScgZoneDict()

    #cur_ts = time.strftime("%Y-%m-%d-%H-%M",time.localtime(float(current_ts)))
    csvfilename = "apdetails.csv"
    try:
        csvptr = open("/tmp/apdetails.csv","wb")
    except IOError:
        print "Cannot open csv file, exiting\n"
        sys.exit(0)

    #fieldnames = ['apMac','apSerialNo','apIP','apName','description','model','location','zoneName','fwVersion','clientCount','gpsInfo','cableMOdInfo','channel','vlan','domainName','uptime','tunnelEnabled','meshRole','connectionStatus','registrationTime']
    fieldnames = ['apmac','apip','apname','model','location','fwVersion','clientCount','meshRole']

    csvptr.write(','.join(fieldnames)+'\r\n')
    dwriter= csv.DictWriter(csvptr,fieldnames, dialect = 'excel', delimiter=',', extrasaction='ignore')
    apDict = {}
    masterDict = {}
    zoneName = 'test'
    masterDict[zoneName] = {} 
    try:
            cmd = "curl -s -b /tmp/headers.txt -k \'https://%s:8443/wsg/api/scg/apsE/byZone/f77a8816-3049-40cd-8484-82919275ddc3\'" % (scg_ip)
            sub_buff = os.popen(cmd)
            buff = sub_buff.read()
            print "grabbing APs in the zone"
            sub_buff.close()
    except TimeoutException:
            print "not able to get zone ap list"
            continue
    try:
            data_j = json.loads(buff)['data']
            ap_count =  int(data_j['totalCount'])
            print '# of APs: %s' % ap_count
            if ap_count > 0:
		
                for i in range(ap_count):
		    if data_j['list'][i]['connectionStatus'] == "Connect":
                        apmac = data_j['list'][i]['apMac']
                        masterDict[zoneName][apmac] = {}
                        masterDict[zoneName][apmac]["apmac"] = data_j['list'][i]['apMac']
                        macfp.write("%s\n" % apmac)
    
                        if 'ip' in data_j['list'][i]:
                            ip = data_j['list'][i]['ip']
                            masterDict[zoneName][apmac]["apip"] =  ip.encode('utf-8')
                        else:
                            masterDict[zoneName][apmac]["apip"] = ''

                        if 'deviceName' in data_j['list'][i]:
                            deviceName = data_j['list'][i]['deviceName']
			    try:
			        masterDict[zoneName][apmac]["apname"] =  deviceName.encode('utf-8')
                            except:
                                if UnicodeEncodeError:
                                      #print " not encoding"
                                    masterDict[zoneName][apmac]["apname"] = ''
                        else:
                            masterDict[zoneName][apmac]["apname"] = ''

                    
                        if 'model' in data_j['list'][i]:
                            model = data_j['list'][i]['model']
                            masterDict[zoneName][apmac]["model"] =  model.encode('utf-8')
		        else:
			    nmasterDict[zoneName][apmac]["model"] = ''

                    
		        if 'clientCount' in data_j['list'][i]:
                            masterDict[zoneName][apmac]["clientCount"] =  data_j['list'][i]['clientCount']
			else:
                            masterDict[zoneName][apmac]["clientCount"] = ''

                    
                        if 'meshRole' in data_j['list'][i]:
                            meshRole = data_j['list'][i]['meshRole'] 
                            try:
                                masterDict[zoneName][apmac]["meshRole"] =  meshRole.encode('utf-8')
                            except:
                                if UnicodeEncodeError:
                                #print " not encoding"
                                    masterDict[zoneName][apmac]["meshRole"] = ''
                        else:
                            masterDict[zoneName][apmac]["meshRole"] = ''

                    
    except:      
            pass  
    macfp.close()

    #### The following gets the list of all aps in all zones from the apDict

    
 
    for zone in masterDict.keys():
        for ap in masterDict[zone].keys():
            dwriter.writerow(masterDict[zone][ap])   
    csvptr.close()
    cmd = "scp /home/admin/tempdir/%s wspbackup@10.150.13.7:/home/wspbackup/scg_rsm/%s" % (csvfilename,csvfilename)     
    print cmd
    os.system(cmd)
    scg.scgLogout()


if __name__ == '__main__':
    main()
       

