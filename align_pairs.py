import csv
import os
import subprocess
import argparse

# Define the command-line argument parser
parser = argparse.ArgumentParser(description="Align pairs of sequences from a FASTA file.")
parser.add_argument('-f', '--fasta_file', required=True, help='Path to the FASTA file.')
parser.add_argument('-p', '--pairs_file', help='Path to the CSV file containing sequence pairs.')
parser.add_argument('-o', '--output_dir', required=True, help='Directory to save the aligned sequences.')
parser.add_argument('--id1', help='First sequence ID to align.')
parser.add_argument('--id2', help='Second sequence ID to align.')

# Parse the command-line arguments
args = parser.parse_args()

# Assign arguments to variables
fasta_file = args.fasta_file
pairs_file = args.pairs_file
output_dir = args.output_dir
id1 = args.id1
id2 = args.id2

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to extract and align sequences
def extract_and_align(seq1_id, seq2_id, fasta_file, output_dir):
    # Create a temporary file with the sequence IDs
    temp_ids_file = 'temp_ids.txt'
    with open(temp_ids_file, 'w') as temp_file:
        temp_file.write(f"{seq1_id}\n")
        temp_file.write(f"{seq2_id}\n")

    # Extract the sequences using seqtk
    extracted_fasta = f"{output_dir}/{seq1_id}_{seq2_id}_extracted.fa"
    with open(extracted_fasta, 'w') as out_fasta:
        subprocess.run(['seqtk', 'subseq', fasta_file, temp_ids_file], stdout=out_fasta)

    # Align the sequences using MAFFT
    aligned_output = f"{output_dir}/{seq1_id}_{seq2_id}_aligned.aln"
    subprocess.run(['mafft', '--auto', '--quiet', '--clustalout', extracted_fasta], stdout=open(aligned_output, 'w'))

    # Remove the temporary extracted fasta file
    os.remove(extracted_fasta)

# Process command-line sequence IDs if provided
if id1 and id2:
    extract_and_align(id1, id2, fasta_file, output_dir)
# Otherwise, process pairs from the pairs file
elif pairs_file:
    # Read the pairs file and process each pair
    with open(pairs_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            seq1_id, seq2_id = row
            extract_and_align(seq1_id, seq2_id, fasta_file, output_dir)
else:
    raise ValueError("Either --id1 and --id2 or --pairs_file must be provided.")

# Clean up temporary files
if os.path.exists('temp_ids.txt'):
    os.remove('temp_ids.txt')



