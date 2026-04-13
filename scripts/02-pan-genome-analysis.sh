#!/bin/zsh

source vars.sh

echo "--------------------------------Running PPanGGOLiN ----------------------------------------"
ppanggolin_list="$reports_dir/ppanggolin-genomes.tsv"
for gff in "$reports_dir/bakta-results/"*.gff3; do
  name=$(basename "$gff" .gff3)
  printf "%s\t%s\n" "$name" "$(realpath "$gff")"
done > "$ppanggolin_list"
mkdir -p "$reports_dir/ppanggolin-results"
conda run -p "$MAMBA_ENVS/ppanggolin_env" \
  ppanggolin workflow \
  --anno "$ppanggolin_list" \
  -f \
  -o "$reports_dir/ppanggolin-results" \
  --cpu "$thread_count"
echo

echo "--------------------------------Building genome reference list ----------------------------------------"
refs_file="$reports_dir/pan-genome-refs.txt"
for genome in "$reads_dir"/*.fna; do
  realpath "$genome"
done > "$refs_file"
echo

echo "--------------------------------Running ggCaller ----------------------------------------"
mkdir -p "$reports_dir/ggcaller-results"
conda run -p "$MAMBA_ENVS/ggcaller_env" \
  ggcaller \
  --refs "$refs_file" \
  --out "$reports_dir/ggcaller-results" \
  --threads "$thread_count"
echo

echo "--------------------------------Running Panaroo ----------------------------------------"
mkdir -p "$reports_dir/panaroo-results"
conda run -p "$MAMBA_ENVS/panaroo_env" \
  panaroo \
  -i "$reports_dir/bakta-results/"*.gff3 \
  -o "$reports_dir/panaroo-results" \
  --clean-mode moderate \
  --remove-invalid-genes \
  -t "$thread_count"
echo

echo "--------------------------------Running Roary ----------------------------------------"
mkdir -p "$reports_dir/roary-results"
conda run -p "$MAMBA_ENVS/roary_env" \
  roary \
  -f "$reports_dir/roary-results" \
  -p "$thread_count" \
  -e -n \
  "$reports_dir/bakta-results/"*.gff3
echo
