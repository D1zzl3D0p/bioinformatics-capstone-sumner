#!/bin/zsh

source vars.sh

if ! command -v docker; then
  echo "ERROR: Docker is required for PSORTb but was not found in PATH." >&2
  echo "       Install Docker Desktop from https://www.docker.com/products/docker-desktop/" >&2
  exit 1
fi

echo "-------------------------------- Extracting core genome ----------------------------------------"
mkdir -p "$reports_dir/phobius-results"

core_proteins_faa="$reports_dir/phobius-results/core_proteins.faa"
if [ -f "$core_proteins_faa" ]; then
  echo "  Using existing core proteins FASTA"
else
  echo "  Extracting high-quality core genome proteins..."
  conda run --no-capture-output -p "$MAMBA_ENVS/data_env" python3 "$scripts_dir/extract_core_proteins.py" --panaroo "$reports_dir/panaroo-results" --output "$core_proteins_faa"
fi
echo

echo "-------------------------------- Running Phobius ----------------------------------------"
mkdir -p "$reports_dir/phobius-results"

phobius_dir="$db_dir/phobius"
if [ ! -f "$phobius_dir/phobius.pl" ]; then
  echo "ERROR: Phobius not found at $phobius_dir" >&2
  echo "       Download from https://phobius.sbc.su.se/data.html" >&2
  exit 1
fi

phobius_abs=$(realpath "$phobius_dir")
core_proteins_abs=$(realpath "$core_proteins_faa")

core_out="$reports_dir/phobius-results/core.phobius.txt"
if [ -f "$core_out" ]; then
  echo "  Skipping core proteins (already done)"
else
  echo "  Processing core genome proteins..."
  docker run --rm -v "${phobius_abs}:/phobius_src:ro" -v "${core_proteins_abs}:/input/core_proteins.faa:ro" -w /tmp debian:stable-slim bash -c 'apt-get update -qq > /dev/null 2>&1; apt-get install -y -qq perl > /dev/null 2>&1; cp -r /phobius_src /phobius; chmod +x /phobius/decodeanhmm.64bit; cp /phobius/decodeanhmm.64bit /phobius/decodeanhmm; perl /phobius/phobius.pl -short /input/core_proteins.faa' > "$core_out" 2>/dev/null
fi
echo

echo "-------------------------------- Running PSORTb ----------------------------------------"
mkdir -p "$reports_dir/psortb-results"

core_psort_out="$reports_dir/psortb-results/core.psortb.txt"
if [ -f "$core_psort_out" ]; then
  echo "  Skipping core proteins (already done)"
else
  echo "  Processing core genome proteins..."
  tmpdir=$(mktemp -d)
  docker run --rm -v "$(realpath "$core_proteins_faa"):/input/core_proteins.faa:ro" -v "${tmpdir}:/results:rw" brinkmanlab/psortb_commandline:1.0.2 psortb -i /input/core_proteins.faa -r /results -n -o 2>/dev/null
  cat "${tmpdir}"/*.txt > "$core_psort_out" 2>/dev/null
  rm -rf "$tmpdir"
fi
echo

echo "-------------------------------- Parsing membrane protein results ----------------------------------------"
mkdir -p "$reports_dir/membrane-protein-results"

conda run --no-capture-output -p "$MAMBA_ENVS/data_env" python3 "$scripts_dir/parse_membrane_proteins.py" --phobius "$reports_dir/phobius-results" --psortb "$reports_dir/psortb-results" --panaroo "$reports_dir/panaroo-results/gene_presence_absence_roary.csv" --output "$reports_dir/membrane-protein-results" --core
echo
