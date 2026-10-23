import boto3

def summarize_moderation_decisions(decisions):
    comprehend = boto3.client('comprehend')
    summary = comprehend.summarize_text(Text=decisions)
    return summary
