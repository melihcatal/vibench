import boto3

bedrock = boto3.client('bedrock')

def select_model():
    model_id = 'amazon.titan-text-express-v1'
    return model_id