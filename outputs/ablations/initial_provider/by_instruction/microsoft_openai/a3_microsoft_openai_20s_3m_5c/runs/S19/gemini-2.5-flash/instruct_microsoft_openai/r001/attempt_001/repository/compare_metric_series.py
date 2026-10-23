import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from observability_client import AWSCloudWatchMetricsClient
from observability_models import MetricQueryRequest

def compare_metric_series(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    dimensions_filter1: Dict[str, str],
    dimensions_filter2: Dict[str, str],
    region_name: str,
    interval: Optional[str] = "PT5M"
) -> Dict[str, Any]:
    """
    Compares metric values for two resources or dimension filters over the same window using AWS CloudWatch.

    Args:
        metric_name: The name of the metric to compare (e.g., "CPUUtilization").
        start_time: The start of the time window.
        end_time: The end of the time window.
        dimensions_filter1: A dictionary of dimension names and values for the first series.
        dimensions_filter2: A dictionary of dimension names and values for the second series.
        region_name: The AWS region to query CloudWatch in.
        interval: The aggregation interval (e.g., 'PT5M' for 5 minutes).

    Returns:
        A dictionary containing the comparison results.
    """
    client = AWSCloudWatchMetricsClient(region_name=region_name)
    
    request1 = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions_filter=dimensions_filter1,
        interval=interval
    )
    
    request2 = MetricQueryRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions_filter=dimensions_filter2,
        interval=interval
    )
    
    response = client.compare_metric_series(request1, request2)
    return response

if __name__ == '__main__':
    # Example usage (requires AWS_REGION environment variable to be set and AWS credentials configured)
    # Replace with your actual metric name, dimensions, and time window.
    # Ensure the metric and dimensions exist in your CloudWatch environment.

    aws_region_example = os.environ.get("AWS_REGION")
    
    end_time_example = datetime.utcnow()
    start_time_example = end_time_example - timedelta(hours=1)
    
    # Example: Compare CPUUtilization for two EC2 instances
    example_metric_name = "CPUUtilization"
    example_dimensions_filter1 = {"InstanceId": "i-0abcdef1234567890"}
    example_dimensions_filter2 = {"InstanceId": "i-0fedcba9876543210"}

    if aws_region_example:
        print(f"Comparing metric '{example_metric_name}' in {aws_region_example} between")
        print(f"  Series 1 (dimensions: {example_dimensions_filter1})")
        print(f"  and Series 2 (dimensions: {example_dimensions_filter2})")
        print(f"  from {start_time_example} to {end_time_example}")
        
        try:
            comparison_data = compare_metric_series(
                metric_name=example_metric_name,
                start_time=start_time_example,
                end_time=end_time_example,
                dimensions_filter1=example_dimensions_filter1,
                dimensions_filter2=example_dimensions_filter2,
                region_name=aws_region_example,
                interval="PT1M"
            )

            print("\nMetric Series Comparison:")
            print(json.dumps(comparison_data, indent=2, default=str))

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    else:
        print("Please set AWS_REGION environment variable for example usage.")
