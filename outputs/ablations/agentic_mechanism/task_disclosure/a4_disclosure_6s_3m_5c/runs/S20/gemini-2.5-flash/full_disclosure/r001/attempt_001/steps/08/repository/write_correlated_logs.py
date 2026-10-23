import os
import google.cloud.logging

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[str], resource_type: str = "global", resource_labels: dict = None):
    """
    Writes application log events with a shared request or correlation identifier to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to (e.g., "my-app-logs").
        correlation_id: The shared request or correlation identifier.
        messages: A list of log messages to write.
        resource_type: The monitored resource type (e.g., "global", "gce_instance").
        resource_labels: A dictionary of labels for the monitored resource.
    """
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)

    # Common labels for all log entries in this batch, including the correlation ID
    common_labels = {"correlation_id": correlation_id}

    for message in messages:
        logger.log(
            text_payload=message,
            labels=common_labels,
            resource={
                "type": resource_type,
                "labels": resource_labels if resource_labels else {}
            }
        )
    print(f"Successfully wrote {len(messages)} log entries with correlation ID '{correlation_id}' to log '{log_name}'.")

if __name__ == '__main__':
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-key.json"

    # Replace with your desired log name and correlation ID
    my_log_name = "my-application-correlated-logs"
    my_correlation_id = "req-12345"
    my_messages = [
        "User 'test_user' initiated transaction.",
        "Processing payment for order #001.",
        "Transaction 'TXN-ABC' completed successfully."
    ]

    # Example with resource labels (optional)
    my_resource_labels = {
        "project_id": client.project, # Assuming client is defined for project_id
        "zone": "us-central1-a",
        "instance_id": "my-instance-1"
    }
    # To run this example, ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # or that you are running in a Google Cloud environment with default credentials.
    # write_correlated_logs(my_log_name, my_correlation_id, my_messages, resource_labels=my_resource_labels)
    print("Example usage commented out. Uncomment and configure GOOGLE_APPLICATION_CREDENTIALS to run.")
