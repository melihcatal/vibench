import boto3


def get_cloudwatch_client():
    return boto3.client("cloudwatch")


def normalize_metric_response(response):
    normalized_response = {}
    for datapoint in response["Datapoints"]:
        normalized_response[datapoint["Timestamp"]] = datapoint["Average"]
    return normalized_response
