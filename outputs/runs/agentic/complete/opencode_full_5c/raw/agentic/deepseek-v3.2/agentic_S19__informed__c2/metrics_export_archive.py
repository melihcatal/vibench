import os
import json
import gzip
import tempfile
from datetime import datetime
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError


class MetricsExportArchiver:
    def __init__(self, bucket_name: Optional[str] = None, region: Optional[str] = None):
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

        if not self.aws_access_key_id or not self.aws_secret_access_key:
            raise ValueError(
                "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
            )

        self.bucket_name = bucket_name or os.environ.get("AWS_S3_BUCKET_NAME")
        if not self.bucket_name:
            raise ValueError(
                "Bucket name must be provided or set in AWS_S3_BUCKET_NAME environment variable"
            )

        self.region = region or os.environ.get("AWS_REGION", "us-east-1")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region,
        )

    def archive_metrics_data(
        self, metrics_data: Dict[str, Any], export_name: str, compress: bool = True
    ) -> Dict[str, Any]:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{export_name}_{timestamp}.json"

        if compress:
            filename += ".gz"

        metadata = {
            "export_name": export_name,
            "export_timestamp": timestamp,
            "data_points": len(metrics_data.get("data", [])),
            "metrics_count": len(metrics_data.get("metrics", [])),
            "compressed": compress,
            "archive_provider": "amazon_s3",
        }

        metrics_data["archive_metadata"] = metadata

        try:
            with tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, suffix=".json"
            ) as tmp_file:
                json_data = json.dumps(metrics_data, default=str).encode("utf-8")

                if compress:
                    json_data = gzip.compress(json_data)

                tmp_file.write(json_data)
                tmp_file.flush()

                object_key = f"metrics-exports/{filename}"

                extra_args = {
                    "ContentType": "application/json",
                    "Metadata": {
                        "export-name": export_name,
                        "export-timestamp": timestamp,
                        "compressed": str(compress),
                    },
                }

                if compress:
                    extra_args["ContentEncoding"] = "gzip"

                self.s3_client.upload_file(
                    tmp_file.name, self.bucket_name, object_key, ExtraArgs=extra_args
                )

                os.unlink(tmp_file.name)

                result = {
                    "success": True,
                    "bucket": self.bucket_name,
                    "object_key": object_key,
                    "filename": filename,
                    "file_size_bytes": len(json_data),
                    "archive_metadata": metadata,
                    "archived_at": datetime.utcnow().isoformat(),
                    "provider": "amazon_s3",
                }

                return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "export_name": export_name,
                "archived_at": datetime.utcnow().isoformat(),
                "provider": "amazon_s3",
            }

    def list_archived_exports(
        self, prefix: str = "metrics-exports/"
    ) -> List[Dict[str, Any]]:
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )

            archives = []
            for obj in response.get("Contents", []):
                archives.append(
                    {
                        "key": obj["Key"],
                        "size_bytes": obj["Size"],
                        "last_modified": obj["LastModified"].isoformat(),
                        "storage_class": obj.get("StorageClass", "STANDARD"),
                    }
                )

            return {
                "success": True,
                "archives": archives,
                "total_count": len(archives),
                "bucket": self.bucket_name,
                "listed_at": datetime.utcnow().isoformat(),
                "provider": "amazon_s3",
            }

        except ClientError as e:
            return {
                "success": False,
                "error": str(e),
                "bucket": self.bucket_name,
                "listed_at": datetime.utcnow().isoformat(),
                "provider": "amazon_s3",
            }

    def retrieve_archived_export(self, object_key: str) -> Dict[str, Any]:
        try:
            with tempfile.NamedTemporaryFile(
                mode="w+b", delete=False, suffix=".json"
            ) as tmp_file:
                self.s3_client.download_file(
                    self.bucket_name, object_key, tmp_file.name
                )

                tmp_file.seek(0)
                file_content = tmp_file.read()

                is_gzipped = object_key.endswith(".gz")

                if is_gzipped:
                    file_content = gzip.decompress(file_content)

                metrics_data = json.loads(file_content.decode("utf-8"))

                os.unlink(tmp_file.name)

                return {
                    "success": True,
                    "object_key": object_key,
                    "metrics_data": metrics_data,
                    "retrieved_at": datetime.utcnow().isoformat(),
                    "provider": "amazon_s3",
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "object_key": object_key,
                "retrieved_at": datetime.utcnow().isoformat(),
                "provider": "amazon_s3",
            }

    def create_export_snapshot(
        self, metrics_data: Dict[str, Any], export_name: str, retention_days: int = 30
    ) -> Dict[str, Any]:
        archive_result = self.archive_metrics_data(
            metrics_data, export_name, compress=True
        )

        if not archive_result.get("success"):
            return archive_result

        try:
            object_key = archive_result["object_key"]

            lifecycle_config = {
                "Rules": [
                    {
                        "ID": f"delete-{export_name}-after-{retention_days}-days",
                        "Status": "Enabled",
                        "Filter": {"Prefix": object_key},
                        "Expiration": {"Days": retention_days},
                    }
                ]
            }

            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=self.bucket_name, LifecycleConfiguration=lifecycle_config
            )

            archive_result["retention_days"] = retention_days
            archive_result["lifecycle_configured"] = True

            return archive_result

        except ClientError as e:
            archive_result["lifecycle_error"] = str(e)
            archive_result["lifecycle_configured"] = False
            return archive_result


if __name__ == "__main__":
    sample_metrics = {
        "metrics": ["cpu_utilization", "memory_usage", "network_throughput"],
        "data": [
            {
                "metric": "cpu_utilization",
                "value": 45.2,
                "timestamp": datetime.utcnow().isoformat(),
            },
            {
                "metric": "memory_usage",
                "value": 67.8,
                "timestamp": datetime.utcnow().isoformat(),
            },
            {
                "metric": "network_throughput",
                "value": 1024,
                "timestamp": datetime.utcnow().isoformat(),
            },
        ],
        "export_config": {"time_range": "last_24_hours", "aggregation": "5min_average"},
    }

    archiver = MetricsExportArchiver(bucket_name="my-metrics-bucket")
    result = archiver.archive_metrics_data(sample_metrics, "daily_metrics_export")
    print(f"Archive result: {result.get('success', False)}")
    if result.get("success"):
        print(f"Archived to: s3://{result['bucket']}/{result['object_key']}")
