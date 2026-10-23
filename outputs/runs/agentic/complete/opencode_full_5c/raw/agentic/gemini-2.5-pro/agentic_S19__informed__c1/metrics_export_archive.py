import os
import json
import boto3
from botocore.exceptions import ClientError
from typing import List
from observability_models import MetricSeries


def archive_metrics_to_s3(
    series_data: List[MetricSeries], bucket_name: str, object_name: str
) -> bool:
    s3_client = boto3.client("s3")

    data_to_serialize = [
        {
            "metric_name": s.metric_name,
            "tags": s.tags,
            "points": [{"timestamp": p.timestamp, "value": p.value} for p in s.points],
        }
        for s in series_data
    ]

    json_data = json.dumps(data_to_serialize, indent=2)

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=json_data,
            ContentType="application/json",
        )
        return True
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
