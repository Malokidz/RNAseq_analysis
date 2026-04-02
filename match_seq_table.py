import pandas as pd
from Bio import SeqIO
import argparse

def add_sequences_to_table(excel_file, fasta_file, output_file, sheet_name=None, gene_id_col='Gene_ID'):
    """
    Add sequences from FASTA to an Excel table by matching Gene IDs.
    Works with FASTA headers like:
        >BgiBS90_000001-T1 BgiBS90_000001
    where the desired gene ID is the second field (e.g., BgiBS90_000001).
    """

    # Load Excel file
    df = pd.read_excel(excel_file, sheet_name=sheet_name) if sheet_name else pd.read_excel(excel_file)

    # Parse FASTA and extract the second token as the gene ID
    id_to_seq = {}
    with open(fasta_file) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            parts = record.description.split()
            if len(parts) < 2:
                continue  # skip malformed headers

            gene_id = parts[1]        # e.g., BgiBS90_000001
            id_to_seq[gene_id] = str(record.seq)

    # Map sequences to DataFrame
    df['Sequence'] = df[gene_id_col].map(id_to_seq)

    # Report matching statistics
    matched = df['Sequence'].notna().sum()
    total = len(df)
    print(f"Matched {matched}/{total} genes ({matched/total:.2%})")

    # Save result
    df.to_excel(output_file, index=False)
    print(f"Saved updated table to: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Attach FASTA sequences to an Excel table based on Gene IDs.')
    parser.add_argument('excel_file', help='Path to input Excel file')
    parser.add_argument('fasta_file', help='Path to FASTA file')
    parser.add_argument('output_file', help='Path to save updated Excel file')
    parser.add_argument('--sheet', help='Excel sheet name (default: first sheet)')
    parser.add_argument('--id_col', default='Gene_ID', help='Column name containing gene IDs in Excel')

    args = parser.parse_args()

    add_sequences_to_table(
        excel_file=args.excel_file,
        fasta_file=args.fasta_file,
        output_file=args.output_file,
        sheet_name=args.sheet,
        gene_id_col=args.id_col
    )
