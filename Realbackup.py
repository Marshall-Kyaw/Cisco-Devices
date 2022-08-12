import paramiko
import time
from getpass import getpass
import datetime

TNOW = datetime.datetime.now().replace(microsecond=0)

username = 'username'
password = 'password'


DEVICE_LIST = open ('devices.txt')                 # devices_list
for RTR in DEVICE_LIST:
    RTR = RTR.strip()
    print ('\n #### Connecting to the device ' + RTR + '\n' )
    SESSION = paramiko.SSHClient()
    SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    SESSION.connect(RTR,port=22,
                    username=username,
                    password=password,
                    look_for_keys=False,
                    allow_agent=False)

    DEVICE_ACCESS = SESSION.invoke_shell()
    DEVICE_ACCESS.send(b'en\n')
    DEVICE_ACCESS.send(b'password\n')           # type your password
    DEVICE_ACCESS.send(b'copy startup-config tftp: \n')
    DEVICE_ACCESS.send(b'192.168.*.** \n')      # type your destination ip
    DEVICE_ACCESS.send(b' \n')
    time.sleep(5)
    output = DEVICE_ACCESS.recv(65000)
    print (output.decode('ascii'))

    SESSION.close
