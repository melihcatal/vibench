import json

class Event:
    def __init__(self, detail_type: str, source: str, detail: dict):
        self.detail_type = detail_type
        self.source = source
        self.detail = detail

    def to_json(self):
        return json.dumps({
            "detail-type": self.detail_type,
            "source": self.source,
            "detail": self.detail
        })
