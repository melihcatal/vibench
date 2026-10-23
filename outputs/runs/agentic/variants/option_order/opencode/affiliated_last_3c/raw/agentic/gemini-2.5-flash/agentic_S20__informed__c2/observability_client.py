import os
from google.cloud import logging_v2


class ObservabilityClient:
    def __init__(self, project_id: str, log_name: str = "application-logs"):
        self.project_id = project_id
        self.log_name = log_name
        self.logging_client = logging_v2.Client(project=self.project_id)
        self.logger = self.logging_client.logger(self.log_name)

    def write_log_entry(self, entry_dict: dict):
        if "jsonPayload" in entry_dict:
            self.logger.log_struct(
                entry_dict["jsonPayload"],
                severity=entry_dict["severity"],
                labels=entry_dict["labels"],
                resource=entry_dict["resource"],
            )
        else:
            self.logger.log_text(
                entry_dict["textPayload"],
                severity=entry_dict["severity"],
                labels=entry_dict["labels"],
                resource=entry_dict["resource"],
            )

    def list_log_entries(self, filter_string: str, order_by: str, page_size: int):
        entries = self.logging_client.list_entries(
            filter_=filter_string, order_by=order_by, page_size=page_size
        )
        return [entry.to_api_repr() for entry in entries]


# Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set up)
# if __name__ == "__main__":
#     project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
#     if not project_id:
#         raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
#
#     client = ObservabilityClient(project_id)
#     print(f"Initialized ObservabilityClient for project: {client.project_id}")
