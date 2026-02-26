# A file to hold all the variables I want to use in my pipeline, because I cannot be bothered
# to try and type all this crap out

# folders and file paths
export data_dir="data"
export reads_dir=$data_dir/00-reads
export index_dir=$data_dir/99-indexes
# export trim_dir=$data_dir/01-cleaned\ and\ trimmed
export scripts_dir="scripts"
export reports_dir="reports"
export thread_count=$(($(nproc) - 1))
export db_dir="databases"

# tool specific settings
export MAMBA_ROOT_PREFIX="/Users/dizzler/Miniforge3"
export MAMBA_ENVS="$MAMBA_ROOT_PREFIX/envs"
export CHECKM2DB="$db_dir/CheckM2_database/uniref100.KO.1.dmnd"
export BUSCO_RESOURCES_DESTINATION="$db_dir/busco_downloads"
