import boto3

def check_unsafe_text(image_path):
    rekognition_client = boto3.client('rekognition')
    with open(image_path, 'rb') as image:
        image_bytes = image.read()
    response = rekognition_client.detect_moderation_labels(
        Image={'Bytes': image_bytes}
    )
    unsafe_labels = [label['Name'] for label in response['ModerationLabels'] if label['ModerationLabelConfidence'] > 50]
    return unsafe_labels

if __name__ == '__main__':
    image_path = 'path/to/your/image.jpg'
    unsafe_text = check_unsafe_text(image_path)
    if unsafe_text:
        print(f'Unsafe text detected: {unsafe_text}')
    else:
        print('No unsafe text detected.')