import os
from google.cloud import vision
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from azure.ai.vision import ImageAnalysisClient, AzureKeyCredential
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc

GOOGLE_VISION_CLIENT = vision.ImageAnnotatorClient()
IBM_VISION_CLIENT = VisualRecognitionV3(
    version='2018-03-19',
    authenticator=IAMAuthenticator(os.getenv('IBM_API_KEY_ID'))
)
AZURE_VISION_CLIENT = ImageAnalysisClient(
    os.getenv('AZURE_VISION_ENDPOINT'), AzureKeyCredential(os.getenv('AZURE_VISION_KEY'))
)
CLARIFAI_VISION_CLIENT = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
CLARIFAI_VISION_METADATA = (('authorization', f'Key {os.getenv(