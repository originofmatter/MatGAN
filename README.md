# MatGAN
Generative deep learning model for inorganic materials


## Video demo 
- [MatGAN in action demo video](https://youtu.be/psneoau1m-8)

## Installation of running environment
$pip install -r requirement.txt

## How to run:

- $python generate_data.py OQMD gan-materials-oqmd.csv
- $python generate_data.py ICSD gan-materials-icsd.csv
- $python generate_data.py MP gan-materials-mp.csv

This will generate 1024 hypothetical materials to corresponding csv files such as gan-materials-oqmd.csv

To generate more materials, just continue to re-run this same command, the results will be appended to the assigned output file

## Generated hypothetical materials by GAN-ICSD

- [Generated materials by GAN-ICSD](https://github.com/originofmatter/MatGAN/blob/master/generated_data/ICSD_GAN_2M.csv)


