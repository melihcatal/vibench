from speech_client import get_comprehend_client

def archive_summary(text):
    comprehend = get_comprehend_client()
    response = comprehend.start_document_summarization_job(
        InputDataConfig={'S3Uri': 's3://input-bucket/'},
        OutputDataConfig={'S3Uri': 's3://output-bucket/'},
        DataAccessRoleArn='arn:aws:iam::123456789012:role/service-role/AmazonComprehendServiceRole'
    )
    return response