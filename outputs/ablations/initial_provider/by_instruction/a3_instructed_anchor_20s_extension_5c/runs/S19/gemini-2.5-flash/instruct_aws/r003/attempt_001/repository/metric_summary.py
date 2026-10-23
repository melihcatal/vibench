from datetime import datetime, timedelta
from typing import Dict, Any, List

from observability_client import ObservabilityClient
from observability_models import MetricQuery

def metric_summary(query: MetricQuery, summary_period_hours: int = 24) -> Dict[str, Any]:
    client = ObservabilityClient()
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=summary_period_hours)

    cloudwatch_dimensions = [{'Name': k, 'Value': v} for k, v in query.dimensions.items()]

    # Get statistics for the metric (e.g., Average, Maximum, Minimum)
    response = client.cloudwatch_client.get_metric_statistics(
        Namespace=query.namespace,
        MetricName=query.metric_name,
        Dimensions=cloudwatch_dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=query.period,
        Statistics=['Average', 'Maximum', 'Minimum', 'Sum', 'SampleCount']
    )

    summary = {
        "metric_name": query.metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "datapoints": response.get('Datapoints', [])
    }

    # Basic anomaly detection (example: if max value is significantly higher than average)
    if response.get('Datapoints'):
        averages = [dp['Average'] for dp in response['Datapoints'] if 'Average' in dp]
        maximums = [dp['Maximum'] for dp in response['Datapoints'] if 'Maximum' in dp]

        if averages and maximums:
            avg_average = sum(averages) / len(averages)
            avg_maximum = sum(maximums) / len(maximums)

            if avg_average > 0 and (avg_maximum / avg_average) > 1.5: # Example threshold
                summary["anomaly_detected"] = True
                summary["anomaly_reason"] = "Maximum value significantly higher than average."
            else:
                summary["anomaly_detected"] = False
        else:
            summary["anomaly_detected"] = False
    else:
        summary["anomaly_detected"] = False
        summary["anomaly_reason"] = "No datapoints available for analysis."

    return summary
