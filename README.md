# MatGAN
Generative deep learning model for inorganic materials


## Video demo of the material generation process
- [MatGAN in action demo video](https://www.youtube.com/watch?v=m8dD-ugoAPA&feature=youtu.be)

## Installation of run environment
$pip install -r requirement.txt

## How to run:

- $python generate_data.py OQMD gan-materials-oqmd.csv
- $python generate_data.py ICSD gan-materials-icsd.csv
- $python generate_data.py MP gan-materials-mp.csv

This will generate 1024 hypothetical materials. After duplicate removal, all unique materials will be saved to gan-materials-oqmd/icsd/mp.csv

To generate more materials, just continue to re-run this same command, the results will be appended to the output file: gan-materials-oqmd.csv

## Generated hypothetical materials by GAN-ICSD

- [Generated materials by GAN-ICSD](.\generated_data\ICSD\generated_ICSD_2m.csv)


