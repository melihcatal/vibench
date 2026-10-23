import boto3


def get_config():
    return {
        'region': 'us-west-2',
        'log_group': 'my-log-group',
        'log_stream': 'my-log-stream',
    }