#!/usr/bin/env python3
"""
extract_core_proteins.py

Extract core genome proteins from Panaroo outputs filtered by quality criteria.
Uses gene_presence_absence_roary.csv to identify core genes, then extracts
sequences using gene_data.csv to map to combined_protein_CDS.fasta.

Usage:
    python extract_core_proteins.py --panaroo <dir> --output <faa>

Output:
    - Core genome protein FASTA file with only high-quality sequences
"""
import argparse
import csv
import os
import sys
from pathlib import Path


def parse_roary_core_genes(csv_path, quality_filters):
    """Parse gene_presence_absence_roary.csv to get core gene info."""
    with open(csv_path, newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)

    sample_start = 14
    sample_cols = header[sample_start:]
    total_samples = len(sample_cols)

    core_gene_info = {}

    with open(csv_path, newline="") as fh:
        reader = csv.reader(fh)
        next(reader)

        for row in reader:
            if len(row) < sample_start:
                continue

            try:
                isolate_count = int(row[3])
            except ValueError:
                continue

            if isolate_count != total_samples:
                continue

            gene_name = row[0]
            annotation = row[2]

            locus_tag = None
            for i in range(total_samples):
                cell = row[sample_start + i] if (sample_start + i) < len(row) else ""
                tags = [t.strip() for t in cell.split("\t") if t.strip()]

                for tag in tags:
                    if any(bad in tag.lower() for bad in quality_filters):
                        continue
                    locus_tag = tag
                    break

                if locus_tag:
                    break

            if locus_tag:
                core_gene_info[gene_name] = {
                    "annotation": annotation,
                    "locus_tag": locus_tag,
                }

    return core_gene_info


def load_annotation_to_seq(gene_data_path):
    """Load gene_data.csv: annotation_id -> sequence."""
    annotation_to_seq = {}
    with open(gene_data_path, newline="") as fh:
        reader = csv.reader(fh)
        next(reader)
        for row in reader:
            if len(row) < 5:
                continue
            annotation_id = row[3]
            sequence = row[4]
            annotation_to_seq[annotation_id] = sequence
    return annotation_to_seq


def main():
    parser = argparse.ArgumentParser(
        description="Extract core genome proteins with quality filtering"
    )
    parser.add_argument(
        "--panaroo",
        required=True,
        help="Path to Panaroo results directory"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output FASTA path for core proteins"
    )
    parser.add_argument(
        "--filters",
        nargs="*",
        default=["pseudo", "truncated", "partial", "frag"],
        help="Quality filters (default: pseudo truncated partial frag)"
    )
    args = parser.parse_args()

    panaroo_dir = Path(args.panaroo)
    roary_csv = panaroo_dir / "gene_presence_absence_roary.csv"
    gene_data = panaroo_dir / "gene_data.csv"

    if not roary_csv.exists():
        print(f"ERROR: {roary_csv} not found", file=sys.stderr)
        sys.exit(1)

    if not gene_data.exists():
        print(f"ERROR: {gene_data} not found", file=sys.stderr)
        sys.exit(1)

    quality_filters = [f.lower() for f in args.filters]

    print("Parsing Roary core genome...")
    core_gene_info = parse_roary_core_genes(roary_csv, quality_filters)
    print(f"  Found {len(core_gene_info)} core gene clusters")

    if not core_gene_info:
        print("ERROR: No core genes found", file=sys.stderr)
        sys.exit(1)

    print("Loading annotation sequences...")
    annotation_to_seq = load_annotation_to_seq(gene_data)
    print(f"  Loaded {len(annotation_to_seq)} sequences")

    core_sequences = {}
    missing = []
    for gene_name, info in core_gene_info.items():
        locus_tag = info["locus_tag"]
        if locus_tag in annotation_to_seq:
            core_sequences[gene_name] = annotation_to_seq[locus_tag]
        else:
            missing.append(locus_tag)

    print(f"  Extracted {len(core_sequences)} core sequences")

    if missing:
        print(f"  Warning: {len(missing)} locus tags not found in gene_data.csv")
        if len(missing) <= 5:
            print(f"    Missing: {missing[:5]}")

    if not core_sequences:
        print("ERROR: No core sequences extracted", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    def clean_gene_name(name):
        """Clean gene name for Phobius compatibility."""
        name = name.replace("~~~", "_")
        name = name.replace(";", "_")
        name = name.replace(":", "_")
        name = name.replace(",", "_")
        name = name.replace(" ", "_")
        return name

    def clean_sequence(seq):
        """Remove stop codon markers (*) from sequence."""
        seq = seq.replace("*", "X")
        return seq

    print(f"Writing {len(core_sequences)} sequences to {args.output}...")
    with open(args.output, "w") as fh:
        for gene_name in sorted(core_sequences.keys()):
            seq = clean_sequence(core_sequences[gene_name])
            name = clean_gene_name(gene_name)
            fh.write(f">{name}\n")
            for i in range(0, len(seq), 60):
                fh.write(f"{seq[i:i+60]}\n")

    print(f"Done. Core genome FASTA: {args.output}")


if __name__ == "__main__":
    main()
