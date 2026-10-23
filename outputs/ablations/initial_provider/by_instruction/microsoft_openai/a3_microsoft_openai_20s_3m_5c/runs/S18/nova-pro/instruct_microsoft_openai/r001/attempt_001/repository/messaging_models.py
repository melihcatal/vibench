from typing import Any

# Define a model for the event
class EventModel:
    def __init__(self, data: Any):
        self.data = data

    # Normalize the event data
    def normalize(self):
        return str(self.data)