import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def stored_document_ocr(blob_name):
    subscription_key = os.getenv('COMPUTER_VISION_SUBSCRIPTION_KEY')
    endpoint = os.getenv('COMPUTER_VISION_ENDPOINT')
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container='documents', blob=blob_name)
    download_stream = blob_client.download_blob()
    image_stream = download_stream.readall()
    result = computervision_client.read_in_stream(image_stream, raw=True)
    operation_location = result.headers['Operation-Location']
    operation_id = operation_location.split('/')[-1]
    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break
    if result.status == 'succeeded':
        print('OCR Result:')
        for text_result in result.analyze_result.readResults:
            for line in text_result.lines:
                print(line.text)
    else:
        print('OCR failed')