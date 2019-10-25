Installation of run environment
$pip install -r requirement.txt

How to run:

$python generate_data.py OQMD gan-materials-oqmd.csv
$python generate_data.py ICSD gan-materials-icsd.csv
$python generate_data.py MP gan-materials-icsd.csv

This will generate 1024 hypothetical materials. After removal of duplicates, all unique materials will be saved to gan-materials-oqmd.csv

To generate more materials, just continue to re-run this same command, the results will be appended to the output file: gan-materials-oqmd.csv



