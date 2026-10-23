import os

class PerspectiveClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY not found in config or environment variables.")

    def get_api_key(self):
        return self.api_key
