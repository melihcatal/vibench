from collections import Counter

from observability_models import IncidentSummary, extract_message, extract_severity


def incident_summary(entries: list[dict]) -> dict:
    severities = Counter(extract_severity(entry) for entry in entries)
    samples = [extract_message(entry) for entry in entries[:5] if extract_message(entry)]
    summary = IncidentSummary(
        title="Incident log summary",
        severity_counts=dict(severities),
        sample_messages=samples,
    )
    return summary.__dict__
