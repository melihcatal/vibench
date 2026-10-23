import os
from observability_client import get_gcp_logging_client
from observability_models import StructuredLog

def write_log_entry(log_name: str = "my-structured-log"):
    """
    Writes a single structured log entry to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
    """
    # Instantiates a client
    logging_client = get_gcp_logging_client()

    # The name of the log to write to
    logger = logging_client.logger(log_name)

    # Create a structured log entry using our Pydantic model
    log_entry = StructuredLog(
        message="User logged in successfully.",
        user_id="user-12345",
        request_method="POST",
        request_url="/auth/login",
        response_status_code=200,
        extra_data={"auth_provider": "google"}
    )

    # Struct log, but can also be `text`
    logger.log_struct(log_entry.to_dict(), severity="INFO")

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    print(f"Wrote structured log to '{log_name}' in project '{project_id}'.")

if __name__ == "__main__":
    write_log_entry()
