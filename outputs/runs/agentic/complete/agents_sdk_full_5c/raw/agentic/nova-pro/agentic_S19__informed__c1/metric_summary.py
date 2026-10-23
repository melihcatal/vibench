import boto3

def metric_summary(metric_name, start_time, end_time):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        modelId='anthropic.claude-v2',
        body={
            'prompt': f'Summarize the recent trends for the {metric_name} metric from {start_time} to {end_time}.',
            'max_tokens_to_sample': 300
        }
    )
    return response['body'].read().decode('utf-8')