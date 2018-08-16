# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 21:40:47 2018

@author: Jon Chin & Gregg Daugherty (WB6YAZ)
"""
#import sys
#
#rp_wspr_path = sys.argv[1:]

import paramiko
host = "10.0.0.188"
port = 22
transport = paramiko.Transport((host, port)) 
password = "changeme"
username = "root"
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)
filepath = '/dev/shm/ALL_WSPR.TXT'
localpath = r'C:\Users\gregg\Documents\Labview\ALL_WSPR_cpy.TXT'
#sftp.put(localpath, filepath)
sftp.get(filepath, localpath)
#sftp.get(rp_wspr_path,localpath)
sftp.close()
transport.close()

