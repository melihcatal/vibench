import os

from google.cloud import monitoring_v3


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def format_time_interval(start_time, end_time):
    return monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
