from google.cloud import storage


def image_asset_archive(bucket_name, image_path, caption):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(image_path)
    blob.upload_from_filename(image_path)
    blob.metadata = {"caption": caption}
    blob.patch()
