import boto3

class DocumentClient:
    def __init__(self):
        self.textract_client = boto3.client('textract')

    def start_document_analysis(self, document_location):
        response = self.textract_client.start_document_analysis(
            DocumentLocation=document_location,
            FeatureTypes=['FORMS', 'TABLES'])
        return response

    def get_analysis_result(self, job_id):
        response = self.textract_client.get_document_analysis(JobId=job_id)
        return response
