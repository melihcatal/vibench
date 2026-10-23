import os
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
visual_recognition = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=authenticator
)

def describe_image(image_path):
    with open(image_path, 'rb') as images_file:
        classes = visual_recognition.classify(
            images_file=images_file).get_result()
    return classes