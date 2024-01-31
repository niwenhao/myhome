# Input: lines from stdin, each line composed with "timestamp(hh:mm:ss) pod_name process_id 1 throughput_per_second"
# I want to summary the throughput_per_second by timestamp.
# Output: each line composed with "timestamp(hh:mm:ss) throughput_per_second"