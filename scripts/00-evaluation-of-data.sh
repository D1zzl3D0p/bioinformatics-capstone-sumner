#! /bin/bash

source vars.sh

echo "--------------------------------Running BUSCO ----------------------------------------"
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
conda run -p "$MAMBA_ENVS/quast_env" \
  quast -o "$reports_dir/quast-results" $reads_dir/*
echo
