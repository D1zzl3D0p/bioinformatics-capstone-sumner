#!/usr/bin/env python3
"""
parse_membrane_proteins.py

Cross-references Phobius and PSORTb results with the Panaroo core genome
to identify membrane-associated proteins present in all samples.

Outputs:
  core_membrane_proteins_all.tsv        - all core genes flagged by either tool
  core_membrane_proteins_consensus.tsv  - core genes flagged by BOTH tools in every sample
"""
import argparse
import csv
import os
import sys
from pathlib import Path


def clean_gene_name(name):
    """Clean gene name to match extract_core_proteins.py output."""
    name = name.replace("~~~", "_")
    name = name.replace(";", "_")
    name = name.replace(":", "_")
    name = name.replace(",", "_")
    name = name.replace(" ", "_")
    return name


# ---- Parsers ----------------------------------------------------------------

def parse_phobius_dir(results_dir, core_mode=False):
    """
    Read *.phobius.txt files (short format):
        SEQENCE ID                  TM SP PREDICTION

    Args:
        results_dir: Directory containing Phobius results
        core_mode: If True, aggregate all per-sample results
                  If False, expect per-sample *.phobius.txt files

    Returns:
        If core_mode: dict of {locus_tag: has_membrane} for all samples
        Else: {sample: set_of_locus_tags_with_TM_or_SP}
    """
    if core_mode:
        all_membrane = {}
        for path in sorted(Path(results_dir).glob("*.phobius.txt")):
            if path.stem == "core":
                continue
            with open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("SEQENCE") or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) < 3:
                        continue
                    seq_id = parts[0].strip()
                    tm = parts[1]
                    sp = parts[2]
                    if tm != "0" or sp == "Y":
                        all_membrane[seq_id] = True
        return all_membrane

    membrane_per_sample = {}
    for path in sorted(Path(results_dir).glob("*.phobius.txt")):
        sample = path.stem.replace(".phobius", "")
        membrane = set()
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("SEQENCE") or line.startswith("#"):
                    continue
                parts = line.split()
                if len(parts) < 3:
                    continue
                seq_id = parts[0].strip()
                tm = parts[1]
                sp = parts[2]
                if tm != "0" or sp == "Y":
                    membrane.add(seq_id)
        membrane_per_sample[sample] = membrane
    return membrane_per_sample


def clean_locus_tag(tag):
    """Clean locus tag for matching with FASTA headers."""
    tag = tag.replace("~~~", "_")
    tag = tag.replace(";", "_")
    tag = tag.replace(":", "_")
    tag = tag.replace(",", "_")
    tag = tag.replace(" ", "_")
    return tag


def parse_psortb_dir(results_dir, core_mode=False):
    """
    Read *.psortb.txt files (terse format):
        SeqID  Score  Localization

    Membrane localizations for gram-negative organisms:
        InnerMembrane, OuterMembrane, Periplasmic

    Args:
        results_dir: Directory containing PSORTb results
        core_mode: If True, aggregate all per-sample results
                  If False, expect per-sample *.psortb.txt files

    Returns:
        If core_mode: dict of {locus_tag: True} with membrane localization
        Else: {sample: set_of_locus_tags_with_membrane_localization}
    """
    membrane_localizations = {"InnerMembrane", "OuterMembrane", "Periplasmic"}

    if core_mode:
        all_membrane = {}
        for path in sorted(Path(results_dir).glob("*.psortb.txt")):
            if path.stem == "core":
                continue
            with open(path) as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("SeqID") or line.startswith("#"):
                        continue
                    parts = line.split("\t")
                    if len(parts) < 3:
                        continue
                    seq_id = clean_locus_tag(parts[0])
                    localization = parts[2].strip()
                    if localization in membrane_localizations:
                        all_membrane[seq_id] = True
        return all_membrane

    membrane_per_sample = {}
    for path in sorted(Path(results_dir).glob("*.psortb.txt")):
        sample = path.stem.replace(".psortb", "")
        membrane = set()
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("SeqID") or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) < 3:
                    continue
                seq_id = parts[0]
                localization = parts[2].strip()
                if localization in membrane_localizations:
                    membrane.add(seq_id)
        membrane_per_sample[sample] = membrane
    return membrane_per_sample


