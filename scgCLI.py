#!/usr/bin/python
import pexpect
import sys
import re
import os
import time
import string
import csv
import json
import cStringIO
import scgwebaccess2
import pdb

zonelist = []

class SCGCLI:

    def __init__(self,scg_ip,scg_user,scg_passwd,enable_passwd,verbose=False):
        #scg_PROMPT = [">","#","--More--",'.*debug)#','.*diagnostic)#']
        scg_PROMPT = [">","#"]
        #scg_PROMPT = ">"
        self.ip = scg_ip
        self.user = scg_user
        self.passwd = scg_passwd
        self.enable_passwd = enable_passwd
        self.prompt = scg_PROMPT
        self.VERBOSE = verbose
    def setvars(self, s, user, passwd, enable_passwd, timeout=120):
        self.user = user
        self.passwd = passwd
        self.enable_passwd = enable_passwd
        self.s = s
        self.s.maxread = 8000
        self.s.timeout = timeout

        
    def connect(self, user, passwd,enable_passwd, timeout=60,sesame_key=None):
        
        self.sesame_key = sesame_key
        #print self.enable_passwd
        ssh_newkey = 'Are you sure you want to continue connecting'    
        #print "Connecting to %s" % self.ip
        s = pexpect.spawn( 'ssh %s@%s' % (self.user,self.ip), searchwindowsize = 128 )
        i = s.expect([pexpect.TIMEOUT, ssh_newkey, '.*password: '])
        print i
        if i == 1:
            s.sendline( 'yes' )

        s.sendline(passwd)  # run a command
        s.expect(self.prompt[0])  # match the prompt
        #self.prompt = "#"
        s.sendline('enable')
        s.expect('.*assword: ')       
        s.sendline(self.enable_passwd)  # run a command  
        s.expect(self.prompt[1])  # match the prompt
        self.setvars(s, user, passwd, enable_passwd, timeout) 

    def cmd(self, cmd, prompt=None, timeout=100, comment=None):
        print cmd
        if self.VERBOSE:
            output = cmd
            if comment != None:
                output = comment
            if len(output):
                print "scg %s# %s" % (self.ip, output)
        #self.prompt = '#'
        self.s.sendline(cmd)
        #if not prompt:
            #prompt = self.prompt[1]
        #i = self.s.expect(prompt, timeout = timeout)
        #i = self.s.expect(self.scg_PROMPT, timeout = timeout)
        i = self.s.expect(self.prompt, timeout = timeout)
        rx = ""
        while i == 2:
            rx += self.s.before
            self.s.sendline("\\f")
            #i = self.s.expect(self.scg_PROMPT, timeout = timeout)
            i = self.s.expect(self.prompt, timeout = timeout)
        rx += self.s.before
        if rx:
            #print rx
            #rx = rx.replace(cmd, '')
            rx = rx.strip()
            pass
        return cStringIO.StringIO(rx).readlines()

    def close(self):
        self.s.close()

    def get_scg_ap_details(self, timeout=120):
        self.s.sendline('debug')
        i = self.s.expect(self.prompt,timeout=timeout)
        self.s.sendline('diagnostic')
        self.s.expect(self.prompt,timeout=timeout)
        self.s.sendline('execute sz100_apdetails')
        self.s.expect(self.prompt, timeout=timeout)
        return ('ok') 
    def get_scg_version(self, timeout=120):
        self.s.sendline('show version')
        self.s.expect(self.prompt)   
        rx = self.s.before
        print rx
        if rx:
            pattern = 'SZ Version.*?(\d.*?)\n'
            res = re.search(pattern,rx)
            if res:
                version = res.group(1)
                return version
            else:
                print "Could not get SZ version"
                return
    def get_scg_ap_list(self, timeout=120):
        self.s.sendline('debug')
        i = self.s.expect(self.prompt,timeout=timeout)
        self.s.sendline('diagnostic')
        self.s.expect(self.prompt,timeout=timeout)
        self.s.sendline('execute getszaplist')
        self.s.expect(self.prompt, timeout=timeout)
        return ('ok')


    def get_supportfile(self,aplist, timeout=120):
        self.s.sendline('debug')
        self.s.expect(self.prompt)
        self.s.sendline('diagnostic')
        self.s.expect(self.prompt)
        for ap in aplist:
            ap = ap.replace('_',':')
            cmd = 'execute getsupport %s' % (ap)
            self.s.sendline(cmd)
            self.s.expect(self.prompt,timeout=timeout)
        return ('ok')
        
    def get_rsmdata(self,ap,crashlist, timeout=120):
        self.s.sendline('debug')
        self.s.expect(self.prompt)
        self.s.sendline('diagnostic')
        self.s.expect(self.prompt)
        ap = ap.replace('_',':')
        for c in crashlist:
            cmd = 'execute getcrashdata %s %s' % (ap,c)
            self.s.sendline(cmd)
            self.s.expect(self.prompt,timeout=timeout)
        return ('ok')        
    def get_sz1_allmonitor(self,apfile):
        self.s.sendline('debug')
        i = self.s.expect(self.prompt)
        self.s.sendline('diagnostic')
        i = self.s.expect(self.prompt)
        cmd = 'execute sz1allmonitor %s' % (apfile)
        print cmd
        #self.s.sendline('execute scgallmonitor')
        self.s.sendline(cmd)
        i = self.s.expect(self.prompt)
        x = self.s.before
        print x
        return ('ok')
    
    def get_sz2_allmonitor(self,apfile, timeout=120):
        print apfile
        self.s.sendline('debug')
        i = self.s.expect(self.prompt, timeout=timeout)
        x = self.s.before
        print x
        self.s.sendline('diagnostic')
        i = self.s.expect(self.prompt, timeout=timeout)
        cmd = 'execute sz2allmonitor %s' % (apfile)
        print cmd
        #self.s.sendline('execute scgallmonitor')
        self.s.sendline(cmd)
        i = self.s.expect(self.prompt)
        x = self.s.before
        print x
        return ('ok')

if __name__ == "__main__":
            
            #user = 'admin'
            #scg = scgwebaccess2.scgAccess('admin')
            #scg_ip = scg.getScgManagementIp()
            #scg_passwd = scg.getScgPassphrase()
            scg_ip = '10.150.0.25'
            user = 'admin'
            scg_passwd = 'rucku$987'
            enable_passwd = 'rucku$987'
            scg = SCGCLI(scg_ip, user,scg_passwd,enable_passwd)    
            scg.connect(user, scg_passwd,enable_passwd)
            #res = scg.cmd("show running-config zone  ")
            #print res
            res = scg.get_scg_ap_details()
            print res
            scg.close()
