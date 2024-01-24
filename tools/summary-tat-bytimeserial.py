import argparse
import sys
import re
import io
import datetime

jnlfile: io.TextIOBase
warmptn : re.Pattern
interval = None
start = None

cnt = 0
sum = 0

def prepare_env():
    parser = argparse.ArgumentParser(description="アクセスジャーナルを解析して、開始時間から一定間隔でTATの平均をリストアップする。")
    parser.add_argument('--input', '-f',
                        type=str,
                        help='入力アクセスジャーナリストログファイルのパス、-で指定した場合、標準入力になる。',
                        required=True
                        )
    parser.add_argument('--warmup', '-w',
                        type=str,
                        help='ウォームアップリクエストの特徴文字列の正規表現式、指定しない場合、ウォームアップなしと見なし',
                        required=False
                        )
    parser.add_argument('--interval', '-i',
                       type=int,
                       help='TAT集計間隔',
                       required=True)


    args = parser.parse_args()

    if args.input != "-":
        jnlfile = open(args.input, "r")
    else:
        jnlfile = sys.stdin
    
    if args.warmup:
        warmptn = re.compile(args.warmup)

    interval = datetime.timedelta(seconds=args.interval)


prepare_env()

for ln in jnlfile:
    if warmptn.search(ln):
        continue
    if ln.find("GRPC_SERVER_REQ") == -1:
        continue

    items = ln.split("\t")
    s = re.sub(r',.*$', "", items[0])
    ts = datetime.datetime.strptime(s, "%Y/%m/%d %H:%M:%S")
    tat = int(re.sub(r'\[msec\]$', "", items[11]))

    if start == None:
        start = ts

    if ts <=start + interval:
        cnt += 1
        sum += tat
    else:
        if start:
            print(start.strftime("%F %T"), sum/cnt)
        
        while start + interval > ts:
            start += interval
        cnt = 1
        sum = tat
