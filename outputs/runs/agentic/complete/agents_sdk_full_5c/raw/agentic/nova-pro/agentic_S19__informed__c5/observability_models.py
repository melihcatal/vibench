from google.cloud import monitoring_v3

def create_time_interval(start_time, end_time):
    return monitoring_v3.types.TimeInterval(start_time=start_time, end_time=end_time)

def create_aggregation():
    return monitoring_v3.types.Aggregation(per_series_aligner=monitoring_v3.enums.AggregationAlignment(value='ALIGN_MEAN'))