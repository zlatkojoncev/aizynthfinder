import pandas as pd
import subprocess
import sys

def run_aizynthcli_for_smiles(smiles, config_path, idx):
    # Create a temporary file for the single SMILES
    with open('temp_smiles.txt', 'w') as f:
        f.write(smiles)
    
    # Create a unique output filename for each SMILES processed
    output_filename = f"output_{idx}.json.gz"
    
    # Construct the command with the output parameter
    command = [
        'aizynthcli',
        '--smiles', 'temp_smiles.txt',
        '--config', config_path,
        '--policy', 'multi_expansion_strategy',
        '--output', output_filename
    ]
    
    # Run the command
    try:
        subprocess.run(command, check=True)
        print(f"Successfully processed SMILES: {smiles}, output: {output_filename}")
    except subprocess.CalledProcessError as e:
        print(f"Error processing SMILES: {smiles}")
        print(f"Error: {e}")

def main():
    csv_file = sys.argv[1]
    config_path = sys.argv[2]
    
    # Read the CSV file without headers and get first column
    try:
        df = pd.read_csv(csv_file, header=None)
        smiles_list = df[0]  # Get first column
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
    
    # Process each SMILES
    total = len(smiles_list)
    for idx, smiles in enumerate(smiles_list, start=1):
        print(f"Processing molecule {idx}/{total}")
        run_aizynthcli_for_smiles(smiles, config_path, idx)

if __name__ == "__main__":
    main()