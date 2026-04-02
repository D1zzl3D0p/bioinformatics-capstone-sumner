#!/bin/zsh

source vars.sh

echo "--------------------------------Download/Update bakta db ----------------------------------------"
if [ ! -f "$db_dir/db/bakta.db" ]; then
  conda run --no-capture-output -p "$MAMBA_ENVS/bakta_env" \
    bakta_db download \
    --output $db_dir \
    --type full
  echo
else
  conda run --no-capture-output -p "$MAMBA_ENVS/bakta_env" \
    bakta_db update --db "$db_dir/db"
fi

echo "--------------------------------Running bakta ----------------------------------------"
mkdir -p "$reports_dir/bakta-results"
for genome in "$reads_dir"/*.fna; do
  prefix=$(basename "$genome" .fna)
  conda run --no-capture-output -p "$MAMBA_ENVS/bakta_env" \
    bakta \
    --db "$db_dir/db" \
    --verbose \
    --output "$reports_dir/bakta-results/" \
    --prefix "$prefix" \
    --threads "$thread_count" \
    --force \
    "$genome"
done
echo
