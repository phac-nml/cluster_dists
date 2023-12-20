import sys
from argparse import (ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter)
import json
import os
from datetime import datetime
from cluster_dists.version import __version__
from cluster_dists.utils import is_file_ok, cluster_membership, get_file_header
from cluster_dists.classes.clusters import cluster_dist_summary
from cluster_dists.constants import RUN_DATA


def parse_args():
    """ Argument Parsing method.

        A function to parse the command line arguments passed at initialization of Cluster dists,
        format these arguments,  and return help prompts to the user shell when specified.

        Returns
        -------
        ArgumentParser object
            The arguments and their user specifications, the usage help prompts and the correct formatting
            for the incoming argument (str, int, etc.)
        """
    class CustomFormatter(ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter):
        """
                Class to instantiate the formatter classes required for the argument parser.
                Required for the correct formatting of the default parser values

                Parameters
                ----------
                ArgumentDefaultsHelpFormatter object
                    Instatiates the default values for the ArgumentParser for display on the command line.
                RawDescriptionHelpFormatter object
                    Ensures the correct display of the default values for the ArgumentParser
                """
        pass

    parser = ArgumentParser(
        description="Cluster Dists: Summarize genetic distances by label v. {}".format(__version__),
        formatter_class=CustomFormatter)
    parser.add_argument('-d', '--dists', type=str, required=True,
                        help='Three column file [query_id,ref_id,dist] or square distance matrix')
    parser.add_argument('-f', '--format', type=str, required=True,
                        help='"pairwise" or "matrix" format')
    parser.add_argument('-m', '--metadata', type=str, required=True,
                        help='Metadata file which contains labels for aggregation')
    parser.add_argument('--outdir', '-o', type=str, required=True, help='Result output files')
    parser.add_argument('--outlier_threshold', '-t', type=float, required=False,
                        help='Flag pairwise comparisons above this threshold (integer or float)',default=None)
    parser.add_argument('--sample_column','-s', required=True, help='Name of column with sample id label',
                        default=None)
    parser.add_argument('--label_column','-c', required=True, help='Name of column with label for aggregating',
                        default=None)
    parser.add_argument('--force','-f', required=False, help='Overwrite existing directory',
                        action='store_true')
    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + __version__)

    return parser.parse_args()




def main():
    cmd_args = parse_args()
    dist_file = cmd_args.dists
    metadata_file = cmd_args.metadata
    outdir = cmd_args.outdir
    threshold = cmd_args.outlier_threshold
    sample_column = cmd_args.sample_column
    label_column = cmd_args.label_column
    force = cmd_args.force
    format = cmd_args.format

    if format not in ['pairwise','matrix']:
        print(f'Error format:{format} must be "pairwise" or "matrix"')
        sys.exit()

    if not is_file_ok(dist_file):
        print(f'Error {dist_file} does not exist or is empty')
        sys.exit()

    if not is_file_ok(metadata_file):
        print(f'Error {metadata_file} does not exist or is empty')
        sys.exit()

    if os.path.isdir(outdir) and not force:
        print(f'Error {outdir} exists, if you would like to overwrite, then specify --force')
        sys.exit()

    if not os.path.isdir(outdir):
        os.makedirs(outdir, 0o755)

    run_data = RUN_DATA
    run_data['analysis_start_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    run_data['parameters'] = vars(cmd_args)
    outlier_report = os.path.join(outdir,"outliers.txt")
    summary_report = os.path.join(outdir, "cluster_summary.txt")
    run_data['outlier_file'] = outlier_report
    run_data['summary_file'] = summary_report

    h = get_file_header(metadata_file).split("\t")
    if not sample_column in h:
        print(f'Error sample id column {sample_column} is not in the {metadata_file} header')
        sys.exit()

    if not label_column in h:
        print(f'Error label column {label_column} is not in the {metadata_file} header')
        sys.exit()

    samples_to_cluster = cluster_membership(sample_column,label_column,metadata_file)
    is_matrix = False
    if format == 'matrix':
        is_matrix = True

    obj = cluster_dist_summary(samples_to_cluster,dist_file,is_matrix,threshold)
    run_data['status'] = obj.status
    obj.write_outliers(outlier_report)
    obj.write_cluster_metrics(summary_report)
    run_data['analysis_end_time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


    with open(os.path.join(outdir,"run.json"),'w' ) as fh:
        fh.write(json.dumps(run_data, indent=4))

    sys.stdout.flush()


