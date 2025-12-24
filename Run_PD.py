#!env python3
# -*- coding: utf-8 -*-
from RIMAPS import PowerDist
from pathlib import Path
import argparse, sys

def main(argv):
    parser = argparse.ArgumentParser("FreeMAPS - the Free/Libre RIMAPS analysis tool, PDS tool")
    parser.add_argument('-F', '--FileNames',  required=False, nargs ='+', help="Input file names. I will do PDS on each file listed here.")
    parser.add_argument('-P', '--Path',  required=False, help="Input folder where images live. I will loop over all images in this folder")
    parser.add_argument('-p', '--Plot',  required=False, action="store_true",  help="Plot PSD for each image file")
    args = parser.parse_args()

    print()
   
    m_files = []
    if args.Path:
        for m_file in Path(args.Path).iterdir():
            #print(f'Processing file from path:  {m_file}')
            m_files.append(m_file)

    for m_file in args.FileNames:
        #print(f'Processing file:  {m_file}')
        m_files.append(m_file)

    print(f'Processing files: {m_files}')
    f = PowerDist.Powerdist()
    f.LogLevel = 3

    for m_file in m_files:
        f.INFO(f'Computing PDS on {m_file}')
        m_outputfig = '/'.join(m_file.split('/')[:-1] + ['PDS_'+m_file.split('/')[-1]])

        f.AddImageFromFile(m_file)
        f.Get2DFFT()
        f.ComputePSD()
        f.PlotPSD(m_outputfig)
        f.DumpPSD(m_outputfig+'.txt')
    
if __name__ == "__main__":
    main(sys.argv[1:])
