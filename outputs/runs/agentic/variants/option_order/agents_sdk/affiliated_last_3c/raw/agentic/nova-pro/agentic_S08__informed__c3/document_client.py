import os

def get_client(service):
    if service == 'textract':
        return boto3.client('textract', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    elif service == 'documentai':
        from google.cloud import documentai
        return documentai.DocumentProcessorServiceClient()
    elif service == 'mindee':
        import mindee
        return mindee.Client(api_key=os.getenv('MINDEE_API_KEY'))
    elif service == 'alibaba_ocr':
        import alibabacloud_ocr_api
        return alibabacloud_ocr_api.Client(os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID'), os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET'))