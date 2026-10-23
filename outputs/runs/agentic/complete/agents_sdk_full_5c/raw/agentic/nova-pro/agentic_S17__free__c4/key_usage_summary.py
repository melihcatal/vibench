import boto3

def summarize_key_usage():
    kms = boto3.client('kms')
    response = kms.list_keys()
    #... (summarize key usage logic here)