import boto3

def summarize_translation_quality(translation_job_id):
    translate_client = boto3.client('translate')
    response = translate_client.get_translation_job(JobId=translation_job_id)
    if response['TranslationJobProperties']['JobStatus'] == 'COMPLETED':
        print('Translation job completed successfully.')
    else:
        print(f'Translation job failed with status: {response[