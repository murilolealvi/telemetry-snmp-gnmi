import os
from passlib.hash import md5_crypt
from jinja2 import Environment, FileSystemLoader

def hash_junos_password(password):
    return md5_crypt.hash(password, salt="salt")

env = Environment(loader=FileSystemLoader('.'))
env.filters['junos_hash'] = hash_junos_password

pe_template = env.get_template('pe-router.j2')
p_template = env.get_template('p-router.j2')

# Map nodes as JSON into the template
pe_routers = [
{
        "hostname": "pe1",
        "loopback_ip": "10.0.0.10/32",
        "nms_ip": "10.10.10.201",
        # to RR
        "rr_iface": "ge-0/0/0",
        "rr_iface_ip": "10.1.10.1/31",
        "rr_ip": "10.0.0.100",
        # to P-router
        "core_iface": "ge-0/0/2",
        "core_ip": "10.1.1.0/31",
        # to CE
        "ce_iface": "ge-0/0/1",
        "ce_ip": "192.168.11.1/24",
        "ce_peer_ip": "192.168.11.2",
        "ce_peer_as": "65001"
    },
    {
        "hostname": "pe2",
        "loopback_ip": "10.0.0.20/32",
        "nms_ip": "10.10.10.201",
        # to RR
        "rr_iface": "ge-0/0/0",
        "rr_iface_ip": "10.1.20.1/31",
        "rr_ip": "10.0.0.100",   
        # to P-router
        "core_iface": "ge-0/0/2",
        "core_ip": "10.1.2.0/31",
        # to CE
        "ce_iface": "ge-0/0/1",
        "ce_ip": "192.168.12.1/24",
        "ce_peer_ip": "192.168.12.2",
        "ce_peer_as": "65002"
    }
]

p_routers = [
    {
        "hostname": "p1",
        "loopback_ip": "10.0.0.30/32",
        "nms_ip": "10.10.10.201",
        "eth1_ip": "10.1.1.1/31",    # to PE1
        "eth2_ip": "10.1.12.0/31",   # to P2
        "eth3_ip": "10.1.13.1/31"    # to P3
    },
    {
        "hostname": "p2",
        "loopback_ip": "10.0.0.40/32",
        "nms_ip": "10.10.10.201",
        "eth1_ip": "10.1.2.1/31",    # to PE2
        "eth2_ip": "10.1.12.1/31",   # to P1
        "eth3_ip": "10.1.23.1/31"    # to P3
    },
    {
        "hostname": "p3",
        "loopback_ip": "10.0.0.50/32",
        "nms_ip": "10.10.10.201",
        "eth1_ip": "10.1.23.0/31",   # to P2
        "eth2_ip": "10.1.13.0/31",   # to P1
        "eth3_ip": "127.0.0.1/8"     # dummy config
    }
]

for router in pe_routers:
    config = pe_template.render(router)
    filename = f"{router['hostname']}.cfg"
    
    with open(filename, 'w') as file:
        file.write(config)
    print(f"File {filename} generated")

for router in p_routers:
    config = p_template.render(router)
    filename = f"{router['hostname']}.cfg"
    
    with open(filename, 'w') as file:
        file.write(config)
    print(f"File {filename} generated")