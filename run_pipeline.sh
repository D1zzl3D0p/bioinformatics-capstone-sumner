#!/bin/zsh

# Stop the script if any command fails
set -e

# Import variables
source vars.sh

# Generate the mamba/conda environments
#./gen_envs.sh

# Start the pipeline
./scripts/00-evaluation-of-data.sh
