from google.cloud import monitoring_v3

def create_time_interval(start_time, end_time):
    return monitoring_v3.types.TimeInterval(start_time=start_time, end_time=end_time)

def create_aggregation(alignment_period, per_series_aligner, cross_series_reducer, group_by_fields):
    return monitoring_v3.types.Aggregation(
        alignment_period=monitoring_v3.types.Duration(seconds=alignment_period),
        per_series_aligner=per_series_aligner,
        cross_series_reducer=cross_series_reducer,
        group_by_fields=group_by_fields)