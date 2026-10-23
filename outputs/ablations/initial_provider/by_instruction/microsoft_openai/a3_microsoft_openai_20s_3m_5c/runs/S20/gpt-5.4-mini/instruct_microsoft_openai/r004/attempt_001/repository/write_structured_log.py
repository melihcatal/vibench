from observability_client import get_client
from observability_models import normalize_log_event


def write_structured_log(event):
    client = get_client()
    payload = normalize_log_event(event)
    return client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": "Convert the input into a structured managed log record and acknowledge ingestion.",
            },
            {"role": "user", "content": str(payload)},
        ],
    )
