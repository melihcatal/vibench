import os


def get_documentai_client():
    client_options = {"api_endpoint": f"{os.getenv('DOCUMENTAI_LOCATION')}-documentai.googleapis.com"}
    return documentai.DocumentProcessorServiceClient(client_options=client_options)


def get_textract_client():
    return boto3.client('textract')


def get_computervision_client():
    return ComputerVisionClient("https://westus2.api.cognitive.microsoft.com/", CognitiveServicesCredentials(os.getenv('COMPUTERVISION_API_KEY')))