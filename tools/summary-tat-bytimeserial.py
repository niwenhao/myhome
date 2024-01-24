import argparse
import sys
import re
import io
import datetime


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
    parser.add_argument('--dataptn', '-d',
                        action="append"
                        help="集計対象レコードキーワード")
    parser.add_argument('--tatindex',
                        type=int,
                        help="tatデータ抽出項目番号(１ベース)")


    args = parser.parse_args()

    if args.input != "-":
        jnlfile = open(args.input, "r")
    else:
        jnlfile = sys.stdin
    
    if args.warmup:
        warmptn = re.compile(args.warmup)
    else:
        warmptn = None

    interval = datetime.timedelta(seconds=args.interval)
    return (jnlfile, warmptn, interval, args.dataptn, args.tatindex)

(jnlfile, warmptn, interval, dataptns, tatindex) = prepare_env()

start = None

cnt = 0
sum = 0

for ln in jnlfile:
    if warmptn and warmptn.search(ln):
        continue

    if ln.find("GRPC_SERVER_REQ") != -1:
        continue

    if dataptns and len(dataptns) > 0:
        matched = False
        for ptn in dataptns:
            if ln.find(ptn) != -1:
                matched = True
        if not matched:
            continue

    items = ln.split("\t")
    s = re.sub(r'\,.*$', "", items[0])
    ts = datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    tat = int(re.sub(r'\[msec\]$', "", items[tatindex-1]))

    if start == None:
        start = ts

    if ts <=start + interval:
        cnt += 1
        sum += tat
    else:
        if start:
            print(start.strftime("%Y-%m-%d %H:%M:%S"), cnt, sum/cnt)
        
        f = False
        while start + interval < ts:
            start += interval
            if f:
                print(start.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                f = True
        cnt = 1
        sum = tat
