from netmiko import ConnectHandler
import getpass
import os
 
def GET_HOSTNAME(CONNECT):
    HOSTNAME=CONNECT.send_command('grep include "System Name" "show sysinfo"',expect_string=r'Press any key to continue..')
    HOSTNAME=CONNECT.send_command('\n',expect_string=r'System Name').split()[2]
    print(f"\n***** Connected to {HOSTNAME} *****")
    return HOSTNAME
def GET_ACCESS_POINTS(CONNECT):
    ACCESS_POINTS=[]
    OUTPUT=CONNECT.send_command('show ap summary')
    LINES=OUTPUT.splitlines()
    for line in LINES:
        if 'AP Name' in line or 'Global AP' in line or 'Number of APs' in line or '-----' in line or not line.strip():
            continue
        WORDS=line.split()
        AP_NAME=WORDS[0]
        ACCESS_POINTS.append(AP_NAME)
    return ACCESS_POINTS
def MIGRATION_FILES(ACCESS_POINTS,NEW_WLC_HOSTNAME,NEW_WLC_IP,HOSTNAME):
    with open(f"{HOSTNAME}-AP-Migration.txt","w") as file:
        for AP in ACCESS_POINTS:
            line=f"config ap primary-base {NEW_WLC_HOSTNAME} {AP} {NEW_WLC_IP}\n"
            file.write(line)
 
print("\n***** Enter information about new controller *****")
NEW_WLC_HOSTNAME=input("What is the hostname of the new WLC: ")
NEW_WLC_IP=input("What is the IP address of the new WLC: ")
print("\n***** Login to old AireOS controller *****")
WLC=input("IP address of WLC: ")
USERNAME=input("Username: ")
PASSWORD=getpass.getpass("Password: ")
CONNECT=ConnectHandler(ip=WLC,port=22,username=USERNAME,password=PASSWORD,device_type="cisco_wlc_ssh",banner_timeout=10)
CONNECT.send_command("config paging disable")
HOSTNAME=GET_HOSTNAME(CONNECT)
ACCESS_POINTS=GET_ACCESS_POINTS(CONNECT)
MIGRATION_FILES(ACCESS_POINTS,NEW_WLC_HOSTNAME,NEW_WLC_IP,HOSTNAME)
print("***** Information collected *****")
CONNECT.send_command("config paging enable")
CONNECT.disconnect()
print("***** Connection closed *****")
