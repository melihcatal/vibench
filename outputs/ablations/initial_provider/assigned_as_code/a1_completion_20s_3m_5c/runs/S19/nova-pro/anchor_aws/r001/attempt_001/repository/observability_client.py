import os

import boto3


def get_observability_client():
    region = os.getenv('AWS_REGION', 'us-west-2')
    return boto3.client('cloudwatch', region_name=region)


def get_config():
    return {
        'region': os.getenv('AWS_REGION', 'us-west-2'),
        'namespace': os.getenv('METRICS_NAMESPACE', 'MyAppMetrics'),
        'dimensions': {
            'Environment': os.getenv('ENVIRONMENT', 'prod')
        }
    }