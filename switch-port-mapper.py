"""
switch-mapper

Trying to find the IP address of the device connected to a switch?

How it works:

Stage 1: Get user credentials and login to switch
Stage 2: Run 'show mac-addr-table' and push output to local file
Stage 3: Run nmap scan and push output to local file

Note:
nmap MAC addresses will be appended to one list
switch MAC table will be appended to another list
the two list will then be compared to correlate IP addresses

while i <= network_len:

    device = nmap[0]

    switch_mac_addr = [mac addresses...]

    if interface_nmap in switch_mac_addr:
        device = {
            # create device...
            "IP": "192.168.76.32",
            "MAC": "FC:4D:D4:D5:24:26",
            "INTERFACE": "0/1"
        }
    
    

Stage 4: Map nmap MAC ADDRESSES to Switch MAC ADDRESS Table together
Stage 5: Display mapping of switch ports to IP Addresses

Example output:

Device:
IP Address: 192.168.1.17
MAC ADDRESS: F0:9F:B2:10:FE:2B
Port: 0/4


todo:

implement sanity check for detecting virtual machines

if 1 interface has multiple mac addresses it MUST be a Hypervisor

add ssh functionality (for fully automatic use)

Python SSH libraries
paramiko: https://github.com/paramiko/paramiko - https://docs.paramiko.org/en/stable/
pexpect: https://github.com/pexpect/pexpect - https://pexpect.readthedocs.io/en/stable/api/pxssh.html

add file read option
"""

import re

# https://stackoverflow.com/questions/26891833/python-regex-extract-mac-addresses-from-string
p_mac_addr = re.compile(r'(?:[0-9a-fA-F]:?){12}')

p_ip_addr = re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b')

p_interface = re.compile(r'(\d\/\d)') 
# Maybe ([0]\/\d) for regex? as 5/1 and other weird interface like 3/1 show up.

# Proof of concept
# one line from each file is matched to be pairs

nmap_mac_addr = []
switch_mac_addr = []

example_nmap = 'Nmap scan report for setup.ubnt.com (192.168.76.1) MAC Address: F0:9F:C2:10:EE:4B (Ubiquiti Networks)'

example_switch = '1        F0:9F:C2:10:EE:4B   0/4                    4        Learned'

ip = re.findall(p_ip_addr, example_nmap)

nmap_mac = re.findall(p_mac_addr, example_switch)

n_interface = re.findall(p_interface, example_switch)

example_device = {
    "IP": ip,
    "MAC": nmap_mac,
    "INTERFACE": n_interface
}

print(example_device)

"""
Examples:

Linux:

# sudo nmap -O 192.168.76.0/24 | grep -e '192.168.' -e 'MAC Address'

Nmap scan report for setup.ubnt.com (192.168.76.1)
MAC Address: F0:9F:C2:10:EE:4B (Ubiquiti Networks)
Nmap scan report for 192.168.76.6
MAC Address: FC:EC:DA:74:A1:76 (Ubiquiti Networks)

Cisco IOS/Ubiquiti:

(Privliged Exec) # show mac-addr-table

VLAN ID  MAC Address         Interface              IfIndex  Status
-------  ------------------  ---------------------  -------  ------------
1        0A:9B:DF:14:A7:52   0/4                    4        Learned
1        8E:27:55:8F:52:35   0/4                    4        Learned
1        96:02:88:38:2F:A3   0/4                    4        Learned
1        B4:2E:99:3C:39:C9   0/2                    2        Learned
1        D6:12:02:75:32:B1   0/4                    4        Learned
1        F0:9F:C2:10:8E:4E   0/5                    5        Learned
1        F0:9F:C2:10:EE:4B   0/1                    1        Learned
1        FC:4D:D4:D5:24:26   0/4                    4        Learned

"""
