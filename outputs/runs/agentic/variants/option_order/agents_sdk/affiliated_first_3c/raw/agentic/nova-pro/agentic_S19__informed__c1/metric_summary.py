import boto3

def summarize_metric_trends(metric_name, start_time, end_time):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'input_text': f'Summarize the trends for the metric {metric_name} from {start_time} to {end_time}'
        }
    )
    return response