from typing import List
import boto3
from translation_models import TranslationRequest, TranslationResponse

class BatchTranslator:
    def __init__(self):
        self.client = boto3.client(service_name='translate', region_name='us-east-1')

    def batch_translate(self, requests: List[TranslationRequest]) -> List[TranslationResponse]:
        texts = [req.text for req in requests]
        source_langs = [req.source_lang for req in requests]
        target_langs = [req.target_lang for req in requests]

        response = self.client.start_text_translation_job(
            InputDataConfig={
                'S3Uri': f's3://{requests[0].s3_input_bucket}/{requests[0].s3_input_key}',
                'ContentType': 'text/plain'
            },
            OutputDataConfig={
                'S3Uri': f's3://{requests[0].s3_output_bucket}/{requests[0].s3_output_key}'
            },
            DataAccessRoleArn=requests[0].data_access_role_arn,
            SourceLanguageCode=source_langs[0],
            TargetLanguageCodes=[target_langs[0]]
        )

        job_id = response['JobId']
        return [TranslationResponse(
            translated_text='',
            source_lang=source_langs[0],
            target_lang=target_langs[0],
            job_id=job_id
        )]