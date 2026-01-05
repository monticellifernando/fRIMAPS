#!env python3
# -*- coding: utf-8 -*-
from RIMAPS import PowerDist
from pathlib import Path
import argparse, sys

def main(argv):
    parser = argparse.ArgumentParser("fRIMAPS - the Free/Libre RIMAPS analysis tool, PSD tool")
    parser.add_argument('-F', '--FileNames',  required=False, nargs ='+', help="Input file names. I will do PSD on each file listed here.")
    parser.add_argument('-P', '--Path',  required=False, help="Input folder where images live. I will loop over all images in this folder")
    parser.add_argument('-p', '--Plot',  required=False, action="store_true",  help="Plot PSD for each image file")
    parser.add_argument('-c', '--Comma',  required=False, action="store_true",  help="Comma for lfoating point instead of dot")
    parser.add_argument('-L', '--LogLevel',  required=False, type=int,  help="LogLevel. 1 ERROR, 2 WARNING, 4 INFO, 5 DEBUG, 7 VERBOSE", default = 4)
    args = parser.parse_args()

    print()
   
    m_files = []
    if args.Path:
        print(f'Appending files from path:  {args.Path}')
        for m_file in Path(args.Path).iterdir():
            m_files.append(str(m_file))

    if args.FileNames:
        print(f'Appending  files  {args.FileNames}')
        for m_file in args.FileNames:
            m_files.append(m_file)

    print(f'Processing files: {m_files}')

    for m_file in m_files:
        f = PowerDist.Powerdist()
        f.LogLevel = args.LogLevel
        m_dir_char = '/'
        if '\\' in m_file:
            f.DEBUG('   Windows filename Detected!')
            m_dir_char = '\\'
        if not m_file.split(m_dir_char)[-1].startswith('PSD'):
            f.INFO(f'Computing PSD on {m_file}')
        else:
            f.WARNING(f'Ignoring PSD produced file {m_file}')
            continue
        m_outputfig = m_dir_char.join(m_file.split(m_dir_char)[:-1] + ['PSD_'+m_file.split(m_dir_char)[-1]])
        try:
            f.AddImageFromFile(m_file)
            f.Get2DFFT()
            f.ComputePSD()
            f.PlotPSD(m_outputfig)
            txtout = m_outputfig+'.txt' 
            f.DumpPSD(txtout)
            if args.Comma:
                f.INFO(f' Updating output text file using commas -> {txtout}...')
                # Read the file content
                with open(txtout, 'r') as file:
                    file_contents = file.read()
                
                # Perform the search and replace operation
                updated_contents = file_contents.replace('.', ',')
                
                # Overwrite the file with the updated content
                with open(txtout, 'w') as file:
                    file.write(updated_contents)
        except Exception as e:
            f.ERROR(f'  problem processing file {m_file}')
            f.ERROR(f'{e}')

    
if __name__ == "__main__":
    main(sys.argv[1:])
