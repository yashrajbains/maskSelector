# maskSelector

'maskSelector': A simple Python package to quickly crop FITS target data and create boolean masking array for galaxy modeling 

## Tutorial
- In terminal, go to directory which contains relevant FITS files
- python ~/maskSelector/maskSelector/core.py
- Input FITS file name as prompted
- Full FITS file is displayed, from which you can select two points and crop the image to contain only relevant data 
- Close plotting window
- Input cropped data file name as prompted
- Cropped data is displayed, from which you can select two points to mask unwanted objects. You can mask any number of objects you want
- Close plotting window
- Input mask array file name as prompted
- Do some science!

## Installation

```bash
git clone https://github.com/your_username/maskSelector.git
cd maskSelector
pip install .
