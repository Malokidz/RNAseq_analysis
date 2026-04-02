import os
import argparse

def calculate_gc_content(sequence):
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100

def parse_fasta_file(filename):
    sequences = {}
    with open(filename, 'r') as file:
        sequence_name = ''
        sequence = ''
        for line in file:
            line = line.strip()
            if line.startswith('>'):
                if sequence_name != '':
                    sequences[sequence_name] = sequence
                sequence_name = line[1:]
                sequence = ''
            else:
                sequence += line
        if sequence_name != '':
            sequences[sequence_name] = sequence
    return sequences

def generate_report(sequences):
    report = []
    for name, sequence in sequences.items():
        length = len(sequence)
        gc_content = calculate_gc_content(sequence)
        report.append((name, length, gc_content))
    return report

def write_report_to_file(report, output_file):
    with open(output_file, 'w') as file:
        file.write("Sequence Name\tLength\tGC Content (%)\n")
        for entry in report:
            file.write("{}\t{}\t{:.2f}\n".format(entry[0], entry[1], entry[2]))

def main():
    parser = argparse.ArgumentParser(description="Calculate GC content of sequences in a FASTA file.")
    parser.add_argument("fasta_file", help="Path to the input FASTA file")
    parser.add_argument("-o", "--output", default="gc_content_report.tsv", help="Path to the output report file")
    args = parser.parse_args()

    fasta_file = args.fasta_file
    output_file = args.output

    sequences = parse_fasta_file(fasta_file)
    report = generate_report(sequences)
    write_report_to_file(report, output_file)
    print(f"Report generated successfully and saved to {output_file}")

if __name__ == "__main__":
    main()
