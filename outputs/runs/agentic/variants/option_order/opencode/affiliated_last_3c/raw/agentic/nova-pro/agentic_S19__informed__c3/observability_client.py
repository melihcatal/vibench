import os
from google.cloud import monitoring_v3

# Set up client
client = monitoring_v3.MetricServiceClient()


# Helper function to get client
def get_client():
    return client


# Helper function to format time
def format_time(timestamp):
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
