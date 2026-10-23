import boto3


def get_client(service_name):
    return boto3.client(service_name)


def configure_logging(log_group_name, log_stream_name):
    return log_group_name, log_stream_name
