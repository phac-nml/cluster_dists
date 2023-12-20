import statistics

class cluster_dist_summary:
    samples_to_cluster = {}
    cluster_metrics = {}
    outliers = {}
    threshold = None
    status = True

    def __init__(self,samples_to_cluster,distance_file,is_matrix,threshold=None):
        self.threshold = threshold
        self.samples_to_cluster = samples_to_cluster
        self.distance_file = distance_file
        self.init_cluster_metrics()

        if is_matrix:
            self.parse_distance_matrix()
        else:
            self.parse_distance_columns()

        self.populate_cluster_metrics()



    def init_cluster_metrics(self):
        for sample_id in self.samples_to_cluster:
            cluster_id = self.samples_to_cluster[sample_id]
            if not cluster_id in self.cluster_metrics:
                self.cluster_metrics[cluster_id] = {
                    'samples':set(),
                    'sample_count':0,
                    'distances':[],
                    'min_dist':None,
                    'ave_dist':None,
                    'med_dist': None,
                    'max_dist':None,
                    'stdev_dist':None,
                    'count_outlier_comparisons':0,
                }
                self.outliers[cluster_id] = {}


    def parse_distance_columns(self):
        with open(self.file_path, 'r') as f:
            next(f)
            for line in f:
                line_split = line.strip().split(self.delim)
                qlabel = line_split[0]
                rlabel = line_split[1]
                if qlabel == rlabel:
                    continue
                qcluster_id = self.samples_to_cluster[qlabel]
                rcluster_id = self.samples_to_cluster[rlabel]
                if qcluster_id == rcluster_id:
                    continue

                # skip reciprocal distances
                if qlabel in self.cluster_metrics['samples'] and rlabel in self.cluster_metrics['samples']:
                    continue

                dist = float(line_split[2])
                if self.threshold != None and dist > self.threshold:
                    if not qlabel in self.outliers[qcluster_id]:
                        self.outliers[qcluster_id][qlabel] = {}
                    self.outliers[qcluster_id][qlabel][rlabel] = dist


                self.cluster_metrics['samples'].add(qlabel)
                self.cluster_metrics['samples'].add(rlabel)
                self.cluster_metrics['distances'].append(dist)


    def parse_distance_matrix(self):
        '''
        Reads in a lower triangle/full distance matrix and splits it into component matricies
        according to the desired number of samples in each batch. Matrix is returned in lower triangle format
        :return:
        '''
        with open(self.file_path, 'r') as f:
            header = next(f).split(self.delim)  # skip header
            samples = header[1:]
            for line in f:
                line_split = line.strip().split(self.delim)
                label = line_split[0]
                distances = list(map(float, line_split[1:]))
                qcluster_id = self.samples_to_cluster[label]
                for idx,value in enumerate(samples):
                    rlabel = header[idx]
                    rcluster_id = self.samples_to_cluster[rlabel]
                    if qcluster_id != rcluster_id or label == rlabel:
                        continue

                    # skip reciprocal distances
                    if label in self.cluster_metrics['samples'] and rlabel in self.cluster_metrics['samples']:
                        continue

                    dist = distances[idx]
                    if self.threshold != None and dist > self.threshold:
                        if not label in self.outliers[qcluster_id]:
                            self.outliers[qcluster_id][label] = {}
                        self.outliers[qcluster_id][label][rlabel] =  dist


                    self.cluster_metrics['samples'].add(label)
                    self.cluster_metrics['samples'].add(rlabel)
                    self.cluster_metrics['distances'].append(dist)


    def populate_cluster_metrics(self):
        for cluster_id in self.cluster_metrics:
            self.cluster_metrics[cluster_id]['sample_count'] = len(self.cluster_metrics[cluster_id]['samples'])
            self.cluster_metrics[cluster_id]['min_dist'] = min(self.cluster_metrics[cluster_id]['distances'])
            self.cluster_metrics[cluster_id]['max_dist'] = max(self.cluster_metrics[cluster_id]['distances'])
            self.cluster_metrics[cluster_id]['med_dist'] = statistics.median(self.cluster_metrics[cluster_id]['distances'])
            self.cluster_metrics[cluster_id]['ave_dist'] = statistics.mean(self.cluster_metrics[cluster_id]['distances'])
            self.cluster_metrics[cluster_id]['stdev_dist'] = statistics.stdev(
                self.cluster_metrics[cluster_id]['distances'])
            self.cluster_metrics[cluster_id]['count_outlier_comparisons'] = self.count_outliers(cluster_id)

    def count_outliers(self,cluster_id):
        for qlabel in self.outliers[cluster_id]:
            if len(self.outliers[cluster_id][qlabel]) == 0:
                return 0
            return len(self.outliers[cluster_id][qlabel]) + 1


    def write_outliers(self,out_file):
        with open(out_file,'w') as fh:
            fh.write(f'cluster_id\tqlabel\trlabel\tdistance\n')
            for cluster_id in self.outliers:
                for qlabel in self.outliers[cluster_id]:
                    for rlabel in self.outliers[cluster_id][qlabel]:
                        dist = self.outliers[cluster_id][qlabel][rlabel]
                        fh.write(f'{cluster_id}\t{qlabel}\t{rlabel}\t{dist}\n')

    def write_cluster_metrics(self,out_file):
        with open(out_file,'w') as fh:
            fh.write(f'cluster_id\tsample_count\tmin_distance\tmax_distance\tmedian_distance\tmean_distance\tstd_deviation\tcount_outlier_comparisons\n')
            for cluster_id in self.cluster_metrics:
                row = [
                    cluster_id,
                    self.cluster_metrics[cluster_id]['sample_count'],self.cluster_metrics[cluster_id]['min_dist'],
                    self.cluster_metrics[cluster_id]['max_dist'], self.cluster_metrics[cluster_id]['med_dist'],
                    self.cluster_metrics[cluster_id]['ave_dist'], self.cluster_metrics[cluster_id]['stdev_dist'],
                    self.cluster_metrics[cluster_id]['count_outlier_comparisons'],
                ]
                fh.write("{}\n".format("\t".join([str(x) for x in row])))





