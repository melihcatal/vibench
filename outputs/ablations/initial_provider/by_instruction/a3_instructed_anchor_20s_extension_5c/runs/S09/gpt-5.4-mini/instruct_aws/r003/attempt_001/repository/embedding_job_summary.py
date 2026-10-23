import json
import sys

import boto3


def main() -> None:
    client = boto3.client("cloudwatch")
    metric = client.get_metric_statistics(Namespace="AWS/Bedrock", MetricName="Invocations", StartTime=__import__("datetime").datetime.utcnow(), EndTime=__import__("datetime").datetime.utcnow(), Period=60, Statistics=["Sum"])
    sys.stdout.write(json.dumps({"provider": "AWS", "summary": metric.get("Datapoints", [])}))


if __name__ == "__main__":
    main()
