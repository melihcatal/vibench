import boto3

class DocumentClient:
    def __init__(self, region_name='us-west-2'):
        self.textract_client = boto3.client('textract', region_name=region_name)

    def start_document_analysis(self, document_bytes, feature_types=['FORMS', 'TABLES']):
        response = self.textract_client.start_document_analysis(
            Document={'Bytes': document_bytes},
            FeatureTypes=feature_types
        )
        return response

    def get_document_analysis_result(self, job_id):
        response = self.textract_client.get_document_analysis(JobId=job_id)
        return response

    def start_document_text_detection(self, document_bytes):
        response = self.textract_client.start_document_text_detection(
            Document={'Bytes': document_bytes}
        )
        return response

    def get_document_text_detection_result(self, job_id):
        response = self.textract_client.get_document_text_detection(JobId=job_id)
        return response
