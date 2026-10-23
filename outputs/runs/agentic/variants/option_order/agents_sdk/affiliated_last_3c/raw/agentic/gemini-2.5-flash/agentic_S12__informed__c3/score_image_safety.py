import os
from clarifai.client.image import Image as ClarifaiImage
from clarifai.client.workflow import Workflow

def score_image_safety(image_url: str):
    """Checks an image for unsafe or policy-sensitive visual content using Clarifai."""
    # CLARIFAI_PAT must be set as an environment variable
    # Using a pre-built Clarifai workflow for moderation
    # Example workflow: "moderation-workflow" or similar public moderation models
    # Find suitable workflow IDs in Clarifai platform
    workflow_id = "moderation-workflow" # A generic moderation workflow ID

    try:
        workflow = Workflow(workflow_id=workflow_id, pat=os.environ.get("CLARIFAI_PAT"))
        
        # ClarifaiImage can also take bytes for local files
        image_prediction = workflow.predict_by_url(image_url, input_type="image")
        
        # The output structure depends on the specific moderation workflow.
        # This is a general way to extract concepts from outputs.
        safety_scores = {}
        for output in image_prediction.outputs:
            if output.data.concepts:
                for concept in output.data.concepts:
                    safety_scores[concept.name] = concept.value
        return safety_scores
    except Exception as e:
        print(f"Error scoring image safety with Clarifai: {e}")
        return None

if __name__ == '__main__':
    # This example requires CLARIFAI_PAT to be set.
    # For demonstration:
    # print(score_image_safety("https://samples.clarifai.com/face-det.jpg"))
    pass
