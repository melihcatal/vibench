import os

AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN')
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL')
SQS_DLQ_URL = os.getenv('SQS_DLQ_URL')
