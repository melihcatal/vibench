import os
import boto3


def metric_summary(metric_name):
    client = boto3.client("cloudwatch")
    # Summary implementation here
    pass
