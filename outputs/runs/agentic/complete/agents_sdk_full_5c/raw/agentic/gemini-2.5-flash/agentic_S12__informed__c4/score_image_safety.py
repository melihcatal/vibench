
import os
from clarifai.client.stub import ClarifaiStub
from clarifai.client.sdk_pb.clarifai.api.resources import resources_pb2
from clarifai.client.sdk_pb.clarifai.api.service import service_pb2, service_pb2_grpc

def score_image_safety(image_bytes: bytes) -> dict:
    """Checks an image for unsafe content using Clarifai's moderation model."""
    pat = os.environ.get("CLARIFAI_PAT")
    if not pat:
        raise ValueError("CLARIFAI_PAT environment variable must be set.")

    stub = ClarifaiStub(pat=pat)

    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            model_id="moderation-recognition",  # Clarifai's general moderation model
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        image=resources_pb2.Image(
                            base64=image_bytes
                        )
                    )
                )
            ]
        ),
        metadata=(("authorization", f"Key {pat}"),)
    )

    if post_model_outputs_response.status.code != 10000:
        raise Exception(f"Clarifai API error: {post_model_outputs_response.status.description}")

    # Extract relevant safety scores
    safety_scores = {}
    for concept in post_model_outputs_response.outputs[0].data.concepts:
        safety_scores[concept.name] = concept.value
    
    return safety_scores

if __name__ == '__main__':
    # This is example usage.
    # Ensure CLARIFAI_PAT is set.
    # Replace with actual image content for testing.
    try:
        with open("example.jpg", "rb") as image_file:
            content = image_file.read()
        safety_scores = score_image_safety(content)
        print("Image Safety Scores:", safety_scores)
    except FileNotFoundError:
        print("example.jpg not found. Please create an example image file or provide actual image content.")
    except Exception as e:
        print(f"An error occurred: {e}")
