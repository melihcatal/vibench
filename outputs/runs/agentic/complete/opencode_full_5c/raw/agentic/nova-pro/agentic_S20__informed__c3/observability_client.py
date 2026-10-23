import boto3


def create_logs_client():
    return boto3.client("logs")


def normalize_log_event(log_event):
    return {"timestamp": log_event["timestamp"], "message": log_event["message"]}
