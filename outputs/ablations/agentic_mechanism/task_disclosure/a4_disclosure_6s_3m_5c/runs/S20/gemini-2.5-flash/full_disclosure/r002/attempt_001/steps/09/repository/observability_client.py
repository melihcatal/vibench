import os
import logging
from google.cloud import logging as gcp_logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

class ObservabilityClient:
    def __init__(self, project_id=None, log_name="application_logs"):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        if not self.project_id:
            raise ValueError("Google Cloud Project ID not provided and GOOGLE_CLOUD_PROJECT environment variable not set.")
        self.log_name = log_name
        self.client = gcp_logging.Client(project=self.project_id)
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.INFO)

        # Add Cloud Logging handler
        handler = CloudLoggingHandler(self.client, name=log_name)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

    def write_log(self, message, severity="INFO", **kwargs):
        log_entry = {
            "severity": severity,
            "jsonPayload": {
                "message": message,
                **kwargs
            }
        }
        self.logger.info(message, extra=log_entry)

    def query_logs(self, filter_string, order_by="timestamp desc", limit=100):
        # This is a simplified example. Real-world queries might need more complex handling.
        # It's recommended to use google-cloud-logging query methods for robust querying.
        # For simplicity, this client helper will only construct a basic filter.
        full_filter = f"logName=projects/{self.project_id}/logs/{self.log_name} AND {filter_string}"
        entries = self.client.list_entries(filter_=full_filter, order_by=order_by, page_size=limit)
        return list(entries)

if __name__ == "__main__":
    # Example Usage (requires GOOGLE_CLOUD_PROJECT env var set and authenticated gcloud)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # gcloud auth application-default login
    try:
        client = ObservabilityClient()
        logger = client.get_logger()

        logger.info("This is a test log entry from observability_client.py")
        client.write_log("Another log entry with custom fields", severity="WARNING", user_id="123", transaction_id="abc")

        print("Successfully wrote log entries. Querying recent logs (may take a moment to appear)...")

        # Example query (adjust filter as needed)
        # recent_logs = client.query_logs(filter_string="severity=INFO", limit=5)
        # for entry in recent_logs:
        #     print(f"Log: {entry.payload} - Severity: {entry.severity}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
