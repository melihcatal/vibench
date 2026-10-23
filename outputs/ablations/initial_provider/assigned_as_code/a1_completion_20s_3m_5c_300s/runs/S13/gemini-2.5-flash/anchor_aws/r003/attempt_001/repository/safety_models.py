from typing import List, Dict, Any

class ModerationRequest:
    def __init__(self, text: str, message_id: str = None):
        self.text = text
        self.message_id = message_id

class ModerationResponse:
    def __init__(self, message_id: str, is_safe: bool, moderation_results: Dict[str, Any]):
        self.message_id = message_id
        self.is_safe = is_safe
        self.moderation_results = moderation_results

class BatchModerationRequest:
    def __init__(self, texts: List[Dict[str, str]]):
        self.texts = texts # Each dict should have 'text' and optionally 'message_id'

class BatchModerationResponse:
    def __init__(self, results: List[ModerationResponse]):
        self.results = results
