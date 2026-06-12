import os
from jinja2 import Template

with open('p-router.j2', 'r') as file:
    template = Template(file.read())

routers = [
    {
        "hostname": "p1",
        "loopback_ip": "10.0.0.13/32",
        "eth1_ip": "10.1.1.1/31",    # to PE1
        "eth2_ip": "10.1.12.0/31",   # to P2
        "eth3_ip": "10.1.13.1/31"    # to P3
    },
    {
        "hostname": "p2",
        "loopback_ip": "10.0.0.14/32",
        "eth1_ip": "10.1.2.1/31",    # to PE2
        "eth2_ip": "10.1.12.1/31",   # to P1
        "eth3_ip": "10.1.23.1/31"    # to P3
    },
    {
        "hostname": "p3",
        "loopback_ip": "10.0.0.15/32",
        "eth1_ip": "10.1.23.0/31",   # to P2
        "eth2_ip": "10.1.13.0/31",   # to P1
        "eth3_ip": "127.0.0.1/8"     # dummy config
    }
]

for router in routers:
    config = template.render(router)
    filename = f"{router['hostname']}.cfg"
    
    with open(filename, 'w') as file:
        file.write(config)
    print(f"File {filename} generated")