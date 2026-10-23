import boto3


def archive_metric_snapshot(payload):
    s3 = boto3.client('s3')
    s3.put_object(Bucket='metric-snapshots', Key=payload['filename'], Body=payload['data'])
    return {'status': 'success'}