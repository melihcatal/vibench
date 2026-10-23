import os
from google.cloud import content_safety_v1


class ContentSafetyClient:
    def __init__(self):
        # Initialize the Google Cloud Content Safety client
        self.client = content_safety_v1.ContentSafetyServiceClient()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv(
            "GOOGLE_CLOUD_LOCATION", "global"
        )  # Content Safety is often global or regional

    def get_client(self):
        return self.client

    def get_project_id(self):
        return self.project_id

    def get_location(self):
        return self.location
