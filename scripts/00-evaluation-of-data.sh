#!/bin/zsh

source vars.sh

echo "--------------------------------Running BUSCO ----------------------------------------"
mkdir -p "$reports_dir/busco-results"
conda run -p "$MAMBA_ENVS/busco_env" \
  busco -i $reads_dir \
  -m genome \
  -o "$reports_dir/busco-results/" \
  -l "enterobacterales_odb10" \
  --cpu $thread_count \
  --download_path $db_dir \
  -f
echo

echo "--------------------------------Running quast ----------------------------------------"
mkdir -p "$reports_dir/quast-results"
conda run -p "$MAMBA_ENVS/quast_env" \
  quast -o "$reports_dir/quast-results" $reads_dir/*
echo
