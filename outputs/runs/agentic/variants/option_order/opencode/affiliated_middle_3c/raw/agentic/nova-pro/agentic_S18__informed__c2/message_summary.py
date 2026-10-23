import os
import boto3


def summarize_messages(messages):
    summaries = []
    for message in messages:
        summaries.append(message["Body"][:100])
    return summaries
