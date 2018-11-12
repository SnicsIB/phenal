#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 12:07:05 2018

@author: ilbumi
"""

import argparse
import subprocess as sp


def create_parser():
    _parser = argparse.ArgumentParser(
        conflict_handler='resolve',
        description="Finds the most deviating from expected occurance dinucleotide "
    )
    _parser.add_argument(
        "input",
        help="Input in EMBOSS USA format. Default format is fasta"
    )
    return _parser


# single nucleotide frequency
args = create_parser().parse_args()
cmd = ("wordcount", args.input, "-wordsize", "1", "-out", "stdout")
process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
out, err = map(lambda x: x.decode("utf-8"), process.communicate())

one_nucl = dict(map(lambda x: x.split('\t'), filter(bool, out.split('\n'))))

# pairs nucleotide frequency
cmd = ("wordcount", args.input, "-wordsize", "2", "-out", "stdout")
process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
out, err = map(lambda x: x.decode("utf-8"), process.communicate())
two_nucl = tuple(map(lambda x: x.split('\t'), filter(bool, out.split('\n'))))

# finding frequencies (real/expected)
total_pairs = sum([float(x[1]) for x in two_nucl])
total_nucls = sum([float(x) for x in one_nucl.values()])
res = []
for pair in two_nucl:
    freq = float(pair[1])/total_pairs
    nucls = list(pair[0])
    expected_freq = float(one_nucl[nucls[0]]) * \
        float(one_nucl[nucls[1]])/total_nucls/total_nucls
    res.append((pair[0], freq/expected_freq))

print("The mostair: {}; Real over expected occurance: {}".format(
    *sorted(res, key=lambda x: max(x[1], 1/x[1]))[-1]))
