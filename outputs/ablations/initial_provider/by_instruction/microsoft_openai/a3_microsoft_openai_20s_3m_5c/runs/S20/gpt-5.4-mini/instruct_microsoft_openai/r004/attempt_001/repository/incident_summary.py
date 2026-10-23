from observability_client import get_client


def incident_summary(error_logs):
    client = get_client()
    return client.responses.create(model="gpt-4.1-mini", input=str(error_logs))
