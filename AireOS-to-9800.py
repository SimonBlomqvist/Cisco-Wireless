from netmiko import ConnectHandler
import getpass
import os

def GET_HOSTNAME(CONNECT):
    HOSTNAME=CONNECT.send_command('grep include "System Name" "show sysinfo"',expect_string=r'Press any key to continue..')
    HOSTNAME=CONNECT.send_command('\n',expect_string=r'System Name').split()[2]
    print(f"\n***** Connected to {HOSTNAME} *****")
    return HOSTNAME

def GET_IP(CONNECT):
    REDUNDANCY=CONNECT.send_command('grep include Redundancy "show redundancy detail"',expect_string=r'Press any key to continue..')
    REDUNDANCY=CONNECT.send_command('\n',expect_string=r'Redundancy').split()
    return REDUNDANCY

def GET_VLAN(CONNECT):
    VLAN=CONNECT.send_command(f'grep include {WLC} "show interface summary"',expect_string=r'Press any key to continue..')
    VLAN=CONNECT.send_command('\n',expect_string=r'management').split()[2]
    return VLAN

def GET_GATEWAY(CONNECT):
    GATEWAY=CONNECT.send_command('grep include Gateway "show interface detailed management"',expect_string=r'Press any key to continue..')
    GATEWAY=CONNECT.send_command('\n',expect_string=r'Gateway').split()[2]
    return GATEWAY

def GET_NETMASK(CONNECT):
    NETMASK=CONNECT.send_command('grep include Netmask "show interface detailed management"',expect_string=r'Press any key to continue..')
    NETMASK=CONNECT.send_command('\n',expect_string=r'Netmask').split()[2]
    return NETMASK

def CONVERT(NETMASK):
    OCTETS=NETMASK.split('.')
    BITS=0
    for OCTET in OCTETS:
        BINARY_OCTET=bin(int(OCTET))
        BIT_COUNT=BINARY_OCTET.count('1')
        BITS+=BIT_COUNT
    return '/'+str(BITS)

def GET_COUNTRY(CONNECT):
    COUNTRY=CONNECT.send_command('show country',expect_string=r'Configured Country').split()[2]
    return COUNTRY

print("\n***** Enter information for new device *****")
INTERFACE=input("Interface range for port-channel (e.g. te0/1/0-1): ")
SNMP_GROUP=input("SNMPv3 group name: ")
SNMP_USER=input("SNMPv3 user: ")
SNMP_PASSWORD=input("SNMPv3 password: ")
LOCAL_USERNAME=input("Local username for the 9800: ")
LOCAL_PASSWORD=input("Local password for the 9800: ")
DOMAIN_NAME=input("Domain name: ")
print("\n***** Login to AireOS controller *****")
WLC=input("IP address of WLC: ")
USERNAME=input("Username: ")
PASSWORD=getpass.getpass("Password: ")
CONNECT=ConnectHandler(ip=WLC,port=22,username=USERNAME,password=PASSWORD,device_type="cisco_wlc_ssh",banner_timeout=10)
CONNECT.send_command("config paging enable")
HOSTNAME=GET_HOSTNAME(CONNECT)
REDUNDANCY=GET_IP(CONNECT)
VLAN=GET_VLAN(CONNECT)
GATEWAY=GET_GATEWAY(CONNECT)
NETMASK=GET_NETMASK(CONNECT)
CIDR=CONVERT(NETMASK)
COUNTRY=GET_COUNTRY(CONNECT)
print("***** Information collected *****")
CONNECT.send_command("config paging disable")
CONNECT.disconnect()
print("***** Connection closed *****")

PRIMARY_WLC=[
    "*****Paste this configuration in exec mode*****\n",
    "chassis 1 renumber 1",
    "chassis 1 priority 2",
    f"chassis redundancy ha-interface local-ip {REDUNDANCY[15]} {CIDR} remote-ip {REDUNDANCY[21]}",
    "configure terminal",
    f"redun-management interface vlan {VLAN} chassis 1 address {REDUNDANCY[4]} chassis 2 address {REDUNDANCY[10]}",
    f"hostname {HOSTNAME}",
    f"ip domain name {DOMAIN_NAME}",
    f"username {LOCAL_USERNAME} privilege 15 algorithm-type scrypt secret {LOCAL_PASSWORD}",
    f"vlan {VLAN}",
    f"interface vlan {VLAN}",
    f"ip address {WLC} {NETMASK}",
    "no shutdown",
    f"wireless management interface vlan {VLAN}",
    f"ip route 0.0.0.0 0.0.0.0 {GATEWAY}",
    f"snmp-server group {SNMP_GROUP} v3 auth",
    f"snmp-server user {SNMP_USER} {SNMP_GROUP} v3 auth sha {SNMP_PASSWORD} priv aes 128 {SNMP_PASSWORD}",
    f"country code {COUNTRY}",
    "aaa new-model",
    "aaa authentication login default local",
    "aaa authorization exec default local",
    "port-channel load-balance src-dst-mixed-ip-port",
    f"interface range {INTERFACE}",
    "no shutdown",
    "switchport mode trunk",
    "channel-group 1 mode active",
    "end",
    "write"
]
SECONDARY_WLC=[
    "*****Paste this configuration in exec mode*****\n",
    "chassis 1 renumber 2",
    "chassis 2 priority 1",
    f"chassis redundancy ha-interface local-ip {REDUNDANCY[21]} {CIDR} remote-ip {REDUNDANCY[15]}",
    "end",
    "write"
]

with open(f"{HOSTNAME}-Primary.txt","w") as file:
    for item in PRIMARY_WLC:
        file.write(item+"\n")
with open(f"{HOSTNAME}-Secondary.txt","w") as file:
    for item in SECONDARY_WLC:
        file.write(item+"\n")
