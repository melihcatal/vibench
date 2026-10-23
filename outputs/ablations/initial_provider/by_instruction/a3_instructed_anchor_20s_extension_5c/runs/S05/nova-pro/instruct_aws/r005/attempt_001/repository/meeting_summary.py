import boto3

def summarize_meeting(transcript):
    client = boto3.client('comprehend')
    result = client.start_summarization_job(
        InputDataConfig={'S3Uri': 's3://your-bucket/input/'},
        OutputDataConfig={'S3Uri': 's3://your-bucket/output/'},
        LanguageCode='en',
        SummarizationType='meeting'
    )
    return result['JobId']