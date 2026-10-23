import os
from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform_v1beta1.types import HarmCategory, HarmProbability, Content, GenerateContentRequest
from google.cloud.aiplatform_v1beta1.services.prediction_service import PredictionServiceClient

def prompt_safety(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_LOCATION')
    model_name = config.get('model_name') or 'gemini-pro' # Using gemini-pro for content moderation

    client_options = {'api_endpoint': f'{location}-aiplatform.googleapis.com'}
    client = PredictionServiceClient(client_options=client_options)

    endpoint = client.endpoint_path(
        project=project_id,
        location=location,
        publisher='google',
        model=model_name
    )

    # The safety settings are typically part of the request to a generative model.
    # For a dedicated safety check, we can send a prompt and check the `safety_ratings` in the response.
    
    # Construct the request to the generative model to get safety ratings
    request = GenerateContentRequest(
        contents=[
            Content(role='user', parts=[
                Content.Part(text=payload['text'])
            ])
        ]
    )

    response = client.generate_content(
        endpoint=endpoint,
        formatted_request=request
    )
    
    is_safe = True
    safety_ratings = []
    if response.candidates:
        candidate = response.candidates[0]
        if candidate.safety_ratings:
            for rating in candidate.safety_ratings:
                safety_ratings.append({'category': HarmCategory(rating.category).name, 'probability': HarmProbability(rating.probability).name})
                if rating.probability > HarmProbability.NEGLIGIBLE:
                    is_safe = False
    
    return {'is_safe': is_safe, 'safety_ratings': safety_ratings, 'checked_text': payload['text']}
