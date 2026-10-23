import os
import re
from observability_client import CloudWatchClient
from observability_models import MetricFilterRequest

# Example unsafe patterns list - can be expanded
UNSAFE_PATTERNS = [
    r'password',
    r'key',
    r'secret',
    r'token',
    r'credential',
    r'http://',
    r'https://',
    r'ftp://',
]

# Combine patterns into a single regex for efficiency
PATTERN = re.compile('|'.join(UNSAFE_PATTERNS), re.IGNORECASE)


def metric_annotation_safety(metric_name: str, start_time: str, end_time: str, dimensions: List[dict], region: str = None):
    """Check free-text metric labels or annotations (dimensions) for unsafe text using a simple regex filter.

    Returns True if any dimension value contains unsafe content, False otherwise.
    """
    region = region or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    client = CloudWatchClient(region=region)
    # Retrieve metric metadata to inspect dimension values (placeholder)
    # CloudWatch DescribeMetric call would be used in real scenario
    response = client.get_metric_metadata(metric_name=metric_name, dimensions=dimensions)
    # response mock: assuming dimensions return in the same structure as request
    for dim in response.get('Dimensions', []):
        value = dim.get('Value', '')
        if PATTERN.search(value):
            return True
    return False
