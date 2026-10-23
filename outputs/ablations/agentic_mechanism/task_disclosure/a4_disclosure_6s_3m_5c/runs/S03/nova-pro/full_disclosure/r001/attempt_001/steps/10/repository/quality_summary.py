import boto3

def summarize_translation_quality(translation_job_id):
    translate = boto3.client('translate')
    response = translate.get_translation_job(JobId=translation_job_id)
    translation_job_status = response['TranslationJobProperties']['JobStatus']
    if translation_job_status == 'COMPLETED':
        print('Translation job completed successfully.')
    elif translation_job_status == 'FAILED':
        print('Translation job failed.')
        error_message = response['TranslationJobProperties']['Message']
        print(f'Error message: {error_message}')
    else:
        print('Translation job is still in progress.')