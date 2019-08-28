#!/usr/bin/env python
# 
# Copyright 2019, Christopher Bennett
# 
# This code is made to be crosscompatable with Python2 and Python 3 though there is no guarentee of this
#
# This python module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This python module is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# See <http://www.gnu.org/licenses/> for a copy of the GNU General Public License

import sys, os, subprocess, re, random
import glob, multiprocessing
import gzip, urllib

def reverse_complement(seq):
    comp_table = {'A':'T', 'C':'G', 'G':'C', 'T':'A'}
    rc_seq = ""
    for s in reversed(seq):
        if s in comp_table:
            rc_seq += comp_table[s]
        else:
            rc_seq += s
    return rc_seq

def read_genome(nfile):
    chr_dic, chr_names, chr_full_names = {}, [], []

    seqs = open(nfile, 'r').read()
    seqs = seqs.strip('\n').split('>')[1:]

    chr_name, chr_full_name, sequence = "", "", ""
    while seqs:
        ix = seqs[0].find('\n')

        chr_full_name, sequence = seqs[0][:ix], seqs[0][ix:].replace('\n','')
        chr_name = chr_full_name.split()[0]

        chr_dic[chr_name] = sequence
        chr_names.append(chr_name)
        chr_full_names.append(chr_full_name)

        seqs.pop(0)
    
    return chr_dic, chr_names, chr_full_names

def read_gtf(nfile, index_by):
    if not os.path.exists(nfile):
        print("Cannot find %s" % nfile)
        return -1

    data_set, data_tags = [], {}     
    with open(nfile, 'r') as ifo:
        count = 0
        for line in ifo:
            if not line or line.startswith('#'):
                continue
 
            line = line.strip().split('\t')
            if len(line) < 2:
                continue

            tags = line[-1].split(';')
            for tag in tags:
                tag = tag.strip().replace('"', '')
                if not tag:
                    continue
 
                label, val = tag.split()

                if label not in data_tags:
                    data_tags[label] = {}
                if val not in data_tags[label]:
                    data_tags[label][val] = []

                data_tags[label][val].append(count)
 
            data_set.append(line[:-1])
            count += 1
 
        print('%d lines read' % (count))

    return data_set, data_tags

def read_bed(nfile, index_id):
     if not os.path.exists(nfile):
        print("Cannot find %s" % nfile)
        return -1

    if not isinstance(index_id, int):
        print("index_id is not of int type")
        return -1

    data_set, data_keys = [], {}
    with open(nfile, 'r') as ifi:
        count = 0
        for line in ifi:
            if line.startswith("#") or not line:
                continue

            line = line.strip().split()

            if index_id > len(line)-1:
                print("Index %d selected is outside the column number %d" % (index_id, len(line)-1)
                return -1

            if line[index_id] not in data_keys:
                data_keys[line[index_id]] = []

            data_set.append(line)
            data_keys[line[index_id]].append(count)

            count += 1
            
        print('%d lines read' % (count))

    return data_set, data_keys

## Reads Gzip from FTP into a PIPE that can be iterated through
def read_urlgzip(ftp):
    request = urllib.request.Request(
        ftp,
        headers={
            "Accept-Encoding":"gzip"
        })
    response = urllib.request.urlopen(request)
    gzipFile = gzip.GzipFile(fileobj=response)

    return gzipFile
