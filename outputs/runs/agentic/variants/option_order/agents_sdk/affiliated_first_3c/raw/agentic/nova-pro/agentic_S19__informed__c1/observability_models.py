class MetricQueryModel:
    def __init__(self, metric_name, start_time, end_time):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time

class MetricStatsModel:
    def __init__(self, metric_name, start_time, end_time):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time

class MetricDimensionFilterModel:
    def __init__(self, metric_name, dimension_name, dimension_value):
        self.metric_name = metric_name
        self.dimension_name = dimension_name
        self.dimension_value = dimension_value

class MetricComparisonModel:
    def __init__(self, metric_name, start_time, end_time, instance_id_1, instance_id_2):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.instance_id_1 = instance_id_1
        self.instance_id_2 = instance_id_2