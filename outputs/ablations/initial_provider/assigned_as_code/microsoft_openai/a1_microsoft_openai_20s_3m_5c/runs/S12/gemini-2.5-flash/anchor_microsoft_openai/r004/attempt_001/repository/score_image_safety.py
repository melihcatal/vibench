from clarifai.client.workflow import Workflow
import os

def score_image_safety(payload, config=None):
    config = config or {}
    # You need to set your CLARIFAI_PAT (Personal Access Token) as an environment variable.
    # For example: export CLARIFAI_PAT='YOUR_CLARIFAI_PAT_HERE'
    workflow_url = config.get('clarifai_workflow_url', "https://clarifai.com/clarifai/main/workflows/moderation-workflow")
    
    workflow = Workflow(workflow_url)

    # The predict method takes a list of inputs. For image bytes, you can pass them directly.
    # The input type is automatically detected by the Clarifai SDK.
    prediction_response = workflow.predict_by_bytes(
        image_bytes=payload['image_bytes'], 
        input_type="image"
    )

    # Parse the prediction response to extract safety scores
    safety_scores = {}
    if prediction_response.results:
        for concept in prediction_response.results[0].outputs[0].data.concepts:
            safety_scores[concept.name] = concept.value
            
    return {'safety_scores': safety_scores}
