import json


def create_log_entry(
    severity, message, labels=None, json_payload=None, correlation_id=None
):
    """
    Creates a dictionary representing a structured log entry.
    """
    entry = {
        "severity": severity,
        "message": message,
    }
    if labels:
        entry["labels"] = labels
    if json_payload:
        entry["jsonPayload"] = json_payload
    if correlation_id:
        if "jsonPayload" not in entry:
            entry["jsonPayload"] = {}
        entry["jsonPayload"]["correlationId"] = correlation_id
    return entry


def build_log_filter(
    severity=None,
    resource_type=None,
    resource_labels=None,
    text_search=None,
    timestamp_start=None,
    timestamp_end=None,
    json_field_filters=None,
):
    """
    Builds a filter string for Google Cloud Logging queries.
    """
    filters = []
    if severity:
        filters.append(f"severity={severity}")
    if resource_type:
        filters.append(f'resource.type="{resource_type}"')
    if resource_labels:
        for key, value in resource_labels.items():
            filters.append(f'resource.labels.{key}="{value}"')
    if text_search:
        filters.append(f'textPayload:"{text_search}" OR jsonPayload:"{text_search}"')
    if timestamp_start:
        filters.append(f'timestamp:>="{timestamp_start}"')
    if timestamp_end:
        filters.append(f'timestamp:<="{timestamp_end}"')
    if json_field_filters:
        for field, value in json_field_filters.items():
            filters.append(f'jsonPayload.{field}="{value}"')

    return " ".join(filters)
