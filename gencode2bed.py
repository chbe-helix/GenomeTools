#!/usr/bin/env python3
# 
# Copyright 2019, Christopher Bennett
# 
# This is a prototype script to align two linear sequences (genomes)
# 
# simple-genome-coord is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# fast-genome-aligner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# See <http://www.gnu.org/licenses/> for a copy of the GNU General Public License
# 

import sys, os, subprocess, re, random
from argparse import ArgumentParser
from itertools import product

def extract_annotations(fns, annotation, id_field):
    base_fn = fns.replace(".gtf", '')
    ofn = '%s-%s-%s.bed' % (base_fn, annotation, id_field)
    ofo = open(ofn, "w")

    with open(fns, 'r') as ifo:
        count = 0
        for line in ifo:
            if not line or line.startswith('#'):
                continue

            chrom, _, ann, l, r, _, strand, _, keys = line.strip().split('\t')
            if annotation and (ann not in [annotation]):
                continue

            count += 1
            keys = keys.split(';')
            dic = {}
            for key in keys:
                key = key.strip().replace('"', '')
                if not key:
                    continue

                label, val = key.split()
                dic[label] = val
            
            tid = dic[id_field]
            if annotation in ['exon']:
                nexon = dic["exon_number"]
            else:
                nexon = 'NA'

            nline = [chrom, l, r, tid, '0', strand, nexon]
            ofo.write('\t'.join(nline))
            ofo.write('\n')  
        print('%d %s features read' % (count, annotation))
    ofo.close()

"""
"""
if __name__ == '__main__':
    parser = ArgumentParser(
        description='Gencode 2 Bed')

    parser.add_argument('--gtf',
                        dest = 'gtf_fn',
                        type = str,
                        required = True,
                        help='gtf file name')
    parser.add_argument('--annotation',
                        dest = 'annotation',
                        type = str,
                        default = "ALL",
                        help='Annotation to extract (Default: ALL')
    parser.add_argument('--id-field',
                        dest = 'id_field',
                        type = str,
                        required = True,
                        help='Field in gtf to use as BED name')
    
    args = parser.parse_args()

    if args.annotation == "ALL":
        args.annotation = ''

    extract_annotations(args.gtf_fn,
                        args.annotation,
                        args.id_field)
