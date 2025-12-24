# RIMAPS analysis script
## About
RIMAPS stands for Rotated Image with Maximum Average Power Spectrum.

This software make use of openly distributed software to compute the 2D fast fourier transform of surface images and returns the RIMAPS spectrum. 
The output format can be configured to be in any (or all) of the following:
* Plain text, space separated columns
* CSV, comma separated values output
* png image

## How to get it

You can either clone this repository:

    git clone git@github.com:monticellifernando/fRIMAPS.git

Or just get the zip file from this page


## Requirements

You need to have a working python environment with the following dependencies installed:
* opencv
* numpy
* matplotlib

## To use it you need to setup your environment! We provide two ways:
* mamba
* python environments

Try one of the following:


### 1 -  Install/setup environment with mamba:
Setup the specific python environment with mamba. The first time set it up like:

    mamba create -n fRIMAPS python=3.11
    mamba activate fRIMAPS
    pip install -r requirements.txt


Next time you use it, just activate the environment:

    mamba activate fRIMAPS

### 2 -  Python venv

First setup your environment. You need to be **inside** the folder of the project for this:

    cd fRIMAPS
    python3 -m venv fRIMAPS
    # And now activate it:
    source fRIMAPS/bin/activate
    pip install -r requirements.txt
    
Done. Next time you use it yo just need to activate it:

    source fRIMAPS/bin/activate

Thats it.



## How to use it!

To run it you need to call the '''fRIMAPS.py''' from the command line with at least the image input file as an argument. For eample, if you want to run over the provided examples of images under Images you can run:

    ./fRIMAPS.py  -f Images/circulo.png 

# PSD tool

We also provide a tool to compute PSD. How to run it? Just run the script passing the folder with all your images as a parameter

    ./Run_PD.py -P Images 

It will produce an output with the PSD computed for each figure in text format.
You can run with ```-h``` to get help:


    ./Run_PD.py -h
    
 
It will show you like:
```
RIMAPS Module! usage: fRIMAPS - the Free/Libre RIMAPS analysis tool, PSD tool [-h] [-F FILENAMES [FILENAMES ...]] [-P PATH] [-p] [-L LOGLEVEL]

options:
  -h, --help            show this help message and exit
  -F FILENAMES [FILENAMES ...], --FileNames FILENAMES [FILENAMES ...]
                        Input file names. I will do PSD on each file listed here.
  -P PATH, --Path PATH  Input folder where images live. I will loop over all images in this folder
  -p, --Plot            Plot PSD for each image file
  -L LOGLEVEL, --LogLevel LOGLEVEL
                        LogLevel. 1 ERROR, 2 WARNING, 4 INFO, 5 DEBUG, 7 VERBOSE

```
 



