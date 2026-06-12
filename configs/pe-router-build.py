import os
from passlib.hash import md5_crypt
from jinja2 import Environment, FileSystemLoader

def hash_junos_password(password):
    return md5_crypt.hash(password, salt="salt")

env = Environment(loader=FileSystemLoader('.'))
env.filters['junos_hash'] = hash_junos_password
template = env.get_template('pe-router.j2')

# Map nodes as JSON into the template
routers = [
{
        "hostname": "pe1",
        "loopback_ip": "10.0.0.10/32",
        "rr_ip": "10.0.0.100",
        # to P-router
        "core_iface": "ge-0/0/2",
        "core_ip": "10.1.1.0/31",
        # to CE
        "ce_iface": "ge-0/0/1",
        "ce_ip": "192.168.11.1/24"
    },
    {
        "hostname": "pe2",
        "loopback_ip": "10.0.0.20/32",
        "rr_ip": "10.0.0.100",   
        # to P-router
        "core_iface": "ge-0/0/2",
        "core_ip": "10.1.2.0/31",
        # to CE
        "ce_iface": "ge-0/0/1",
        "ce_ip": "192.168.12.1/24"
    }
]

for router in routers:
    config = template.render(router)
    filename = f"{router['hostname']}.cfg"
    
    with open(filename, 'w') as file:
        file.write(config)
    print(f"File {filename} generated")