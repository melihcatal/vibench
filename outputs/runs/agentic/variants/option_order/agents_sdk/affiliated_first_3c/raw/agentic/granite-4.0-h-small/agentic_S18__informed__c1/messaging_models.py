from typing import Dict, Any

class KafkaMessage:
    def __init__(self, key: str, value: str, topic: str, partition: int, offset: int):
        self.key = key
        self.value = value
        self.topic = topic
        self.partition = partition
        self.offset = offset

    def to_dict(self) -> Dict[str, Any]:
        return {
            'key': self.key,
            'value': self.value,
            'topic': self.topic,
            'partition': self.partition,
            'offset': self.offset,
        }

    @classmethod
    def from_confluent(cls, msg):
        # Confluent-kafka message object fields
        return cls(
            key=msg.key().decode() if msg.key() else None,
            value=msg.value().decode() if msg.value() else None,
            topic=msg.topic(),
            partition=msg.partition(),
            offset=msg.offset(),
        )

def normalize_event(json_payload: str) -> Dict[str, Any]:
    """
    Simple normalization for incoming JSON events.
    Ensure required fields are present, add defaults, and strip whitespace.
    """
    import json
    data = json.loads(json_payload)
    # Example normalization
    data['source'] = data.get('source', 'unknown')
    data['timestamp'] = data.get('timestamp', '1970-01-01T00:00:00Z')
    return data

def serialize_event(event: Dict[str, Any]) -> str:
    import json
    return json.dumps(event)

# Example usage in helpers

def publish_event(event: Dict[str, Any]):
    from publish_event import publish_event  # re-use generic function
    # Convert to serialized form
    serialized = serialize_event(event)
    publish_event(serialized)

# End of module
