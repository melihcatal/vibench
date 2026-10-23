import boto3


def summarize_error_logs(log_group_name, query_string):
    client = boto3.client("comprehend")
    response = client.detect_sentiment(Text=query_string, LanguageCode="en")
    return response["Sentiment"]
