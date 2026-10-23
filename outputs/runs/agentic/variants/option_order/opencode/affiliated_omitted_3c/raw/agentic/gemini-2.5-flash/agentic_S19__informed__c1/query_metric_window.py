from typing import List
from datetime import datetime, timedelta
import observability_client
from observability_models import (
    MetricQuery,
    TimeWindow,
    MetricData,
    MetricDataPoint,
    Dimension,
)


def query_metric_window(
    metric_query: MetricQuery,
    time_window: TimeWindow,
) -> List[MetricData]:
    cloudwatch = observability_client.get_aws_client("cloudwatch")

    start_time = datetime.fromisoformat(time_window.start_time.replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(time_window.end_time.replace("Z", "+00:00"))

    dimensions_param = (
        [{"Name": d.name, "Value": d.value} for d in metric_query.dimensions]
        if metric_query.dimensions
        else []
    )

    response = cloudwatch.get_metric_data(
        MetricDataQueries=[
            {
                "Id": "m1",
                "MetricStat": {
                    "Metric": {
                        "Namespace": metric_query.namespace,
                        "MetricName": metric_query.metric_name,
                        "Dimensions": dimensions_param,
                    },
                    "Period": metric_query.period,
                    "Stat": metric_query.stat,
                },
                "ReturnData": True,
            },
        ],
        StartTime=start_time,
        EndTime=end_time,
    )

    metric_datas = []
    for result in response["MetricDataResults"]:
        datapoints = []
        for i in range(len(result["Timestamps"])):
            datapoints.append(
                MetricDataPoint(
                    timestamp=result["Timestamps"][i].isoformat(),
                    value=result["Values"][i],
                    unit=result.get("Unit", "Unknown"),
                )
            )
        metric_datas.append(MetricData(label=result["Label"], datapoints=datapoints))

    return metric_datas
