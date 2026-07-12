import sys
import time
import random

if len(sys.argv) != 4:
    sys.stderr.write("Usage: dynamic_routes.py <base_octet> <next_hop> <local_as>\n")
    sys.exit(1)

# Map the arguments
base_octet = sys.argv[1]
next_hop = sys.argv[2]
local_as = sys.argv[3]

# Generate 50 unique dynamic routes
DYNAMIC_ROUTES = [f"10.{base_octet}.{i}.0/24" for i in range(1, 51)]

# Dictionary to track the state of each route
route_states = {route: False for route in DYNAMIC_ROUTES}

def send_to_exabgp(command):
    sys.stdout.write(command + "\n")
    sys.stdout.flush()

time.sleep(10)

try:
    while True:
        target = random.choice(DYNAMIC_ROUTES)
        
        if route_states[target]:
            send_to_exabgp(f"withdraw route {target} next-hop {next_hop}")
            route_states[target] = False
        else:
            send_to_exabgp(f"announce route {target} next-hop {next_hop} as-path [ {local_as} ]")
            route_states[target] = True
            
        time.sleep(random.uniform(0.1, 2.0))

except KeyboardInterrupt:
    pass