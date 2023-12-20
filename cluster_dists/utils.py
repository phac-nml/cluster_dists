import os
import pandas as pd
from cluster_dists.constants import MIN_FILE_SIZE

def get_file_length(f):
    return int(os.popen(f'wc -l {f}').read().split()[0])

def get_file_header(f):
    return str(os.popen(f'head -n1 {f}').read())

def is_file_ok(f):
    status = True
    if not os.path.isfile(f):
        status = False
    elif get_file_length(f) < 2:
        status = False
    elif os.path.getsize(f) < MIN_FILE_SIZE:
        status = False

    return status


def cluster_membership(sample_id_col,cluster_col,file):
    df = pd.read_csv(file,header=0,delim="\t")
    columns = df.columns.values.tolist()
    if not sample_id_col in columns or cluster_col not in columns:
        return {}
    return dict(zip(df[sample_id_col],df[cluster_col]))
