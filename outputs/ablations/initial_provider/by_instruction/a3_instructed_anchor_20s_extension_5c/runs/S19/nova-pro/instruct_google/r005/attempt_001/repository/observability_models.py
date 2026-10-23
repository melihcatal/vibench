from google.cloud.monitoring_v3 import Aggregation

def normalize_aggregation(aggregation):
    return {
        'alignment_period': aggregation.alignment_period,
        'per_series_aligner': aggregation.per_series_aligner,
    }
