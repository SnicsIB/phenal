"""
Creates cog matrix from cog database.

Usage:

    python cog_matrix_builder.py -i [cog_database_file] -o [output_file]


Args:

    [cog_database_file] -- path to file, default: cog2003-2014.csv, if does not exist, can be retrieved from NCBI's ftp server
    [output_file] -- path to output file, default: cog_matrix.csv

Dependencies:

    pandas 0.22.0


Example:

    python cog_matrix_builder.py -i cog.csv  -o matrix.csv
"""
from ftplib import FTP
from sys import argv
import pandas as pd
import os


cog_db = 'cog2003-2014.csv'
output = 'cog_matrix.csv'
try:
    for argi in range(len(argv)):
        if argv[argi] == '-i':
            cog_db = argv[argi+1]
        if argv[argi] == '-o':
            output = argv[argi+1]
except IndexError:
    print('Incorrect input')
    exit(1)

# preparing COG database files
if cog_db == 'cog2003-2014.csv':
    data_ncbi = 'ftp.ncbi.nih.gov'
    filepaths = os.listdir()
    with FTP(data_ncbi) as ftp:
        ftp.login()
        ftp.cwd('pub/COG/COG2014/data/')
        if cog_db not in filepaths:
            print('downloading... ' + cog_db)
            with open(cog_db, 'wb') as fl:
                ftp.retrbinary('RETR ' + cog_db, fl.write)

# transforming table
df = {}
try:
    with open(cog_db) as fin:
        print('transforming... ' + cog_db)
        for raw_line in fin:
            fields = raw_line.split(',')
            if fields[1] not in df.keys():
                df[fields[1]] = {}
            df[fields[1]][fields[6]] = 1
    pd.DataFrame(df).fillna(0).transpose().to_csv(output)
except IOError:
    print('Input file does not exist (IOE)')
    exit(2)
