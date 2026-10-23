import boto3


class MessagingClient:
    def __init__(self, region_name: str, topic_arn: str = None, queue_url: str = None, dead_letter_queue_url: str = None):
        self.region_name = region_name
        self.topic_arn = topic_arn
        self.queue_url = queue_url
        self.dead_letter_queue_url = dead_letter_queue_url
        self.sns_client = boto3.client("sns", region_name=self.region_name)
        self.sqs_client = boto3.client("sqs", region_name=self.region_name)

    def get_sns_client(self):
        return self.sns_client

    def get_sqs_client(self):
        return self.sqs_client
