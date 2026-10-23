from __future__ import annotations

from typing import Any, Dict

from observability_client import text_generation_model, load_config, metric_client
from observability_models import MetricSummaryRequest
from google.cloud import monitoring_v3
from datetime import datetime, timedelta, timezone


def metric_summary(request: MetricSummaryRequest) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)
    interval = monitoring_v3.TimeInterval({"end_time": end_time, "start_time": start_time})
    series = client.list_time_series(request={"name": f"projects/{config.project_id}", "filter": request.filter_expression or f'metric.type = "{request.metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    values = []
    for ts in series:
        for point in ts.points:
            values.append(float(point.value.double_value or point.value.int64_value or point.value.distribution_value.count))
    model = text_generation_model()
    prompt = f"Summarize trend and possible anomalies for {request.metric_type} given values: {values[:50]}"
    summary = model.predict(prompt=prompt, temperature=0.2, max_output_tokens=256)
    return {"metric_type": request.metric_type, "summary": getattr(summary, 'text', str(summary)), "project_id": config.project_id}
