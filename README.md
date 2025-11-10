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

    git clone git@github.com:monticellifernando/RIMAPS.git

Or just get the zip file from this page


## Requirements

You need to have a working python environment with the following dependencies installed:
* opencv
* numpy
* matplotlib

## Install/setup environment with mamba:
Setup the specific python environment with mamba. The first time set it up like:



    mamba create -n fRIMAPS python=3.11
    mamba activate fRIMAPS
    pip install -r requirements.txt


Next time you use it, just activate the environment:

    mamba activate fRIMAPS


## How to use it!

To run it you need to call the '''fRIMAPS.py''' from the command line with at least the image input file as an argument. For eample, if you want to run over the provided examples of images under Images you can run:

    ./fRIMAPS.py  -f Images/circulo.png 


