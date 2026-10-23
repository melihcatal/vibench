from azure.servicebus import ServiceBusClient
from messaging_models import ServiceBusConfig

class MessagingClient:
    def __init__(self, config: ServiceBusConfig):
        self.config = config
        self._client = None

    def _get_client(self):
        if self._client is None:
            self._client = ServiceBusClient.from_connection_string(self.config.connection_string)
        return self._client

    def get_topic_sender(self):
        if not self.config.topic_name:
            raise ValueError("Topic name must be provided in config for a sender.")
        return self._get_client().get_topic_sender(topic_name=self.config.topic_name)

    def get_queue_sender(self):
        if not self.config.queue_name:
            raise ValueError("Queue name must be provided in config for a sender.")
        return self._get_client().get_queue_sender(queue_name=self.config.queue_name)

    def get_subscription_receiver(self):
        if not self.config.topic_name or not self.config.subscription_name:
            raise ValueError("Topic name and subscription name must be provided in config for a receiver.")
        return self._get_client().get_subscription_receiver(topic_name=self.config.topic_name,
                                                           subscription_name=self.config.subscription_name)

    def get_queue_receiver(self):
        if not self.config.queue_name:
            raise ValueError("Queue name must be provided in config for a receiver.")
        return self._get_client().get_queue_receiver(queue_name=self.config.queue_name)

    def get_dead_letter_queue_sender(self):
        if not self.config.dead_letter_queue_name:
            raise ValueError("Dead letter queue name must be provided in config for a dead-letter sender.")
        return self._get_client().get_queue_sender(queue_name=self.config.dead_letter_queue_name)

    def close(self):
        if self._client:
            self._client.close()

