#!/usr/bin/env python3

import sys
import gzip
import urllib.request

if __name__ == "__main__":
    if not sys.argv[1]:
        print("Needs at least one file name")
        exit(1)

    ftp = sys.argv[1]
    if "/" not in ftp:
        print("incorrect input format")
        exit(1)

    request = urllib.request.Request(
        ftp,
        headers={
            "Accept-Encoding":"gzip"
        })
    response = urllib.request.urlopen(request)
    gzipFile = gzip.GzipFile(fileobj=response)

    for gline in gzipFile:
        gline = gline.decode('utf-8')
        sys.stdout.write(gline)

    gzipFile.close()
