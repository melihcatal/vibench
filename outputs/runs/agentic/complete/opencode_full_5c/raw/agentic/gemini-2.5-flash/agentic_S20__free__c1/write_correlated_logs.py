import os
import uuid
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import LogEntry

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOG_NAME = "my-correlated-app-log"


def write_correlated_logs(request_id: str, user_id: str, transaction_amount: float):
    client = ObservabilityClient(project_id=PROJECT_ID)

    log_entries = [
        LogEntry(
            severity="INFO",
            message=f"Request received for user {user_id}",
            resource_type="global",
            resource_labels={"project_id": PROJECT_ID},
            json_payload={
                "requestId": request_id,
                "userId": user_id,
                "stage": "received",
            },
            trace=request_id,  # Using request_id as trace for correlation
        ),
        LogEntry(
            severity="INFO",
            message=f"Processing transaction for request {request_id}",
            resource_type="global",
            resource_labels={"project_id": PROJECT_ID},
            json_payload={
                "requestId": request_id,
                "transactionAmount": transaction_amount,
                "stage": "processing",
            },
            trace=request_id,
        ),
        LogEntry(
            severity="INFO",
            message=f"Transaction completed for request {request_id}",
            resource_type="global",
            resource_labels={"project_id": PROJECT_ID},
            json_payload={
                "requestId": request_id,
                "status": "success",
                "stage": "completed",
            },
            trace=request_id,
        ),
    ]

    client.write_log_entries(log_name=LOG_NAME, log_entry_datas=log_entries)
    print(f"Wrote {len(log_entries)} correlated logs for request ID: {request_id}")


if __name__ == "__main__":
    # Example usage:
    correlation_id = str(uuid.uuid4())
    write_correlated_logs(
        request_id=correlation_id, user_id=str(uuid.uuid4()), transaction_amount=123.45
    )
