import os
from datetime import datetime
from typing import Dict, List
from observability_client import ObservabilityClient
from observability_models import MetricDimensionFilterResponse

def query_metric_data_filtered_by_dimensions(
    namespace: str,
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Dict[str, str]
) -> MetricDimensionFilterResponse:
    """
    Queries metric data filtered by resource labels or dimensions using Amazon CloudWatch.
    """
    aws_region = os.environ.get("AWS_REGION")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not all([aws_region, aws_access_key_id, aws_secret_access_key]):
        raise ValueError("AWS_REGION, AWS_ACCESS_KEY_ID, and AWS_SECRET_ACCESS_KEY environment variables must be set.")

    # OpenAI API Key is not directly used for this file but passed for client initialization consistency.
    dummy_openai_api_key = os.environ.get("OPENAI_API_KEY", "dummy_key") 

    client = ObservabilityClient(
        openai_api_key=dummy_openai_api_key,
        aws_region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    filter_response = client.get_cloudwatch_filtered_metric_dimensions(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=dimensions
    )
    return filter_response
