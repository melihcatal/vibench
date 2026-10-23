from google.cloud import storage


def onboarding_summary(user_id, summary):
    client = storage.Client()
    bucket = client.get_bucket('onboarding-summaries')
    blob = bucket.blob(f'{user_id}.txt')
    blob.upload_from_string(summary)
    return {'status': 'success'}