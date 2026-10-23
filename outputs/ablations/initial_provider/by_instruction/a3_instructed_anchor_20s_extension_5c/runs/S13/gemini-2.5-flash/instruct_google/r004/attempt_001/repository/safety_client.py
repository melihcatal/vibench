import os

class SafetyClient:
    def __init__(self, api_key: str = None, project_id: str = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        self.project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID")

        if not self.api_key:
            raise ValueError("Google API Key not provided and not found in GOOGLE_API_KEY environment variable.")

    def get_api_key(self) -> str:
        return self.api_key

    def get_project_id(self) -> str:
        return self.project_id

# Example of a helper function for common client setup
def initialize_google_client():
    return SafetyClient()
