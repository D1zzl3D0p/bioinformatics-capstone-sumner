#! /bin/bash

source vars.sh

for file in "$reads_dir"/*; do
  echo
  echo "processing file $file"
  echo

  echo "--------------------------------Running Datasets ----------------------------------------"
  datasets summary genome accession "$(basename "data/00-reads/GCF_000007545.1_ASM754v1_genomic.fna" | cut -d'_' -f1,2)" \
    >$reports_dir/ncbi-summary/"$(basename "$file").json"

  # echo "--------------------------------Running BUSCO ----------------------------------------"
  # busco -i "$file" -m genome -o "$reports_dir/busco-results/$file/" -l "enterobacterales_odb10" --cpu 11
  #
  # echo "--------------------------------Running Quast ----------------------------------------"
  # quast -o "$reports_dir/quast-results" "$file"

  #echo "--------------------------------Running Quast ----------------------------------------"

done
