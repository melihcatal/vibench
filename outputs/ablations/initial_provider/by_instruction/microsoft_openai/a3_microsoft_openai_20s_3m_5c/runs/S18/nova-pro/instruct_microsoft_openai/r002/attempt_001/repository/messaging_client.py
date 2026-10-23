import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

class MessagingClient:
    def __init__(self):
        self.client = openai.Client()

    def publish(self, event):
        return self.client.publish(event)

    def consume(self):
        return self.client.consume()

    def dead_letter(self, message):
        self.client.dead_letter(message)

    def batch_publish(self, messages):
        return self.client.batch_publish(messages)