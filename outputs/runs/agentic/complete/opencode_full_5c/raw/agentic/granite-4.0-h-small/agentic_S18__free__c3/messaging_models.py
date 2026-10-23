import os

# [HELPER] messaging_models.py
# Local models and normalization helpers for Pub/Sub integration


class Message:
    """Normalization of incoming message body."""

    def __init__(self, raw_body: dict):
        self.raw = raw_body
        self.id = raw_body.get("id", os.urandom(8).hex())
        self.content = raw_body.get("content", "")
        self.metadata = raw_body.get("metadata", {})

    def as_dict(self) -> dict:
        return {"id": self.id, "content": self.content, "metadata": self.metadata}


class PublishRequest:
    """Helper to build a publication request payload."""

    def __init__(
        self, topic_arn: str, messages: list[dict], message_attributes: dict = None
    ):
        self.topic_arn = topic_arn
        self.messages = messages
        self.message_attributes = message_attributes or {}

    def to_sns_args(self) -> dict:
        """Convert this request into arguments for boto3 SNS publish batch call."""
        sns_args = {
            "TopicArn": self.topic_arn,
            "Message": json.dumps(
                self.messages[0]
            ),  # placeholder, each publish is separate
        }
        return sns_args


class ConsumeResult:
    """Result wrapper for consumed messages (body + receipt)."""

    def __init__(self, body: dict, receipt_handle: str):
        self.body = body
        self.receipt_handle = receipt_handle

    def is_successful(self) -> bool:
        return bool(self.body)
