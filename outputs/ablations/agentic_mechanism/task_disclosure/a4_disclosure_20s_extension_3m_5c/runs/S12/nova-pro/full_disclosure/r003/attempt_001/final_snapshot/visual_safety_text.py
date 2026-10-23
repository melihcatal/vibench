import boto3

def check_visual_labels(labels):
    comprehend = boto3.client('comprehend')
    toxic_content_detected = False
    for label in labels:
        response = comprehend.detect_toxic_content(
            TextSegments=[
                {
                    'Text': label
                }
            ]
        )
        if response['ToxicContentDetected']:
            toxic_content_detected = True
            break
    return toxic_content_detected