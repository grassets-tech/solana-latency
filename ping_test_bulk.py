import csv
from concurrent.futures import ThreadPoolExecutor
from ping3 import ping, verbose_ping
import subprocess
import re

INPUT_FILE = 'ips.csv'
OUTPUT_FILE = 'ping_results.csv'

def ping_ip(validator):
    try:
        result = []
        ip = validator[0]
        result = subprocess.run(
            ['ping', '-c', '10', '-i', '2', '-W', '5', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        output = result.stdout
        print(output)
        timedout = re.search(r'timed', output)
        if timedout is not None:
            return [validator[0], 'N/A', 'N/A']

        # Parse packet loss
        loss_match = re.search(r'(\d+)% packet loss', output)
        packet_loss = loss_match.group(1) if loss_match else 'N/A'

        # Parse average latency
        rtt_match = re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/', output)
        avg_latency = rtt_match.group(1) if rtt_match else 'N/A'

        result = [validator[0], avg_latency, packet_loss]
        print (result)
        return (result)
    except Exception as e:
        return [validator[0], validator[4], 'N/A', 'N/A']

def main():
    # Read IPs from file
    ips = []
    with open(INPUT_FILE) as f:
       for line in f:
           l = line.strip().split(",")
           ips.append(l)
    print("Start latency testing...")

    # Concurrent ping
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(ping_ip, ips))
    print(results)
    
    # Write results to CSV
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['IP', 'Latency', 'Packet Loss'])
        writer.writerows(results)

    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
