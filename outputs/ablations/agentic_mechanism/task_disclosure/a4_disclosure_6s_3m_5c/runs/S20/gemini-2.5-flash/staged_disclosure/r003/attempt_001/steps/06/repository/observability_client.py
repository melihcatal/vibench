
import os

class ObservabilityClient:
    def __init__(self, project_id: str, log_name: str):
        self.project_id = project_id
        self.log_name = log_name
        # In a real scenario, you would initialize the Google Cloud Logging client here.
        # For example:
        # from google.cloud import logging
        # self.client = logging.Client(project=self.project_id)
        # self.logger = self.client.logger(self.log_name)
        print(f"ObservabilityClient initialized for project: {self.project_id}, log: {self.log_name}")

    def log_entry(self, message: str, severity: str = "INFO", labels: dict = None):
        """
        Simulates logging a single entry to the configured log.
        In a real scenario, this would use the Google Cloud Logging client.
        """
        log_entry_data = {
            "message": message,
            "severity": severity,
            "labels": labels if labels else {},
            "log_name": self.log_name,
            "project_id": self.project_id
        }
        # Example of how to log in Google Cloud Logging:
        # self.logger.log(text_payload=message, severity=severity, labels=labels)
        print(f"Logged entry: {log_entry_data}")
        return log_entry_data

    def query_logs(self, filter_string: str, order_by: str = "timestamp desc", limit: int = 10):
        """
        Simulates querying logs based on a filter string.
        In a real scenario, this would use the Google Cloud Logging client's list_entries method.
        """
        print(f"Querying logs for project: {self.project_id} with filter: '{filter_string}', order by: '{order_by}', limit: {limit}")
        # Example of how to query logs in Google Cloud Logging:
        # entries = self.client.list_entries(
        #     filter_=filter_string,
        #     order_by=order_by,
        #     page_size=limit
        # )
        # return [entry for entry in entries]
        print("Simulating log query result...")
        return [
            {"timestamp": "2026-09-19T10:00:00Z", "message": "Simulated log entry 1", "severity": "INFO"},
            {"timestamp": "2026-09-19T10:01:00Z", "message": "Simulated log entry 2", "severity": "WARNING"}
        ]

# Example of how to use environment variables for configuration
if __name__ == "__main__":
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
    LOG_NAME = os.getenv("GCP_LOG_NAME", "your-application-log")

    client = ObservabilityClient(project_id=PROJECT_ID, log_name=LOG_NAME)

    # Simulate logging an entry
    client.log_entry("User logged in successfully.", severity="INFO", labels={"user_id": "123"})
    client.log_entry("Failed to connect to database.", severity="ERROR", labels={"service": "auth-service"})

    # Simulate querying logs
    results = client.query_logs(filter_string='severity="ERROR"', limit=1)
    print("Query Results:", results)
