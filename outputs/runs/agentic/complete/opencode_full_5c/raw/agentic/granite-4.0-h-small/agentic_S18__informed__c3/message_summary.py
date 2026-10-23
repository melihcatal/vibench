import json
from datetime import datetime


class MessageSummary:
    """
    Summarizes processing of a single message batch.
    """

    def __init__(
        self,
        batch_id: str,
        success_count: int,
        failure_count: int,
        processed_at: datetime,
    ):
        self.batch_id = batch_id
        self.success_count = success_count
        self.failure_count = failure_count
        self.processed_at = processed_at
        self.errors = []  # list of dict: {'msg_id': ..., 'error': ...}

    def add_error(self, msg_id: str, error: Exception):
        self.errors.append({"msg_id": msg_id, "error": str(error)})

    def to_json(self) -> str:
        data = {
            "batch_id": self.batch_id,
            "success": self.success_count,
            "failure": self.failure_count,
            "processed_at": self.processed_at.isoformat(),
            "errors": self.errors,
        }
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        summary = cls(
            batch_id=data["batch_id"],
            success_count=data["success"],
            failure_count=data["failure"],
            processed_at=datetime.fromisoformat(data["processed_at"]),
        )
        summary.errors = data.get("errors", [])
        return summary


if __name__ == "__main__":
    # Simple demo (remove in production)
    s = MessageSummary(
        batch_id="batch_1",
        success_count=5,
        failure_count=1,
        processed_at=datetime.now(),
    )
    s.add_error("msg_7", ValueError("payload malformed"))
    print(s.to_json())
