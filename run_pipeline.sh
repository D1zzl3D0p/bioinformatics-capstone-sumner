#!/bin/zsh

# 1. Stop the script if any command fails
set -e

# 2. Fix Mamba 2.0 Warning: Explicitly set the root prefix
export MAMBA_ROOT_PREFIX="/Users/dizzler/Miniforge3"

# 3. Initialize Mamba/Conda using the variable we just set
source "${MAMBA_ROOT_PREFIX}/etc/profile.d/conda.sh"
source "${MAMBA_ROOT_PREFIX}/etc/profile.d/mamba.sh"

# Import your variables
source vars.sh

# 4. Create the environment for Intel architecture (needed for bioconda tools on M1/M2/M3)
# We use CONDA_SUBDIR=osx-64 to ensure we get the right versions of quast/busco
echo "Creating environment..."
CONDA_SUBDIR=osx-64 mamba create -n capstone_env -y -c bioconda -c conda-forge \
    python=3.9 \
    ncbi-datasets-cli\
    seqkit \
    busco \
    sepp \
    quast

# 5. Activate the environment
mamba activate capstone_env

# 6. Ensure the environment always uses Intel mode for future installs
conda config --env --set subdir osx-64

# 7. Run your evaluation script
echo "Starting evaluation..."
./scripts/00-evaluation-of-data.sh
