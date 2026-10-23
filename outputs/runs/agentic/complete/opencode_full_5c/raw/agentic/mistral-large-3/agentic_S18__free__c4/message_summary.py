from typing import Dict, Any, List
import json
from collections import defaultdict

# Provider-specific: No external provider, but aggregates results for later-step processing


class MessageSummary:
    def __init__(self):
        self.processed_messages = []
        self.error_messages = []

    def add_processed_message(self, message: Dict[str, Any]) -> None:
        self.processed_messages.append(message)

    def add_error_message(self, message: Dict[str, Any], error: str) -> None:
        self.error_messages.append({"message": message, "error": error})

    def generate_summary(self) -> Dict[str, Any]:
        return {
            "total_processed": len(self.processed_messages),
            "total_errors": len(self.error_messages),
            "error_details": [error["error"] for error in self.error_messages],
        }
