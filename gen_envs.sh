#!/bin/zsh
set -e

source vars.sh

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
create_env "data_env" python=3.11 ncbi-datasets-cli=18.18.0 seqkit=2.12.0

# --- 2. Evolutionary/Lineage (BUSCO & SEPP) ---
# SEPP and BUSCO often share dependencies like HMMER and Diamond
create_env "busco_env" python=3.10 busco=6.0.0 sepp=4.5.5

# --- 3. Assembly Evaluation (QUAST) ---
create_env "quast_env" python=3.9 quast=5.3.0

# --- 4. Genome Annotation (bakta) ---
create_env "bakta_env" bakta=1.12.0

echo "All environments created successfully!"
