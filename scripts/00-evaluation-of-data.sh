#! /bin/bash

source vars.sh

for file in "$reads_dir"/*; do
  echo
  echo "--------------------------------Processing File: $file -------------------------------------"
  echo

  echo "--------------------------------Running Datasets ----------------------------------------"
  conda run -p "$MAMBA_ENVS/data_env" \
    datasets summary genome accession "$(basename "data/00-reads/GCF_000007545.1_ASM754v1_genomic.fna" | cut -d'_' -f1,2)" \
    >$reports_dir/ncbi-summary/"$(basename "$file").json"
  echo

  echo "--------------------------------Running BUSCO ----------------------------------------"
  conda run -p "$MAMBA_ENVS/busco_env" \
    busco -i "$file" \
    -m genome \
    -o "$reports_dir/busco-results/$(basename "$file")/" \
    -l "enterobacterales_odb10" \
    --cpu $thread_count
  echo

  echo "--------------------------------Running quast ----------------------------------------"
  conda run -p "$MAMBA_ENVS/quast_env" \
    quast -o "$reports_dir/quast-results/$(basename "$file")" "$file"
  echo
done

echo "Downloading checkm2 database, this may take a while ...."
curl -C - -L https://zenodo.org/records/5571251/files/checkm2_database.tar.gz?download=1 -o "$db_dir/checkm2_database.tar.gz"
echo "finished with database download, it got downloaded to:"
echo "$CHECKM2DB"
echo "extracting database ...."
tar -xzf "$db_dir/checkm2_database.tar.gz" -C "$db_dir"

echo "--------------------------------Running checkm2 ----------------------------------------"
conda run -p "$MAMBA_ENVS/checkm2_env" \
  checkm2 predict \
  --threads $thread_count \
  --input "$reads_dir" \
  --output-directory "$reports_dir/checkm-results" \
  --extension .fna \
  --database_path "$CHECKM2DB" \
  --force
echo
