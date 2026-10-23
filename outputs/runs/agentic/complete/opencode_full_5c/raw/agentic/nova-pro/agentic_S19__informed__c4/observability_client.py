import os

from google.cloud import monitoring_v3


def create_client():
    return monitoring_v3.MetricServiceClient()
