# Input: lines from stdin, each line composed with "timestamp(hh:mm:ss) pod_name process_id 1 throughput_per_second"
# I want to summary the throughput_per_second by timestamp.
# Output: each line composed with "timestamp(hh:mm:ss) throughput_per_second"

import sys
from collections import defaultdict

throughput_by_timestamp = defaultdict(float)

for line in sys.stdin:
    parts = line.split()
    timestamp = parts[0]
    throughput = float(parts[4])
    throughput_by_timestamp[timestamp] += throughput

for timestamp, throughput in throughput_by_timestamp.items():
    print(f"{timestamp} {throughput}")