def parse_panaroo_csv(csv_path):
    """
    Parse Panaroo gene_presence_absence.csv.

    Returns:
      core_genes    - {gene_name: {"annotation": str, "sample_tags": {sample: [locus_tags]}}}
                      only for genes present in ALL samples
      sample_names  - ordered list of sample column headers
      total_samples - int
    """
    with open(csv_path, newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader)

    sample_names = header[14:]
    total_samples = len(sample_names)
    sample_start = 14

    core_genes = {}
    with open(csv_path, newline="") as fh:
        reader = csv.reader(fh)
        next(reader)
        for row in reader:
            if len(row) < sample_start + 1:
                continue
            gene_name = row[0]
            annotation = row[2]

            present_count = 0
            for i in range(total_samples):
                cell = row[sample_start + i] if (sample_start + i) < len(row) else ""
                tags = [t.strip() for t in cell.split("\t") if t.strip()]
                if tags:
                    present_count += 1

            if present_count != total_samples:
                continue

            sample_tags = {}
            for i, sample in enumerate(sample_names):
                cell = row[sample_start + i] if (sample_start + i) < len(row) else ""
                tags = [t.strip() for t in cell.split("\t") if t.strip()]
                if tags:
                    sample_tags[sample] = tags

            core_genes[gene_name] = {
                "annotation": annotation,
                "sample_tags": sample_tags,
            }

    return core_genes, sample_names, total_samples


