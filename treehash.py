#!/usr/bin/env python3
import sys
import os
import json
import hashlib
from argparse import ArgumentParser

ONE_MiB = 1024 * 1024

verbose = False

def P(x):
    if verbose:
        print(x)


def main():
    global verbose
    parser = ArgumentParser()
    parser.add_argument('-j', '--comparetojson',
                        help='compare calculated to this aws cli output json',
                        default=None)
    parser.add_argument('-c', '--comparetohash', help='compare to this hash',
                        default=None)
    parser.add_argument('-v', '--verbose', help='turn on verbose mode',
                        action='store_true', default=False)
    parser.add_argument('FILE', help='file on which to calculate treehash')

    args = parser.parse_args(sys.argv[1:])

    verbose = args.verbose

    j = None
    compare = None
    if args.comparetojson:
        with open(args.comparetojson, 'rt') as fp:
            j = json.load(fp)
        compare = j.get('checksum', None)
        if compare is None:
            raise Exception("No checksum key in json input")
    elif args.comparetohash:
        compare = args.comparetohash

    th = None
    with open(args.FILE, 'rb') as fp:
        th = treehash(fp).hex()

    if compare:
        if th != compare:
            print("Checksums are not Equal!")
            print("Calculated: %s" % th)
            print("From file:  %s" % compare)
            os.exit(1)
        else:
            print("Checksums are equal!")
    print("Calculated: %s" % th)


def treehash(fp):
    ch = get_chunk_hashes(fp)
    return chunkhash(ch)


def get_chunk_hashes(fp):

    file_size = os.stat(fp.name).st_size
    num_chunks = file_size / ONE_MiB
    if num_chunks > int(num_chunks):
        num_chunks += 1
    num_chunks = int(num_chunks)

    if num_chunks == 0:
        P("Empty file!")
        return [hashlib.sha256().digest()]

    chunk_hashes = []

    cnt = 0
    while True:
        buf = fp.read(ONE_MiB)
        if len(buf) == 0:
            break
        sha = hashlib.sha256()
        sha.update(buf)
        chunk_hashes.append(sha.digest())
        cnt += 1
        if cnt % 500 == 0:
            P("Read %dMB" % cnt)

    P("Done reading file.\nRead %dMB" % cnt)
    P("File read, returning %d chunks" % len(chunk_hashes))
    return chunk_hashes


def chunkhash(chunk_hashes):
    prev_hashes = chunk_hashes

    lp = len(prev_hashes)
    while lp > 1:
        P("len(prev_hashes): %d" % lp)

        curr_hashes = []
        i = 0
        while True:
            if i >= lp:
                break
            if (lp-i) >= 2:
                sha = hashlib.sha256()
                sha.update(prev_hashes[i])
                sha.update(prev_hashes[i+1])
                curr_hashes.append(sha.digest())
            else:
                curr_hashes.append(prev_hashes[i])
            i += 2
        prev_hashes = curr_hashes
        lp = len(prev_hashes)
    return prev_hashes[0]

if __name__ == '__main__':
    main()
