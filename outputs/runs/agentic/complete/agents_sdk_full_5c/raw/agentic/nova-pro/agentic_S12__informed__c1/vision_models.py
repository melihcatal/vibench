from google.cloud import vision
from ibm_watson import VisualRecognitionV3
from azure.ai.vision import ImageAnalysisClient
from clarifai_grpc.grpc.api import resources_pb2, service_pb2

def normalize_google_labels(labels):
    return [{'name': label.description, 'score': label.score} for label in labels]

def normalize_ibm_classes(classes):
    return [{'name': class_result['class'], 'score': class_result['score']} for class_result in classes['images'][0]['classifiers'][0]['classes']]

def normalize_azure_text(text):
    return text.text

def normalize_clarifai_moderation(moderation):
    return [{'name': concept.name, 'value': concept.value} for concept in moderation.outputs[0].data.concepts]

