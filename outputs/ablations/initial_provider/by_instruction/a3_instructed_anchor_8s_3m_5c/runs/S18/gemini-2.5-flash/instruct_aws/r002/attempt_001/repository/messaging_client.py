import os
import boto3

def get_sns_topic_arn():
    """
    Retrieves the AWS SNS Topic ARN from environment variables.
    """
    topic_arn = os.environ.get("AWS_SNS_TOPIC_ARN")
    if not topic_arn:
        raise ValueError("AWS_SNS_TOPIC_ARN environment variable not set.")
    return topic_arn

def get_sqs_queue_url():
    """
    Retrieves the AWS SQS Queue URL from environment variables.
    """
    queue_url = os.environ.get("AWS_SQS_QUEUE_URL")
    if not queue_url:
        raise ValueError("AWS_SQS_QUEUE_URL environment variable not set.")
    return queue_url

def get_sqs_dead_letter_queue_url():
    """
    Retrieves the AWS SQS Dead-Letter Queue URL from environment variables.
    """
    dlq_url = os.environ.get("AWS_SQS_DEAD_LETTER_QUEUE_URL")
    if not dlq_url:
        raise ValueError("AWS_SQS_DEAD_LETTER_QUEUE_URL environment variable not set.")
    return dlq_url

def get_sagemaker_endpoint_name():
    """
    Retrieves the AWS SageMaker endpoint name from environment variables.
    """
    endpoint_name = os.environ.get("AWS_SAGEMAKER_ENDPOINT_NAME")
    if not endpoint_name:
        raise ValueError("AWS_SAGEMAKER_ENDPOINT_NAME environment variable not set.")
    return endpoint_name

def get_translate_client():
    """
    Returns an AWS Translate client.
    """
    return boto3.client('translate')

def get_comprehend_client():
    """
    Returns an AWS Comprehend client.
    """
    return boto3.client('comprehend')

def get_dynamodb_table_name():
    """
    Retrieves the AWS DynamoDB table name from environment variables.
    """
    table_name = os.environ.get("AWS_DYNAMODB_TABLE_NAME")
    if not table_name:
        raise ValueError("AWS_DYNAMODB_TABLE_NAME environment variable not set.")
    return table_name

def get_dynamodb_client():
    """
    Returns an AWS DynamoDB client.
    """
    return boto3.client('dynamodb')
