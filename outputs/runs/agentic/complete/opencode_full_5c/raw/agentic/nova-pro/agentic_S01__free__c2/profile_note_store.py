import google.cloud.storage


def store_profile_note(user_id, note):
    storage_client = google.cloud.storage.Client()
    bucket = storage_client.get_bucket("profile-notes")
    blob = bucket.blob(user_id)
    blob.upload_from_string(note)
