class PublishRequest:
    def __init__(self, topic_arn, message):
        self.topic_arn = topic_arn
        self.message = message

class PublishBatchRequest:
    def __init__(self, topic_arn, messages):
        self.topic_arn = topic_arn
        self.messages = messages

class ConsumeRequest:
    def __init__(self, queue_url):
        self.queue_url = queue_url

class DeadLetterRequest:
    def __init__(self, queue_url, message):
        self.queue_url = queue_url
        self.message = message