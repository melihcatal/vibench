import boto3

def moderation_summary(responses):
    comprehend = boto3.client('comprehend')
    summary = {}
    for response in responses:
        for label in response['Labels']:
            if label['Name'] not in summary:
                summary[label['Name']] = 0
            summary[label['Name']] += 1
    return summary
