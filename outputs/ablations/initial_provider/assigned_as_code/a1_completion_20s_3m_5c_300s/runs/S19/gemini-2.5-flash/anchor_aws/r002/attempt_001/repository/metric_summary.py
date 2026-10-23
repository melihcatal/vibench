from datetime import datetime, timezone
from typing import Dict, Any, List

from observability_client import get_cloudwatch_client, get_vertex_ai_model

def metric_summary(payload: Dict[str, Any], config: Dict[str, Any] = None) -> Dict[str, str]:
    config = config or {}
    # Fetch metric data using CloudWatch (consistent with other SAME-SCENARIO files)
    cloudwatch_client = get_cloudwatch_client(config.get("region"))

    response = cloudwatch_client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in config.get("dimensions", {}).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=["Average"]
    )
    datapoints = response["Datapoints"]
    
    metric_data_str = "\n".join([f"Timestamp: {p['Timestamp']}, Average: {p['Average']}" for p in datapoints])

    # Summarize using Google Cloud Vertex AI (Gemini)
    vertex_ai_model = get_vertex_ai_model(
        project_id=config["gcp_project_id"],
        location=config["gcp_region"],
        model_name="gemini-pro"
    )

    prompt = f"Summarize the following metric data and identify any trends or anomalies: {metric_data_str}"
    response = vertex_ai_model.generate_content(prompt)
    
    summary = response.text

    return {"summary": summary}
