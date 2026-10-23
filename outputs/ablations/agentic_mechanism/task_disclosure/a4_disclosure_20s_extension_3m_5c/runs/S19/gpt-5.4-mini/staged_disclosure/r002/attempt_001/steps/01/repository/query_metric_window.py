import argparse
import json
import os
from datetime import datetime, timedelta, timezone

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("metric_name")
    p.add_argument("--hours", type=int, default=1)
    p.add_argument("--from-ts", type=int, dest="from_ts")
    p.add_argument("--to-ts", type=int, dest="to_ts")
    return p.parse_args()


def main():
    args = parse_args()
    end_ts = args.to_ts or int(datetime.now(timezone.utc).timestamp())
    start_ts = args.from_ts or int((datetime.now(timezone.utc) - timedelta(hours=args.hours)).timestamp())

    configuration = Configuration()
    configuration.api_key["apiKeyAuth"] = os.environ["DD_API_KEY"]
    configuration.app_key["apiKeyAuth"] = os.environ["DD_APP_KEY"]
    configuration.server_variables["site"] = os.getenv("DD_SITE", "datadoghq.com")

    query = f"{args.metric_name}{{*}}"
    with ApiClient(configuration) as api_client:
        api = MetricsApi(api_client)
        response = api.query_metrics(_from=start_ts, to=end_ts, query=query)

    series = []
    for point in getattr(response, "series", []) or []:
        for point_data in getattr(point, "pointlist", []) or []:
            if point_data and len(point_data) == 2 and point_data[1] is not None:
                series.append({"timestamp": int(point_data[0]), "value": point_data[1]})

    print(json.dumps({"metric": args.metric_name, "from": start_ts, "to": end_ts, "datapoints": series}, indent=2))


if __name__ == "__main__":
    main()
