import os
import datetime
from openai import OpenAI
from .observability_client import query_time_series
from .observability_models import MetricQuery, TimeInterval, MetricResponse, TimeSeriesPoint

def metric_summary(metric_name: str, duration_hours: int = 24) -> str:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=duration_hours)
    interval = TimeInterval(start_time=start_time, end_time=end_time)
    query = MetricQuery(metric_type=metric_name)
    response: MetricResponse = query_time_series(query, interval)
    data_str = [{"time": p.timestamp.isoformat(), "value": p.value} for p in response.points]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful metrics analyst."},
            {"role": "user", "content": f"Summarize recent trends or anomalies in this metric data points: {data_str}"}
        ]
    )
    return completion.choices[0].message.content