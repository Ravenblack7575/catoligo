#!/usr/bin/env python3
"""
BlastCheck - Command line tool for analyzing PCR assay BLAST results
Usage: python blastcheck.py <forward_csv> <reverse_csv> <probe_csv> [output_csv]
"""

import pandas as pd
import regex as re
import sys
import os
import argparse

def extract_accession(text):
    """Extract accession number from BLAST result text and normalize"""
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # Try to extract from HYPERLINK formula
    match = re.search(r'HYPERLINK\(".*?","(.*?)"\)', text)
    if match:
        result = match.group(1).strip().upper()
        # print(f"Extracted from HYPERLINK: '{result}' | Original: {text}")
        return result
    # Fallback: extract accession from anywhere in the text
    match2 = re.search(r'[A-Z]{1,3}[_]?\d+\.\d+', text)
    if match2:
        result = match2.group(0).strip().upper()
        # print(f"Extracted from regex: '{result}' | Original: {text}")
        return result
    result = text.strip().upper()
    # print(f"Extracted fallback: '{result}' | Original: {text}")
    return result

def load_and_clean_blast_file(filepath):
    df = pd.read_csv(filepath)
    df.dropna(inplace=True)
    df.columns = df.columns.str.replace(' ','', regex=True).str.lower()
    print(f"Columns in {filepath}: {df.columns.tolist()}")  # Add this for debugging

    if 'accession' not in df.columns:
        raise ValueError(f"'accession' column not found in {filepath}")
    if 'description' not in df.columns:
        print(f"Warning: 'description' column not found in {filepath}")

    df['accession'] = df['accession'].apply(extract_accession).str.strip().str.upper()
    return df

def analyze_blast_results(forward_csv, reverse_csv, probe_csv, output_csv):
    """Main analysis function"""
    print("BlastCheck - PCR Assay BLAST Analysis Tool")
    print("=" * 50)
    
    try:
        # Load and clean all three files
        print(f"Loading forward primer results: {forward_csv}")
        forward_df = load_and_clean_blast_file(forward_csv)
        
        print(f"Loading reverse primer results: {reverse_csv}")
        reverse_df = load_and_clean_blast_file(reverse_csv)
        
        print(f"Loading probe results: {probe_csv}")
        probe_df = load_and_clean_blast_file(probe_csv)
        
        # Get unique accession numbers from each file
        forward_accessions = set(forward_df['accession'].unique())
        reverse_accessions = set(reverse_df['accession'].unique())
        probe_accessions = set(probe_df['accession'].unique())
        
        print(f"\nResults summary:")
        print(f"  Forward primer hits: {len(forward_accessions)}")
        print(f"  Reverse primer hits: {len(reverse_accessions)}")
        print(f"  Probe hits: {len(probe_accessions)}")
        
        # Find accessions that appear in all three sets
        complete_matches = forward_accessions & reverse_accessions & probe_accessions
        print(f"  Complete assay matches: {len(complete_matches)}")
        
        if len(complete_matches) == 0:
            print("\nWarning: No targets found that match all three components!")
            print("Check that your BLAST results contain overlapping targets.")
            return None
        
        # Get descriptions for matched accessions
        results = []
        for accession in complete_matches:
            probe_rows = probe_df[probe_df['accession'] == accession]
            if not probe_rows.empty and 'description' in probe_rows.columns:
                description_row = probe_rows.iloc[0]
                description = description_row['description']
            else:
                description = ""
            results.append({
                'accession_number': accession,
                'description': description
        })
        
        # Create results DataFrame
        results_df = pd.DataFrame(results)
        
        # Save to CSV
        results_df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"\nResults saved to: {output_csv}")
        
        return results_df
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='Analyze PCR assay BLAST results to find complete matches',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python blastcheck.py forward.csv reverse.csv probe.csv
  python blastcheck.py forward.csv reverse.csv probe.csv my_results.csv
  python blastcheck.py -h  (show this help)
        """
    )
    
    parser.add_argument('forward_csv', help='Forward primer BLAST results CSV file')
    parser.add_argument('reverse_csv', help='Reverse primer BLAST results CSV file')
    parser.add_argument('probe_csv', help='Probe BLAST results CSV file')
    parser.add_argument('output_csv', nargs='?', default='assay_targets.csv',
                       help='Output CSV filename (default: assay_targets.csv)')
    
    # Check if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()


        
    # Run the analysis
    results = analyze_blast_results(
        args.forward_csv,
        args.reverse_csv, 
        args.probe_csv,
        args.output_csv
    )
    
    if results is not None:
        print(f"\nSuccess! Found {len(results)} complete matches.")
        print("\nFirst few results:")
        print(results.head().to_string(index=False))

if __name__ == "__main__":
    main()