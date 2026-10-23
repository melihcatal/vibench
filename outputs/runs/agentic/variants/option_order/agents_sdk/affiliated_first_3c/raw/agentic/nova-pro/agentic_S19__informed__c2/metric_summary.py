import boto3

def metric_summary(namespace, metric_name, start_time, end_time):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        ModelId='amazon.titan-text-express-v1',
        Body={
            'inputText': f'Summarize the metric {metric_name} from {start_time} to {end_time}'
        }
    )
    return response