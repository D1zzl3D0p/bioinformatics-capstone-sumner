#!/bin/zsh
set -e

source "${MAMBA_ROOT_PREFIX}/etc/profile.d/conda.sh"
source "${MAMBA_ROOT_PREFIX}/etc/profile.d/mamba.sh"

# Function to create osx-64 envs on Apple Silicon
create_env() {
  local name=$1
  shift
  echo "--- Creating environment: $name ---"
  CONDA_SUBDIR=osx-64 mamba create -n "$name" -y -c bioconda -c conda-forge "$@"
  # Ensure this env always stays in x86 mode for future manual installs
  conda activate "$name"
  conda config --env --set subdir osx-64
  conda deactivate
}

# --- 1. Data Processing Env (Lightweight tools) ---
create_env "data_env" python=3.11 ncbi-datasets-cli seqkit

# --- 2. Quality Assessment (CheckM2) ---
# CheckM2 is picky; we'll use Python 3.8 as it's the most stable for its ML models
create_env "checkm2_env" python=3.8 checkm2

# --- 3. Evolutionary/Lineage (BUSCO & SEPP) ---
# SEPP and BUSCO often share dependencies like HMMER and Diamond
create_env "busco_env" python=3.10 busco sepp

# --- 4. Assembly Evaluation (QUAST) ---
create_env "quast_env" python=3.9 quast

echo "All environments created successfully!"
