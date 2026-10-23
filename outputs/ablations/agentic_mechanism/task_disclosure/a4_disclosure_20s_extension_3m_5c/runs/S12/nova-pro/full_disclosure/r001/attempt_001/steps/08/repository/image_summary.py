import boto3


class ImageSummary:
    def __init__(self):
        self.rekognition_client = boto3.client('rekognition', region_name='us-west-2', aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY')

    def summarize_image(self, image_bytes):
        response = self.rekognition_client.detect_labels(
            Image={'Bytes': image_bytes},
            MaxLabels=10
        )
        labels = [label['Name'] for label in response['Labels']]
        return ' '.join(labels)
