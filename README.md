# bioinformatics-capstone-sumner

A bioinformatics pipeline for analyzing and annotating bacterial genome assemblies. This project downloads genome sequences from NCBI, performs quality assessment, and runs genome annotation.

## Overview

This pipeline processes bacterial genome assemblies (Enterobacterales) through two main stages:

**Stage 0 — Quality Evaluation** (`scripts/00-evaluation-of-data.sh`)
- **BUSCO**: Assesses genome completeness using single-copy orthologs
- **QUAST**: Generates assembly quality reports

**Stage 1 — Genome Annotation** (`scripts/01-genome-annotation.sh`)
- **Bakta**: Rapid and standardized annotation of bacterial genomes

## Data

Place genome assemblies (`.fna` files) in `data/00-reads/`. Current samples include:
- GCF_000007545.1, GCF_000020745.1, GCF_000020885.1, GCF_000020925.1
- GCF_000022165.1, GCF_000170215.1, GCF_000170255.1, GCF_000171255.1
- GCF_000171275.1, GCF_000171315.1, GCF_000171415.1, GCF_000171515.1, GCF_000171535.2

## Dependencies

- conda or mamba (Miniforge recommended)
- macOS (OSX-64 architecture; Apple Silicon users run via Rosetta via `CONDA_SUBDIR=osx-64`)

## Installation

```bash
git clone https://github.com/D1zzl3D0p/bioinformatics-capstone-sumner
cd bioinformatics-capstone-sumner
./gen_envs.sh   # Create all conda environments
./run_pipeline.sh
```

## Tools Installed

| Tool | Version | Purpose | Environment |
|------|---------|---------|-------------|
| `ncbi-datasets-cli` | 18.18.0 | Download and summarize NCBI genome data | `data_env` |
| `seqkit` | 2.12.0 | FASTA/Q file manipulation and statistics | `data_env` |
| `busco` | 6.0.0 | Genome completeness assessment | `busco_env` |
| `sepp` | 4.5.5 | Phylogenetic placement of sequences | `busco_env` |
| `quast` | 5.3.0 | Genome assembly quality evaluation | `quast_env` |
| `bakta` | 1.12.0 | Rapid bacterial genome annotation | `bakta_env` |

## Project Structure

```
.
├── data/
│   ├── 00-reads/           # Genome assembly files (.fna)
│   └── 99-indexes/         # Mash indexes
├── databases/              # Tool databases (bakta, busco)
├── reports/
│   ├── bakta-results/      # Bakta annotation output
│   ├── busco-results/      # BUSCO analysis output
│   ├── ncbi-summary/       # NCBI genome summaries
│   └── quast-results/      # QUAST reports
├── scripts/
│   ├── 00-evaluation-of-data.sh   # BUSCO + QUAST
│   └── 01-genome-annotation.sh    # Bakta annotation
├── gen_envs.sh            # Create conda environments
├── run_pipeline.sh        # Main entry point
└── vars.sh                # Environment variables
```

## Usage

Generate conda environments (first time only):
```bash
./gen_envs.sh
```

Run the full pipeline:
```bash
./run_pipeline.sh
```

Run individual stages:
```bash
source vars.sh
./scripts/00-evaluation-of-data.sh   # Quality evaluation
./scripts/01-genome-annotation.sh    # Genome annotation
```

## Citations

If using this pipeline or the tools it employs, please cite:

**BUSCO**
> Manni M, Berkeley MR, Seppey M, Simão FA, Zdobnov EM. 2021. BUSCO Update: Novel and Streamlined Workflows along with Broader and Deeper Phylogenetic Coverage for Scoring of Eukaryotic, Prokaryotic, and Viral Genomes. *Molecular Biology and Evolution* 38(10):4647–4654. https://doi.org/10.1093/molbev/msab199

**QUAST**
> Gurevich A, Saveliev V, Vyahhi N, Tesler G. 2013. QUAST: quality assessment tool for genome assemblies. *Bioinformatics* 29(8):1072–1075. https://doi.org/10.1093/bioinformatics/btt086

**Bakta**
> Schwengers O, Jelonek L, Dieckmann MA, Beyvers S, Blom J, Goesmann A. 2021. Bakta: rapid and standardized annotation of bacterial genomes via a comprehensive database. *Microbial Genomics* 7(11):000685. https://doi.org/10.1099/mgen.0.000685

**SeqKit**
> Shen W, Le S, Li Y, Hu F. 2016. SeqKit: A Cross-Platform and Ultrafast Toolkit for FASTA/Q File Manipulation. *PLOS ONE* 11(10):e0163962. https://doi.org/10.1371/journal.pone.0163962

**SEPP**
> Mirarab S, Nguyen N, Warnow T. 2012. SEPP: SATe-enabled phylogenetic placement. *Pacific Symposium on Biocomputing* 17:247–258. https://doi.org/10.1142/9789814366496_0024

**NCBI Datasets**
> National Center for Biotechnology Information (NCBI). NCBI Datasets. https://www.ncbi.nlm.nih.gov/datasets/
