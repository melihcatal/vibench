import boto3
import json
from datetime import datetime
from observability_models import MetricsExportRequest, MetricsExportResponse


def export_metrics_to_archive(request: MetricsExportRequest) -> MetricsExportResponse:
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    # Simulated metric data export
    export_data = {
        "metrics": request.metric_names,
        "window_hours": request.window_hours,
        "data": [
            {"metric": metric, "timestamp": datetime.utcnow().isoformat(), "value": 42.0}
            for metric in request.metric_names
        ]
    }
    
    export_key = f"metrics_export/{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.{request.export_format}"
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME", "metrics-archive-bucket")
    
    s3_client.put_object(
        Bucket=bucket_name,
        Key=export_key,
        Body=json.dumps(export_data).encode()
    )
    
    return MetricsExportResponse(
        archive_path=f"s3://{bucket_name}/{export_key}"
    )