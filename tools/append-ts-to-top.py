# To process top logs form stdin
# Take out timestamp from line like "top - HH:MM:SS ........". The HH:MM:SS is the timestame.
# From the follow lines take out line end with redis-server and insert timestame before the line and output it.
# and do previous process again......

import re
import sys

timestamp = None
for line in sys.stdin:
  line = line.strip()
  if line.startswith('top - '):
    timestamp = re.search(r'(\d+:\d+:\d+)', line).group(1)
  elif line.endswith('redis-server'):
    if timestamp:
      print(timestamp, line)
      timestamp = None
