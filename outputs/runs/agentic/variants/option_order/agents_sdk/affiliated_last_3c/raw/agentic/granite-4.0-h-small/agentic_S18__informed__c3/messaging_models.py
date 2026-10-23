from typing import Any, Dict

class EventMessage:
    """Wrapper for a Pub/Sub event payload.",
    def __init__(self, data: Any):
        self.data = data
    
    def to_json(self) -> str:
        """Serialize payload to JSON string.",
        return json.dumps(self.data)
    

class DeadLetterPayload:
    """Structure for messages sent to a dead-letter topic.",
    def __init__(self, original_message: str, metadata: Dict[str, Any]):
        self.original_message = original_message
        self.metadata = metadata
    
    def to_json(self) -> str:
        return json.dumps({
            "original_message": self.original_message,
            "metadata": self.metadata,
        })
