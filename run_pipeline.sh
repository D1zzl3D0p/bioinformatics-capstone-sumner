#! /bin/bash

# This file runs the full pipeline

# Import variables
source vars.sh

# Load conda
eval "$(conda shell.bash hook)"

# Install packages
conda install -c bioconda fastp

conda activate

# clean and trim reads
./scripts/01-cleaning\ and\ trimming.sh
