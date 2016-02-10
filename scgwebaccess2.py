
#!/usr/bin/python
import json,urllib
import sys,os,io
import re,ast,csv

class scgAccess(object):
    def __init__(self,scg_user):
        """ Constructor"""
        self.scg_user = scg_user

    def getScgManagementIp(self):
        self.scg_ip = None
        buff = os.popen("curl -s http://localhost:8085/wsg/api/native-rest/cf/controlBlade").read()
        data_j = json.loads(buff)
        if data_j["data"]:
            dataList = data_j["data"]          
            
            for d in dataList:
                try:
                    if d["bindingInterfaces"]:
                        management_interface = (d["bindingInterfaces"])["Management"]
                    if d["bindingIps"]:
                        self.scg_ip =(d["bindingIps"])[management_interface]
                        #After we get first one ip, then can exit for loop
                        break
                except:
                    print " Not able to get scg mgmt interface and IP addr, exiting"
                    sys.exit(0)
        else:
            print " Not able to get scg mgmt interface and IP addr, exiting"
            sys.exit(0)
        return self.scg_ip

    def getScgPassphrase(self):
        ## The following gets the user password
        self.scg_passwd = None
        buff = os.popen("curl -s http://localhost:8085/wsg/api/native-rest/passphrase/92cc1b65-c3cd-4f26-8c9b-3e7b055c7c25/").read()
        data_j = json.loads(buff)
        if data_j["data"]:
            try:
                self.scg_passwd = data_j["data"]['passphrase']
            except:
                print "Failed to get the passphrase, exiting"
                sys.exit(0)
        else:
            print "Failed to get the passphrase, exiting"
            sys.exit(0)
        return self.scg_passwd

    def scgLogin(self):
        #print "scg_passwd", self.scg_passwd
        t_string = "-d \'{\"userName\":\"%s\", \"password\":\"%s\"}\' \'https://%s:8443/wsg/api/scg/session/login\'" % (self.scg_user,self.scg_passwd,self.scg_ip)
        command = "curl -s  --cookie-jar /tmp/headers.txt -k -X PUT -H \"TimezoneOffset:-180\" -H \"GMTOffset:+0300\" -H \"Accept: application/json\" -H \"Content-type: application/json\" %s"  % t_string
        buff = os.popen(command).read()
        data_j = json.loads(buff)
        if "success" in data_j.keys():
            if data_j["success"] == True:
                #print  "login is successful"
                pass
            else:
                print " login failed, exiting"
                sys.exit(0)



    def scgLogout(self):
        try:
            buff = os.popen("curl -s -b /tmp/headers.txt -k -X PUT \'https://%s:8443/wsg/api/scg/session/currentUser/logout\'" % self.scg_ip).read()

        except:
            print "scg logout failed, exiting"
            sys.exit(0)

        data_j = json.loads(buff)
        if data_j["success"]:
            if data_j["success"] == True:
                print  "logout is successful"
            else:
                print " logout failed, exiting"
                sys.exit(0)
        else:
            print " logout failed, exiting"
            sys.exit(0)
        return

    def getScgFtpDetails(self):
        buff = os.popen("curl -s http://localhost:8085/wsg/api/native-rest/cf/system/systemSettings").read()
        data_j = json.loads(buff)
        if data_j["data"]:
            ftpDict = data_j["data"]
            self.ftp_ip = ''
            self.ftp_port = ''
            self.ftp_user = ''
            self.ftp_passwd = ''

            for key in ftpDict.keys():
                if key == 'ftpPwd':
                    self.ftp_passwd = ftpDict[key]
                elif key == 'ftpUser':
                    self.ftp_user = ftpDict[key]
                elif key == 'ftpPort':
                    self.ftp_port = ftpDict[key]
                elif key == 'ftpHost':
                    self.ftp_ip = ftpDict[key]

            if self.ftp_ip == '' or self.ftp_passwd == '' or self.ftp_user == '':
                print "ftp serverinformation is not complete, please check ftp server configuration on scg"
                return('','','','')
        else:
            print "ftp serverinformation is not complete, please check ftp server configuration on scg, exiting"
            return('','','','')
        return (self.ftp_ip,self.ftp_user,self.ftp_passwd,self.ftp_port)

    def createScgZoneDict(self):
        buff = os.popen("curl -s http://localhost:8085/wsg/api/native-rest/cf/domain").read()
        data_j = json.loads(buff)
        if not data_j["data"]:
            print "No domains in the network"
            sys.exit(0)
        else:
            for domain in data_j["data"]:
                if domain['domainName'] == 'Administration Domain':
                    adm_domain_uuid = domain['key']
                    break

        criteria = '[{"displayName":"Management Domain","columnName":"domainName","value":"Administration Domain","operator":"eq","displayValue":"Administration Domain"}]'
        cmd = "curl -s -b /tmp/headers.txt -k \'https://%s:8443/wsg/api/scg/zones/byDomain/%s?criteria=%s\'" % (self.scg_ip,adm_domain_uuid,urllib.quote_plus(criteria))
        buff = os.popen(cmd).read()
        data_j = json.loads(buff)
        self.staging_zone_uuid = ''
        if data_j["data"]:
            zoneList = data_j["data"]["list"]
            zoneDict = {}
            for zone in zoneList:
                if zone["mobilityZoneName"] and zone["key"]:
                    zone_name = zone['mobilityZoneName']
                    zone_key = zone['key']
                    zoneDict[zone_name] = zone_key
                    ## find the staging zone key
                    if zone['mobilityZoneName'] == "Staging Zone":
                        self.staging_zone_uuid = zone['key']
                else:
                    continue
        else:
            print "no zones configured in scg, exiting"
            sys.exit(0)
        self.zoneDict = zoneDict
        return (self.staging_zone_uuid, self.zoneDict)

if __name__ == "__main__":

    mywsg =scgAccess('admin')
    scg_ip = mywsg.getScgManagementIp()
    scg_passwd = mywsg.getScgPassphrase()
    #mywsg.scgLogin()
    #mywsg.getScgFtpDetails()
    #(staging_zone_uuid,zoneDict) = mywsg.createScgZoneDict()
    #print staging_zone_uuid,zoneDict
    mywsg.scgLogout()

