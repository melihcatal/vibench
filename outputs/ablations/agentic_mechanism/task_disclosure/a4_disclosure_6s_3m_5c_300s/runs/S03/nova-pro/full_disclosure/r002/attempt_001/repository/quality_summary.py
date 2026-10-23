import boto3

def summarize_translation_quality(translation_job_id):
    translate_client = boto3.client('translate')
    response = translate_client.get_translation_job(JobId=translation_job_id)
    quality_metrics = response['TranslationJobProperties']['Settings']['QualityEstimation']
    summary = {
        'JobId': translation_job_id,
        'QualityMetrics': quality_metrics
    }
    return summary

# Example usage:
# translation_job_id = 'your-translation-job-id'
# print(summarize_translation_quality(translation_job_id))