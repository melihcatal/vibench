import boto3

def get_textract_client():
    return boto3.client('textract')

def start_document_analysis(document_location, feature_types):
    client = get_textract_client()
    response = client.start_document_analysis(
        DocumentLocation=document_location,
        FeatureTypes=feature_types
    )
    return response

def get_document_analysis_result(job_id):
    client = get_textract_client()
    response = client.get_document_analysis(
        JobId=job_id
    )
    return response