#!/usr/bin/python

# This script is used to generate a summary of the journal entries in adapter journal files.
# It reads the journal logs from a file path specified using option -f or --file. if the file path is not specified, it reads the journal logs from the stdin.
# It excludes the journal entries that are generated by request which identified by the regular expression `\tI\t` in the journal log.
# It process the logs matching the expression spectified by the options -p or --pattern, the options is multiple to specific multiple pattern.
# Each line of the matched logs has items seprated with `\t`.
#   <timestamp(yyyy/mm/dd hh:mi:ss)> O <IP> <port> <request_id> <trace_id> <method> <path> <request_size> <status> <response_size> <duration>
# The script generates a summary of the journal entries in the following format:
#   <timestame(yyyy/mm/dd hh:mi)> <status> <count> <min_duration> <max_duration> <avg_duration>
# The jounral file is sorted by the timestamp in ascending order and has millions of lines. So the script must be memory friendly.
# 

import argparse
import re
from collections import defaultdict

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='File path to read the journal logs from')
    parser.add_argument('-p', '--pattern', nargs='+', help='Pattern(s) to match in the logs')
    return parser.parse_args()

def process_line(line, patterns, summary):
    if not re.search(r'\tI\t', line):  # exclude lines generated by request
        for pattern in patterns:
            if re.search(pattern, line):
                parts = line.split('\t')
                timestamp, status, duration = parts[0], parts[9], float(parts[11])
                summary[(timestamp[:16], status)][0] += 1
                summary[(timestamp[:16], status)][1] = min(summary[(timestamp[:16], status)][1], duration)
                summary[(timestamp[:16], status)][2] = max(summary[(timestamp[:16], status)][2], duration)
                summary[(timestamp[:16], status)][3] += duration
    return timestamp[:16]

def print_summary(summary, key):
    count, min_duration, max_duration, total_duration = summary[key]
    print(f'{key[0]} {key[1]} {count} {min_duration} {max_duration} {total_duration/count}')
    del summary[key]

def main():
    args = parse_args()
    summary = defaultdict(lambda: [0, float('inf'), float('-inf'), 0])  # count, min, max, total
    last_timestamp = None
    with open(args.file, 'r') if args.file else sys.stdin as file:
        for line in file:
            current_timestamp = process_line(line, args.pattern, summary)
            if last_timestamp and current_timestamp != last_timestamp:
                for key in list(summary.keys()):
                    if key[0] == last_timestamp:
                        print_summary(summary, key)
            last_timestamp = current_timestamp
    for key in list(summary.keys()):  # print remaining summaries
        print_summary(summary, key)

if __name__ == "__main__":
    main()