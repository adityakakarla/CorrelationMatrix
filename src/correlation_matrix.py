#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from timeit import default_timer as timer
import humanfriendly
import sys
import subprocess

try:
    from gp.data import GCT, write_gct
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "genepattern-python"])
    from gp.data import GCT, write_gct

beginning_of_time = timer()

parser = argparse.ArgumentParser()
# ~~~~Module Required Arguments~~~~~ #
parser.add_argument("-i", "--input",
                    type=str,
                    required=True,
                    help="Input GCT file path")
parser.add_argument("-m", "--method",
                    type=str,
                    default="pearson",
                    choices=["pearson", "spearman", "kendall"],
                    help="Correlation method: 'pearson', 'spearman', or 'kendall' [default: pearson]")
parser.add_argument("-d", "--dimension",
                    type=str,
                    default="column",
                    choices=["column", "row"],
                    help="Dimension to correlate: 'column' or 'row' [default: column]")
# ~~~~Development Optional Arguments~~~~~ #
parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="increase output verbosity")
parser.add_argument("--debug",
                    action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

if args.verbose:
    print("Starting correlation matrix calculation...")
    print("~~~~~~~~~~~~~~~~~~~~~~")
    print("Using arguments:")
    print(args)
    print("Now getting work done.")
    print("~~~~~~~~~~~~~~~~~~~~~~")

# Read input GCT file using genepattern-python
if args.verbose:
    print(f"Reading {args.input}...")
gct_data = GCT(args.input)

if args.verbose:
    print(f"Read input file with {gct_data.shape[0]} rows and {gct_data.shape[1]} columns")

# Calculate correlation matrix
if args.dimension == "column":
    matrix_data = gct_data.values
    if args.verbose:
        print(f"Calculating {args.method} correlation between columns...")
    if args.method == "pearson":
        cor_matrix = np.corrcoef(matrix_data.T)
    else:  # for spearman or kendall
        cor_matrix = pd.DataFrame(matrix_data).corr(method=args.method).values
    col_names = gct_data.columns
    row_names = col_names
    cor_df = pd.DataFrame(cor_matrix, index=row_names, columns=col_names)
    cor_df['Description'] = None
    cor_df = cor_df.reset_index(drop=False)
    cor_df['Name'] = cor_df['index']
    cor_df = cor_df.set_index(['Name','Description']).drop(columns=['index'])
elif args.dimension == "row":
    modified_df = gct_data.reset_index(drop=False).drop(columns=['Description']).set_index('Name')
    matrix_data = modified_df.values
    if args.verbose:
        print(f"Calculating {args.method} correlation between rows...")
    if args.method == "pearson":
        cor_matrix = np.corrcoef(matrix_data)
    else:  # for spearman or kendall
        cor_matrix = pd.DataFrame(matrix_data.T).corr(method=args.method).values
    row_names = modified_df.index
    col_names = row_names
    cor_df = pd.DataFrame(cor_matrix, index=row_names, columns=col_names)
    cor_df['Description'] = None
    cor_df = cor_df.reset_index(drop=False).set_index(['Name','Description'])
else:
    raise ValueError("Invalid dimension specified. Use 'column' or 'row'")

# Write the GCT file using genepattern-python
if args.verbose:
    print(f"Writing output to output.gct...")

write_gct(cor_df, file_path='./output.gct')

if args.verbose:
    print(f"Generated correlation matrix with {cor_df.shape[0]} rows and {cor_df.shape[1]} columns")
    print(f"Output written to output.gct")

end_of_time = timer()
print("We are done! Wall time elapsed:", humanfriendly.format_timespan(end_of_time - beginning_of_time))