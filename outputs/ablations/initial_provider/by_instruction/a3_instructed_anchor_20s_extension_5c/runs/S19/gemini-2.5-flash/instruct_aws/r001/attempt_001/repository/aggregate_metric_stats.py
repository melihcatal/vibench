from datetime import datetime, timedelta
from typing import List, Dict, Optional

from observability_client import ObservabilityClient
from observability_models import MetricStatisticsResult

def aggregate_metric_stats(metric_name: str, namespace: str, duration_minutes: int, period_seconds: int, statistics: List[str], dimensions: Optional[Dict[str, str]] = None) -> MetricStatisticsResult:
    client = ObservabilityClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)

    datapoints_raw = client.get_metric_data(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        period=period_seconds,
        statistics=statistics,
        dimensions=dimensions
    )

    aggregated_stats = {stat: 0.0 for stat in statistics}
    if datapoints_raw:
        for stat in statistics:
            # This is a very basic aggregation. CloudWatch returns pre-aggregated stats if period is large enough.
            # For simple demonstration, we will just take the last value for the requested statistic if multiple are present, 
            # or sum them up if it's a 'Sum' statistic.
            # A more robust solution would process the `datapoints_raw` based on specific aggregation logic.
            # CloudWatch `get_metric_statistics` already returns aggregated values for the given period and statistics.
            # So, we can simply extract them.
            if stat in datapoints_raw[0]: # Check if the statistic exists in the first datapoint (assuming consistent structure)
                aggregated_stats[stat] = sum(dp.get(stat, 0.0) for dp in datapoints_raw)
            

    # The CloudWatch get_metric_statistics already returns aggregated statistics based on the period. 
    # The 'datapoints_raw' will contain one datapoint per period with the requested statistics. 
    # To get overall aggregated stats for the entire duration, we would typically sum/avg/etc. across these datapoints.
    # However, for simplicity and alignment with how get_metric_statistics works, we'll assume the primary statistic desired
    # is present in the datapoints and summarize it.

    final_statistics = {}
    for stat in statistics:
        # Example: if user asks for 'Average', and CloudWatch returns multiple 'Average' datapoints for different periods,
        # we might want the overall average of these averages, or the last one. 
        # For now, let's just take the average of all returned values for each statistic.
        values_for_stat = [dp.get(stat) for dp in datapoints_raw if dp.get(stat) is not None]
        if values_for_stat:
            final_statistics[stat] = sum(values_for_stat) / len(values_for_stat)
        else:
            final_statistics[stat] = 0.0 # Or None, depending on desired behavior


    return MetricStatisticsResult(metric_name=metric_name, namespace=namespace, statistics=final_statistics, dimensions=dimensions)
