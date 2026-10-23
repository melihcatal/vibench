from typing import Dict, List, Optional
import os
from datetime import datetime
import boto3
from openai import OpenAI
from observability_models import MetricDatapoint, normalize_metric_response


def metric_summary(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    dimensions: Optional[List[Dict[str, str]]] = None,
    region: str = "us-east-1"
) -> str:
    """
    Summarize recent metric trends or anomalies using Amazon CloudWatch Metrics and OpenAI GPT.
    
    Args:
        metric_name: Name of the CloudWatch metric to query.
        namespace: Namespace of the CloudWatch metric.
        start_time: Start of the time window.
        end_time: End of the time window.
        dimensions: Optional list of dimension dictionaries.
        region: AWS region where the metric is stored.
        
    Returns:
        Summary of metric trends or anomalies as a string.
    """
    if dimensions is None:
        dimensions = []
    
    # Query metric data from CloudWatch
    cloudwatch = boto3.client(
        "cloudwatch",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=int((end_time - start_time).total_seconds()),
        Statistics=["Average", "Sum", "Minimum", "Maximum"]
    )
    
    datapoints = normalize_metric_response(response)
    
    # Prepare prompt for OpenAI GPT
    prompt = (
        f"Summarize the following metric datapoints for {metric_name} in the {namespace} namespace:\n"
        f"Datapoints: {[{\"timestamp\": dp.timestamp.isoformat(), \"value\": dp.value} for dp in datapoints]}\n"
        "Provide a concise summary of trends, anomalies, or notable patterns in 2-3 sentences."
    )
    
    # Generate summary using OpenAI GPT
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes metric data."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"Failed to generate metric summary: {e}")