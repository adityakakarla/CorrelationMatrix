#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from timeit import default_timer as timer
import humanfriendly
import sys
import subprocess

try:
    from cmapPy.pandasGEXpress.parse_gct import parse as parse_gct
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "cmapPy"])
    from cmapPy.pandasGEXpress.parse_gct import parse as parse_gct

from cmapPy.pandasGEXpress.write_gct import write as write_gct
from cmapPy.pandasGEXpress.GCToo import GCToo

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

# Read input GCT file using cmapPy
if args.verbose:
    print(f"Reading {args.input}...")
gct_data = parse_gct(args.input)

if args.verbose:
    print(f"Read input file with {gct_data.data_df.shape[0]} rows and {gct_data.data_df.shape[1]} columns")

# Get the matrix data
matrix_data = gct_data.data_df.values

# Calculate correlation matrix
if args.dimension == "column":
    if args.verbose:
        print(f"Calculating {args.method} correlation between columns...")
    if args.method == "pearson":
        cor_matrix = np.corrcoef(matrix_data.T)
    else:  # for spearman or kendall
        cor_matrix = pd.DataFrame(matrix_data).corr(method=args.method).values
    col_names = gct_data.data_df.columns
    row_names = col_names
elif args.dimension == "row":
    if args.verbose:
        print(f"Calculating {args.method} correlation between rows...")
    if args.method == "pearson":
        cor_matrix = np.corrcoef(matrix_data)
    else:  # for spearman or kendall
        cor_matrix = pd.DataFrame(matrix_data.T).corr(method=args.method).values
    row_names = gct_data.data_df.index
    col_names = row_names
else:
    raise ValueError("Invalid dimension specified. Use 'column' or 'row'")

# Create a pandas DataFrame with the correlation matrix
cor_df = pd.DataFrame(cor_matrix, index=row_names, columns=col_names)

# Create row metadata for GCToo (includes id and description)
row_metadata_df = pd.DataFrame(index=row_names)
row_metadata_df['id'] = row_names
row_metadata_df['description'] = row_names

# Create column metadata for GCToo
col_metadata_df = pd.DataFrame(index=col_names)
col_metadata_df['id'] = col_names
col_metadata_df['description'] = col_names

# Create a GCToo object
result_gct = GCToo(data_df=cor_df, 
                  row_metadata_df=row_metadata_df,
                  col_metadata_df=col_metadata_df)

# Write the GCT file using cmapPy
if args.verbose:
    print(f"Writing output to output.gct...")
write_gct(result_gct, 'output.gct')

if args.verbose:
    print(f"Generated correlation matrix with {cor_df.shape[0]} rows and {cor_df.shape[1]} columns")
    print(f"Output written to output.gct")

end_of_time = timer()
print("We are done! Wall time elapsed:", humanfriendly.format_timespan(end_of_time - beginning_of_time))