import boto3

transcribe = boto3.client('transcribe')

s3 = boto3.client('s3')