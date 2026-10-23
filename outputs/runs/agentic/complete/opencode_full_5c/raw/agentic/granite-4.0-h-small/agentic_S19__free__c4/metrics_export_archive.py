# [LATER-STEP] metrics_export_archive.py
import observability_client as client
import datetime
import json
import os


def archive_metric_snapshot(
    metric_name: str,
    start_time: str,
    end_time: str,
    archive_path: str = "/tmp/metric_snapshots",
):
    """Archive exported metric snapshots in managed object storage or local directory.
    Retrieves data via the concrete provider (e.g., Datadog) and writes JSON snapshots.
    """
    raw = client.query(metric=metric_name, start=start_time, end=end_time)
    data = (
        raw  # Assuming raw is serializable; adjust if provider returns custom objects
    )
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_file = os.path.join(archive_path, f"{metric_name}_{timestamp}.json")
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2)
    return {"archive_file": out_file}
