#!/bin/bash

# File containing the list of FASTA file names to concatenate and remove
list_file="fasta_file_names.txt"

# Output FASTA file
output_file="concatenated_sequences.fasta"

# Loop through each file name in the list file
while IFS= read -r fasta_file; do
    # Check if the file exists
    if [ -f "$fasta_file" ]; then
        # Print the name of the file
        echo "### $fasta_file ###"
        # Append the content of the file (including header lines starting with '>') to the output file
        cat "$fasta_file" >> "$output_file"
        echo "File $fasta_file concatenated."
        # Remove the file
        rm "$fasta_file"
        echo "File $fasta_file removed."
    else
        echo "File $fasta_file does not exist."
    fi
done < "$list_file"
