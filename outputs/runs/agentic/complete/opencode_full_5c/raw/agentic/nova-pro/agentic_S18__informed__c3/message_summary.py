import boto3


# Summarize message processing results
def summarize_message_processing(messages):
    comprehend_client = boto3.client("comprehend")
    summaries = []
    for message in messages:
        response = comprehend_client.detect_sentiment(
            Text=message["Message"], LanguageCode="en"
        )
        summaries.append(response["Sentiment"])
    return summaries
