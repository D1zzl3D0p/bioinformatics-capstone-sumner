# bioinformatics-capstone-sumner

A bioinformatics pipeline for analyzing and annotating bacterial genome assemblies. This project downloads genome sequences from NCBI, performs quality assessment, genome annotation, and pan-genome comparison across four independent tools.

## Overview

This pipeline processes bacterial genome assemblies (Enterobacterales) through three main stages:

**Stage 0 — Quality Evaluation** (`scripts/00-evaluation-of-data.sh`)
- **BUSCO**: Assesses genome completeness using single-copy orthologs
- **QUAST**: Generates assembly quality reports

**Stage 1 — Genome Annotation** (`scripts/01-genome-annotation.sh`)
- **Bakta**: Rapid and standardized annotation of bacterial genomes

**Stage 2 — Pan-Genome Analysis** (`scripts/02-pan-genome-analysis.sh`)

Four pan-genome tools are run in parallel to enable methodological comparison of their outputs:
- **PPanGGOLiN**: Partitions the pangenome into persistent, shell, and cloud gene families using a probabilistic model on a pangenome graph
- **ggCaller**: Graph-based gene calling and pangenome analysis across all genomes simultaneously
- **Panaroo**: Graph-based pangenome pipeline with error correction, using Bakta GFF3 annotations as input
- **Roary**: Rapid core genome alignment and pangenome clustering, using Bakta GFF3 annotations as input

**Stage 3 — Membrane Protein Analysis** (`scripts/03-membrane-protein-analysis.sh`)

Identifies membrane-associated proteins conserved across all samples by combining two complementary predictors against the Panaroo core genome:
- **Phobius**: Predicts transmembrane topology and signal peptides from protein sequences (run per sample via conda)
- **PSORTb**: Predicts subcellular localization in gram-negative bacteria — inner membrane, outer membrane, periplasmic, etc. (run per sample via Docker)

Results are cross-referenced with Panaroo's `gene_presence_absence.csv` to filter for core genes only. Two output files are produced:
- `core_membrane_proteins_all.tsv` — core genes flagged by either tool in any sample
- `core_membrane_proteins_consensus.tsv` — core genes flagged by **both** tools in **every** sample

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
| `ppanggolin` | 2.2.5 | Probabilistic pangenome graph partitioning | `ppanggolin_env` |
| `ggcaller` | 1.5.0 | Graph-based gene calling and pan-genome analysis | `ggcaller_env` |
| `panaroo` | 1.6.0 | Error-correcting graph-based pangenome pipeline | `panaroo_env` |
| `roary` | 3.13.0 | Rapid core genome alignment and pangenome clustering | `roary_env` |
| `phobius` | 1.01 | Transmembrane topology and signal peptide prediction | Docker |
| `psortb` | latest | Subcellular localization prediction (gram-negative) | Docker |

## Project Structure

```
.
├── data/
│   ├── 00-reads/                  # Genome assembly files (.fna)
│   └── 99-indexes/                # Mash indexes
├── databases/                     # Tool databases (bakta, busco)
├── reports/
│   ├── bakta-results/             # Bakta annotation output (.gff3)
│   ├── busco-results/             # BUSCO analysis output
│   ├── ggcaller-results/          # ggCaller pan-genome output
│   ├── ncbi-summary/              # NCBI genome summaries
│   ├── panaroo-results/           # Panaroo pan-genome output
│   ├── ppanggolin-results/        # PPanGGOLiN pan-genome output
│   ├── quast-results/             # QUAST reports
│   ├── roary-results/             # Roary pan-genome output
│   ├── phobius-results/           # Phobius per-sample predictions
│   ├── psortb-results/            # PSORTb per-sample predictions
│   └── membrane-protein-results/  # Cross-referenced core membrane proteins
├── scripts/
│   ├── 00-evaluation-of-data.sh   # BUSCO + QUAST
│   ├── 01-genome-annotation.sh    # Bakta annotation
│   ├── 02-pan-genome-analysis.sh  # Pan-genome comparison
│   ├── 03-membrane-protein-analysis.sh  # Phobius + PSORTb membrane prediction
│   └── parse_membrane_proteins.py       # Cross-reference & output script
├── gen_envs.sh                    # Create conda environments
├── run_pipeline.sh                # Main entry point
└── vars.sh                        # Environment variables
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
./scripts/02-pan-genome-analysis.sh  # Pan-genome comparison
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

**PPanGGOLiN**
> Gautreau G, Bazin A, Gachet M, Planel R, Burlot L, Dubois M, Perrin A, Médigue C, Calteau A, Cruveiller S, Matias C, Ambroset C, Siguier P, Glaser P, Touchon M, Rocha EPC. 2020. PPanGGOLiN: Depicting microbial diversity via a partitioned pangenome graph. *PLOS Computational Biology* 16(3):e1007732. https://doi.org/10.1371/journal.pcbi.1007732

**ggCaller**
> Horsfield ST, Tonkin-Hill G, Croucher NJ, Lees JA. 2023. Accurate and fast graph-based pangenome annotation and clustering with ggCaller. *Genome Research* 33(9):1622–1637. https://doi.org/10.1101/gr.277733.123

**Panaroo**
> Tonkin-Hill G, MacAlasdair N, Coelho LP, Croucher NJ, Corander J, Parkhill J, Bentley SD. 2020. Producing polished prokaryotic pangenomes with the Panaroo pipeline. *Genome Biology* 21:180. https://doi.org/10.1186/s13059-020-02090-4

**Roary**
> Page AJ, Cummins CA, Hunt M, Wong VK, Reuter S, Holden MTG, Fookes M, Falush D, Keane JA, Parkhill J. 2015. Roary: rapid large-scale prokaryote pan genome analysis. *Bioinformatics* 31(22):3691–3693. https://doi.org/10.1093/bioinformatics/btv421
