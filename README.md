[![PyPI](https://img.shields.io/badge/Install%20with-PyPI-blue)](https://pypi.org/project/cluster_dists/#description)
[![Bioconda](https://img.shields.io/badge/Install%20with-bioconda-green)](https://anaconda.org/bioconda/cluster_dists)
[![Conda](https://img.shields.io/conda/dn/bioconda/cluster_dists?color=green)](https://anaconda.org/bioconda/cluster_dists)
[![License: Apache-2.0](https://img.shields.io/github/license/phac-nml/cluster_dists)](https://www.apache.org/licenses/LICENSE-2.0)


## Profile Dists

## Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Quick Start](#quick-start)
- [FAQ](#faq)
- [Citation](#citation)
- [Legal](#legal)
- [Contact](#contact)

## Introduction

Aggolomerative clustering will distort the underlying pairwise distances of samples and it is often desireable from an opperational perspective
to know the actual pair wise distance characteristics of a given grouping.
To address needs of users within our team we have designed a solution for summarizing the pairwise distance characteristics of a group of samples.
The tool is designed with outbreak clusters in mind but the labels used as input can be any text label and could summarize the genetic distances
within any categorical metadata label such as geography or host. 


## Installation

Install the latest released version from conda:

        conda create -c bioconda -c conda-forge -n cluster_dists cluster_dists

Install using pip:

        pip install cluster_dists

Install the latest master branch version directly from Github:

        pip install git+https://github.com/phac-nml/cluster_dists.git



## Usage
If you run ``cluster_dists``, you should see the following usage statement:

    usage: main.py [-h] -d DISTS -b FORMAT -m METADATA --outdir OUTDIR
               [--outlier_threshold OUTLIER_THRESHOLD] --sample_column
               SAMPLE_COLUMN --label_column LABEL_COLUMN [--force] [-V]
 


## FAQ

Coming soon

## Citation

Robertson, James, Wells, Matthew, Schonfeld, Justin, Reimer, Aleisha. Cluster Dists: Summarizing pairwise distances within categorical groupings. 2023. https://github.com/phac-nml/cluster_dists

## Legal

Copyright Government of Canada 2023

Written by: National Microbiology Laboratory, Public Health Agency of Canada

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.


## Contact

**James Robertson**: james.robertson@phac-aspc.gc.ca
