import boto3

transcribe = boto3.client('transcribe')
translate = boto3.client('translate')
comprehend = boto3.client('comprehend')
sagemaker_runtime = boto3.client('sagemaker-runtime')

def get_transcribe_client():
    return transcribe

def get_translate_client():
    return translate

def get_comprehend_client():
    return comprehend

def get_sagemaker_runtime_client():
    return sagemaker_runtime