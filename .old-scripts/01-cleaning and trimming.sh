#! /bin/bash

source vars.sh

# echo $data_dir
# echo $raws_dir
# echo $scripts_dir

for i in data/00-raws/*R1*.gz; do
  filename=$(basename $i)
  base=${filename/_R1_*/}
  cur_file_1=$i
  cur_file_2=${i/R1/R2}

  # A command to use max amount of cores, and output to the
  # trim_dir specified in vars.sh
  fastp \
    -w "$(nproc)" \
    -i "$cur_file_1" \
    -I "$cur_file_2" \
    -o "${cur_file_1/$raws_dir/$trim_dir}" \
    -O "${cur_file_2/$raws_dir/$trim_dir}" \
    -h "$reports_dir/00_fastp_$base.html" \
    -j "$reports_dir/00_fastp_$base.json"

done