# ---- Main -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Identify core membrane proteins from Phobius and PSORTb results"
    )
    parser.add_argument("--phobius",  required=True, help="Dir with *.phobius.txt files")
    parser.add_argument("--psortb",   required=True, help="Dir with *.psortb.txt files")
    parser.add_argument("--panaroo",  required=True, help="Panaroo gene_presence_absence.csv")
    parser.add_argument("--output",   required=True, help="Output directory")
    parser.add_argument("--core",    action="store_true",
                        help="Use core genome mode: single core.phobius.txt and core PSORTb results")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.core:
        core_genes, sample_names, total_samples = parse_panaroo_csv(args.panaroo)
        print(f"parsing Panaroo core genome ({len(core_genes)} core genes)...")

        phobius_membrane = parse_phobius_dir(args.phobius, core_mode=True)
        print(f"  Phobius membrane proteins: {len(phobius_membrane)}")

        psortb_membrane = parse_psortb_dir(args.psortb, core_mode=True)
        print(f"  PSORTb membrane proteins: {len(psortb_membrane)}")

        rows = []
        for gene_name, gdata in core_genes.items():
            annotation = gdata["annotation"]
            clean_name = clean_gene_name(gene_name)
            phobius_hit = clean_name in phobius_membrane
            psortb_hit = clean_name in psortb_membrane

            rows.append({
                "Gene": gene_name,
                "Annotation": annotation,
                "Phobius_Flag": "Yes" if phobius_hit else "No",
                "PSORTb_Flag": "Yes" if psortb_hit else "No",
                "Consensus": "Yes" if phobius_hit and psortb_hit else "No",
            })

        rows.sort(key=lambda r: (
            r["Consensus"] == "Yes",
            r["Phobius_Flag"] == "Yes",
            r["PSORTb_Flag"] == "Yes"
        ), reverse=True)

        fieldnames = ["Gene", "Annotation", "Phobius_Flag", "PSORTb_Flag", "Consensus"]

        all_path = Path(args.output) / "core_membrane_proteins_all.tsv"
        flagged = [r for r in rows if r["Phobius_Flag"] == "Yes" or r["PSORTb_Flag"] == "Yes"]
        with open(all_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(flagged)

        consensus_path = Path(args.output) / "core_membrane_proteins_consensus.tsv"
        strict = [r for r in rows if r["Consensus"] == "Yes"]
        with open(consensus_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(strict)

        print(f"\nResults:")
        print(f"  Core genes flagged by Phobius only:  {sum(1 for r in rows if r['Phobius_Flag'] == 'Yes')}")
        print(f"  Core genes flagged by PSORTb only:     {sum(1 for r in rows if r['PSORTb_Flag'] == 'Yes')}")
        print(f"  Core genes flagged by either tool:   {len(flagged)}")
        print(f"  Core membrane proteins (consensus):   {len(strict)}")
        print(f"\nOutput files:")
        print(f"  {all_path}")
        print(f"  {consensus_path}")
        return

    print("Parsing Phobius results...")
    phobius = parse_phobius_dir(args.phobius)
    print(f"  {len(phobius)} samples loaded")

    print("Parsing PSORTb results...")
    psortb = parse_psortb_dir(args.psortb)
    print(f"  {len(psortb)} samples loaded")

    print("Parsing Panaroo core genome...")
    core_genes, sample_names, total_samples = parse_panaroo_csv(args.panaroo)
    print(f"  {total_samples} total samples")
    print(f"  {len(core_genes)} core genes identified")

    rows = []
    for gene_name, gdata in core_genes.items():
        annotation   = gdata["annotation"]
        sample_tags  = gdata["sample_tags"]

        phobius_hits = 0
        psortb_hits  = 0
        consensus    = 0

        for sample, tags in sample_tags.items():
            tag_set = set(tags)
            ph = tag_set & phobius.get(sample, set())
            ps = tag_set & psortb.get(sample, set())
            both = ph & ps
            if ph:
                phobius_hits += 1
            if ps:
                psortb_hits += 1
            if both:
                consensus += 1

        rows.append({
            "Gene":               gene_name,
            "Annotation":         annotation,
            "Phobius_Samples":    phobius_hits,
            "PSORTb_Samples":     psortb_hits,
            "Consensus_Samples": consensus,
            "Total_Samples":     total_samples,
            "Phobius_Fraction":  f"{phobius_hits / total_samples:.3f}",
            "PSORTb_Fraction":   f"{psortb_hits / total_samples:.3f}",
            "Consensus_Fraction": f"{consensus / total_samples:.3f}",
        })

    rows.sort(key=lambda r: (r["Consensus_Samples"], r["Phobius_Samples"],
                              r["PSORTb_Samples"]), reverse=True)

    fieldnames = [
        "Gene", "Annotation",
        "Phobius_Samples", "PSORTb_Samples", "Consensus_Samples",
        "Total_Samples", "Phobius_Fraction", "PSORTb_Fraction", "Consensus_Fraction",
    ]

    all_path = Path(args.output) / "core_membrane_proteins_all.tsv"
    flagged = [r for r in rows if r["Phobius_Samples"] > 0 or r["PSORTb_Samples"] > 0]
    with open(all_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(flagged)

    consensus_path = Path(args.output) / "core_membrane_proteins_consensus.tsv"
    strict = [r for r in rows if r["Consensus_Samples"] == total_samples]
    with open(consensus_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(strict)

    print(f"\nResults:")
    print(f"  Core genes flagged by Phobius only:      {sum(1 for r in rows if r['Phobius_Samples'] > 0)}")
    print(f"  Core genes flagged by PSORTb only:       {sum(1 for r in rows if r['PSORTb_Samples'] > 0)}")
    print(f"  Core genes flagged by either tool:       {len(flagged)}")
    print(f"  Core membrane proteins (full consensus): {len(strict)}")
    print(f"\nOutput files:")
    print(f"  {all_path}")
    print(f"  {consensus_path}")


if __name__ == "__main__":
    main()
