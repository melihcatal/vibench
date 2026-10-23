import os
from datetime import datetime
from observability_client import ObservabilityClient
from observability_models import StructuredLogEntry

# Ensure GOOGLE_CLOUD_PROJECT environment variable is set
# For local testing, you might set it like: export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

client = ObservabilityClient(project_id=PROJECT_ID, log_name="my-structured-app-log")


def write_structured_log_event(
    message: str, severity: str, user_id: str, product_id: str, quantity: int
):
    entry = StructuredLogEntry(
        message=message,
        severity=severity,
        json_payload={
            "user_id": user_id,
            "product_id": product_id,
            "quantity": quantity,
            "event_type": "purchase",
            "application": "ecommerce-frontend",
        },
    )
    client.write_structured_log(entry)
    print(f"Wrote structured log: {{message}}")


if __name__ == "__main__":
    # Example usage:
    write_structured_log_event(
        message="User completed a purchase",
        severity="INFO",
        user_id="user-123",
        product_id="prod-abc",
        quantity=2,
    )

    write_structured_log_event(
        message="Failed to process payment",
        severity="ERROR",
        user_id="user-456",
        product_id="prod-xyz",
        quantity=1,
    )
