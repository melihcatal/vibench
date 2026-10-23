import json

class MessagePayload:
    def __init__(self, message_id: str, content: str, source: str):
        self.message_id = message_id
        self.content = content
        self.source = source

    def to_json(self):
        return json.dumps({
            "message_id": self.message_id,
            "content": self.content,
            "source": self.source
        })
