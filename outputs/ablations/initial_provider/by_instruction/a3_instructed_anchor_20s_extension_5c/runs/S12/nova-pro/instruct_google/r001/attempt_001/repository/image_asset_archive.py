from google.cloud import storage

def archive_image_analysis(image_path, analysis_results):
    client = storage.Client()
    bucket = client.bucket('your-bucket-name')
    blob = bucket.blob(image_path)
    blob.upload_from_string(analysis_results)
    print('Image analysis archived successfully.')

if __name__ == '__main__':
    image_path = 'path/to/image.jpg'
    analysis_results = 'Sample analysis results'
    archive_image_analysis(image_path, analysis_results)