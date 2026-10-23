import os
from google.cloud import monitoring_v3
from google.cloud import storage


def export_metrics(project_id):
    client = monitoring_v3.MetricServiceClient()
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f'projects/{project_id}',
        filter='metric.type="compute.googleapis.com/instance/cpu/utilization"'
    )
    time_series = client.list_time_series(request=request)
    for ts in time_series:
        print(ts)


def archive_metrics(bucket_name, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    blob.upload_from_string('Metric data')


if __name__ == '__main__':
    project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
    bucket_name = 'your-bucket-name'
    file_name = 'metrics.txt'
    export_metrics(project_id)
    archive_metrics(bucket_name, file_name)