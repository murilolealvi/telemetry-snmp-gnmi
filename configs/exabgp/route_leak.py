import time
import sys
import csv
from datetime import datetime, timezone

if len(sys.argv) != 5:
    sys.stderr.write("Usage: route-leak.py <num_routes> <next_hop> <local_asn> <minutes>\n")
    sys.exit(1)

# Map the arguments
NUM_ROUTES = int(sys.argv[1])
NEXT_HOP = sys.argv[2]
LOCAL_ASN = sys.argv[3]
MAX_RUNTIME = sys.argv[4]
AS_PATH = f"[ {LOCAL_ASN} ]"
FLAP_INTERVAL = 15  # Seconds to wait between announce and withdraw

def generate_prefixes(count):
    prefixes = []
    for i in range(count):
        first_octet = i % 256
        second_octet = 32 + (i % 256)
        third_octet = 16 + (i // 256)
        prefixes.append(f"172.{second_octet}.{third_octet}.0/24")
    return prefixes

def main():
    prefixes = generate_prefixes(NUM_ROUTES)
    cycle = 1
    time.sleep(15)

    duration_seconds = MAX_RUNTIME * 60
    end_time = time.time() + float(duration_seconds)

    while time.time() < end_time:

        sys.stderr.write(f"[Cycle {cycle}] Announcing {NUM_ROUTES} routes...\n")
        
        for p in prefixes:
            sys.stdout.write(f"announce route {p} next-hop {NEXT_HOP} as-path {AS_PATH}\n")
        sys.stdout.flush()

        time.sleep(FLAP_INTERVAL)

        sys.stderr.write(f"[Cycle {cycle}] Withdrawing {NUM_ROUTES} routes...\n")
        
        for p in prefixes:
            sys.stdout.write(f"withdraw route {p} next-hop {NEXT_HOP}\n")
        sys.stdout.flush()
        
        time.sleep(FLAP_INTERVAL)
        cycle += 1

    sys.stderr.write("\nStopping the simulator and withdrawing all routes...\n")
    for p in prefixes:
        sys.stdout.write(f"withdraw route {p} next-hop {NEXT_HOP}\n")
    sys.stdout.flush()

if __name__ == "__main__":
    main()