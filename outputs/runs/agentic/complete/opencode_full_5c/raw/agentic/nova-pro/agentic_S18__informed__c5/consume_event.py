import boto3

# Create an SQS client
sqs = boto3.client("sqs")

# Set the name of the queue
queue_url = "your-queue-url"

# Receive message from SQS queue
response = sqs.receive_message(
    QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=0
)

# Get the message
message = response["Messages"][0]

# Print out the body
print(message["Body"])

# Delete received message from queue
sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
