import boto3

AWS_REGION = 'us-west-2'

def get_textract_client():
    return boto3.client('textract', region_name=AWS_REGION)

def start_document_analysis(client, document_location, feature_types):
    response = client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=feature_types
    )
    return response

def get_document_analysis_result(client, job_id):
    response = client.get_document_analysis(JobId=job_id)
    return response