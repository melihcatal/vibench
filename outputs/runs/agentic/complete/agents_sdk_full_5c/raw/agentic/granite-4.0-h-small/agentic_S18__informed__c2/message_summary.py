import json
from typing import List
from messaging_models import ProcessingResult

class MessageSummary:
    """Aggregates results of a batch of processed messages."""
    def __init__(self, results: List[ProcessingResult]):
        self.results = results
        self._aggregate()

    def _aggregate(self):
        self.total = len(self.results)
        self.ok = sum(1 for r in self.results if r["status"] == "ok")
        self.failed = sum(1 for r in self.results if r["status"] == "failed")
        self.dead_letter = sum(1 for r in self.results if r["status"] == "dead_letter")
        self.reasons = self._collect_failure_reasons()

    def _collect_failure_reasons(self) -> dict[str, int]:
        """Count occurrences of each failure reason."""
        counts = {}
        for r in self.results:
            if r["status"] == "failed" and r["reason"]:
                counts[r["reason"]] = counts.get(r["reason"], 0) + 1
        return counts

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "ok": self.ok,
            "failed": self.failed,
            "dead_letter": self.dead_letter,
            "reasons": self.reasons,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

if __name__ == "__main__":
    # Simple demo – build a fake batch of results
    fake_results = [
        {"status": "ok", "message_id": "msg-1"},
        {"status": "failed", "message_id": "msg-2", "reason": "validation"},
        {"status": "failed", "message_id": "msg-3", "reason": "validation"},
        {"status": "dead_letter", "message_id": "msg-4"},
    ]
    summary = MessageSummary(fake_results)
    print(summary.to_json())
