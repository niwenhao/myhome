# read a log file that each line is composed with "start_time(formated with hh:mm:ss) podname process_id durition access_per_second"
# it means has durition seconds with the throughput of access_per_second since the start_time
# I want to extends each line to durition lines same as the origion line but repire the start_time to the right vale.

import sys
import datetime

def extend_log_lines(log_lines):
    extended_lines = []
    for line in log_lines:
        start_time, podname, process_id, duration, access_per_second = line.split()
        start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")
        for i in range(int(duration)):
            new_start_time = start_time + datetime.timedelta(seconds=i)
            new_start_time_str = new_start_time.strftime("%H:%M:%S")
            new_line = f"{new_start_time_str} {podname} {process_id} {duration} {access_per_second}"
            extended_lines.append(new_line)
    return extended_lines


for line in sys.stdin:
    extended_lines = extend_log_lines([line])  
    for extended_line in extended_lines:
        print(extended_line)

