import boto3
from observability_client import cw_client
from observability_models import MetricData


def metric_summary(metric_name: str, start_time: str, end_time: str, period: int):
    datapoints = query_metric_window(metric_name, start_time, end_time, period)
    if not datapoints:
        return "No data available"
    average_values = [dp.value for dp in datapoints]
    trend = "increasing" if average_values[-1] > average_values[0] else "decreasing"
    return f"Trend: {trend}, Average: {sum(average_values) / len(average_values)}"
