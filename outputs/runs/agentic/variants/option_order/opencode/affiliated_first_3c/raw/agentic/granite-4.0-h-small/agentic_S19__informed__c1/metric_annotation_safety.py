import os
from observable_client import get_provider_client
from observable_models import QueryMetricWindowRequest

PROVIDER = os.getenv("METRICS_PROVIDER", "datadog")


def check_metric_labels_for_safety(metric_name: str, limit: int = 100) -> bool:
    """Check free‑text metric labels or annotations for unsafe content (e.g., profanity).

    Uses the chosen provider's SDK to fetch recent labels/annotations, then runs a
    safety check (here we call a generic guardrails service via a placeholder function).

    Returns True if all labels are safe, False otherwise.
    """
    client = get_provider_client(PROVIDER)
    # Fetch recent labels (example for Datadog and IBM; other providers may differ)
    if PROVIDER == "datadog":
        # Datadog API: list custom metrics and their tags
        metrics = client.metrics.get_metrics(tags=True, limit=limit)
        labels = [tag for metric in metrics for tag in metric.get("tags", [])]
    elif PROVIDER == "ibm_monitoring":
        # IBM: list custom metrics with their label sets
        metrics = client.list_metrics(limit=limit)
        labels = [lbl for m in metrics for lbl in m.get("labels", {}).values()]
    elif PROVIDER == "azure":
        # Azure Monitor: list metric definitions with annotations
        definitions = client.metric_definitions.list(resource="", metric=metric_name)
        labels = [defn.annotation for defn in definitions]
    elif PROVIDER == "cloudwatch":
        # CloudWatch: list metrics with Dimension filters (no direct labels)
        raise NotImplementedError("CloudWatch label retrieval not implemented")
    elif PROVIDER == "alibaba":
        # Alibaba CloudMonitor: list metrics with label info
        metrics = client.DescribeMetrics(marker="", limit=limit)
        labels = [lbl for m in metrics for lbl in m.get("labels", {}).values()]
    elif PROVIDER == "google":
        # Google Monitoring: list metric descriptors
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        descriptors = client.metric_descriptor.list(name=f"projects/{project}")
        labels = [desc.label for desc in descriptors]
    else:
        raise ValueError(f"Unsupported provider for label safety check: {PROVIDER}")

    # Placeholder safety check – replace with real guardrails call
    unsafe = any(is_unsafe(label) for label in labels)
    return not unsafe


# Simple stub for illustration; real implementation would call a moderation API


def is_unsafe(text: str) -> bool:
    unsafe_words = {"badword", "offensive"}
    return any(word in text.lower() for word in unsafe_words)


if __name__ == "__main__":
    safe = check_metric_labels_for_safety("system.cpu.user")
    print("Labels safe?" if safe else "Labels contain unsafe content!")
