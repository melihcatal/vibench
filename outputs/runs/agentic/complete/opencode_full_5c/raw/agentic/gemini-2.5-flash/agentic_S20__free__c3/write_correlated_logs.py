import os
import uuid
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

client = ObservabilityClient(project_id=PROJECT_ID, log_name="my-correlated-app-log")


def write_correlated_log_events(request_id: str, user_id: str):
    # First log event in a correlated sequence
    entry1 = CorrelatedLogEntry(
        message="Request received for user data",
        correlation_id=request_id,
        severity="INFO",
        json_payload={
            "user_id": user_id,
            "api_endpoint": "/api/v1/users",
            "stage": "start",
        },
    )
    client.write_correlated_log(entry1)
    print(f"Wrote correlated log (stage 1): {{entry1.message}}")

    # Second log event in the same correlated sequence
    entry2 = CorrelatedLogEntry(
        message="Fetching user profile from database",
        correlation_id=request_id,
        severity="DEBUG",
        json_payload={
            "user_id": user_id,
            "database_query": "SELECT * FROM users WHERE id=:user_id",
            "stage": "db_fetch",
        },
    )
    client.write_correlated_log(entry2)
    print(f"Wrote correlated log (stage 2): {{entry2.message}}")

    # Third log event in the same correlated sequence
    entry3 = CorrelatedLogEntry(
        message="User profile successfully retrieved and sent",
        correlation_id=request_id,
        severity="INFO",
        json_payload={"user_id": user_id, "response_status": 200, "stage": "complete"},
    )
    client.write_correlated_log(entry3)
    print(f"Wrote correlated log (stage 3): {{entry3.message}}")


if __name__ == "__main__":
    # Example usage:
    correlation_id_1 = str(uuid.uuid4())
    print(f"--- Writing logs for request ID: {{correlation_id_1}} ---")
    write_correlated_log_events(correlation_id_1, "test-user-A")

    print("\n")

    correlation_id_2 = str(uuid.uuid4())
    print(f"--- Writing logs for request ID: {{correlation_id_2}} ---")
    write_correlated_log_events(correlation_id_2, "test-user-B")
