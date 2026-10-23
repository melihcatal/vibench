import google.cloud.storage


def summarize_onboarding_state(user_id):
    storage_client = google.cloud.storage.Client()
    bucket = storage_client.get_bucket("onboarding-states")
    blob = bucket.blob(user_id)
    content = blob.download_as_text()
    return content
