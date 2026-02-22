# bioinformatics-capstone-sumner

A bioinformatics pipeline for analyzing bacterial genome assemblies. This project downloads genome sequences from NCBI and performs quality assessment using BUSCO and QUAST.

## Overview

This pipeline processes bacterial genome assemblies (Enterobacterales) and evaluates their quality through:
- **NCBI Datasets**: Summarizes genome metadata
- **BUSCO**: Assesses genome completeness using single-copy orthologs
- **QUAST**: Generates quality reports for genome assemblies

## Data

Place genome assemblies (`.fna` files) in `data/00-reads/`. Current samples include:
- GCF_000007545.1, GCF_000020745.1, GCF_000020885.1, GCF_000020925.1
- GCF_000022165.1, GCF_000170215.1, GCF_000170255.1, GCF_000171255.1
- GCF_000171275.1, GCF_000171315.1, GCF_000171415.1, GCF_000171515.1, GCF_000171535.2

## Dependencies

- conda or mamba
- macOS (OSX-64 architecture)

## Installation

```bash
git clone https://github.com/D1zzl3D0p/bioinformatics-capstone-sumner
cd bioinformatics-capstone-sumner
./run_pipeline.sh
```

The pipeline will:
1. Create a conda environment (`capstone_env`) with required tools
2. Activate the environment
3. Run the evaluation script

## Tools Installed

- `ncbi-datasets-cli` - Download and summarize NCBI genome data
- `seqkit` - FASTA/Q file manipulation
- `busco` - Genome completeness assessment
- `sepp` - Species placement in phylogenetic trees
- `quast` - Genome assembly quality evaluation

## Project Structure

```
.
├── data/
│   ├── 00-reads/           # Genome assembly files
│   └── 99-indexes/        # Mash indexes
├── reports/
│   ├── busco-results/      # BUSCO analysis output
│   ├── ncbi-summary/       # NCBI genome summaries
│   └── quast-results/      # QUAST reports
├── scripts/
│   └── 00-evaluation-of-data.sh
├── tools/
│   └── mash-OSX64-v2.3/    # Mash tool
├── run_pipeline.sh        # Main entry point
└── vars.sh                # Environment variables
```

## Usage

Run the full pipeline:
```bash
./run_pipeline.sh
```

Run individual steps:
```bash
source vars.sh
./scripts/00-evaluation-of-data.sh
```
