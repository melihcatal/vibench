import boto3

def stream_completion(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.start_document_classification_job(
        InputDataConfig={'S3Uri': 's3://input-bucket/'}, 
        OutputDataConfig={'S3Uri': 's3://output-bucket/'}, 
        DataAccessRoleArn='arn:aws:iam::123456789012:role/service-role/AmazonComprehendServiceRole-example-role',
        Mode='SYNC',
        JobName='example-job'
    )
    return response['JobId']