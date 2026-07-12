import subprocess
import time
import sys


CLIENT_NODE = "iperf-client"
SERVER_IP = "10.60.0.100"

# Traffic profile
BASELINE_BW = "10M"    
BASELINE_TIME = 45        

PEAK_BW = "200M"         
PEAK_TIME = 15            

def run_iperf(bandwidth, duration, phase_name):
    """Executes a blocking iperf3 command for a specific duration."""
    print(f"[{time.strftime('%H:%M:%S')}] Starting {phase_name} Phase: {bandwidth}bps for {duration}s")
    cmd = f"docker exec {CLIENT_NODE} iperf3 -c {SERVER_IP} -u -b {bandwidth} -t {duration}"
    
    # Block the script until the iperf3 timer finishes
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("Starting Volumetric Traffic Simulator...")
print("-" * 40)

try:
    while True:
        # Normal Traffic
        run_iperf(BASELINE_BW, BASELINE_TIME, "BASELINE")
        
        # Volumetric Spike
        run_iperf(PEAK_BW, PEAK_TIME, "ATTACK PEAK")

except KeyboardInterrupt:
    print("\nSimulator stopped by user.")

    cleanup_cmd = f"docker exec {CLIENT_NODE} pkill iperf3"
    subprocess.run(cleanup_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sys.exit(0)