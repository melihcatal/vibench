import boto3

class DocumentClient:
    def __init__(self, region_name='us-east-1'):
        self.textract_client = boto3.client('textract', region_name=region_name)

    def start_document_analysis(self, document_location, feature_types):
        response = self.textract_client.start_document_analysis(
            DocumentLocation=document_location,
            FeatureTypes=feature_types
        )
        return response

    def get_analysis_result(self, job_id):
        response = self.textract_client.get_document_analysis(JobId=job_id)
        return response

if __name__ == '__main__':
    document_client = DocumentClient()
    document_location = {'S3Object': {'Bucket': 'your-bucket-name', 'Name': 'your-document-name'}}
    feature_types = ['FORMS', 'TABLES']
    analysis_job = document_client.start_document_analysis(document_location, feature_types)
    print(analysis_job)