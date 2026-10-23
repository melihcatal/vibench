import os
import google.cloud.logging


class ObservabilityClient:
    def __init__(self, project_id: Optional[str] = None):
        if project_id is None:
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project_id is None:
                raise ValueError(
                    "Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set."
                )
        self.project_id = project_id
        self.logging_client = google.cloud.logging.Client(project=self.project_id)

    def get_logger(self, log_name: str) -> google.cloud.logging.Logger:
        return self.logging_client.logger(log_name)
