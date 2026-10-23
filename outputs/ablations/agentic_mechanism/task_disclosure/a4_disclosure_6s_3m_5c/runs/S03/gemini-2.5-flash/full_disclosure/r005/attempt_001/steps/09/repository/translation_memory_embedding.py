import os
from typing import List

from google.cloud import aiplatform
from google.protobuf import struct_pb2

def embed_text_segments(
    project_id: str,
    location: str,
    text_segments: List[str],
) -> List[List[float]]:
    """Embeds a list of text segments using Google Cloud Vertex AI's text-embedding-gecko model.

    Args:
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        text_segments: A list of strings to embed.

    Returns:
        A list of lists of floats, where each inner list is the embedding for a corresponding text segment.
    """

    aiplatform.init(project=project_id, location=location)

    # Initialize the prediction client
    prediction_client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )
    endpoint = (
        f"projects/{project_id}/locations/{location}/endpoints/text-embedding-gecko"
    )

    instances = []
    for text in text_segments:
        instance = struct_pb2.Value()
        instance.struct_value.fields["content"].string_value = text
        instance.struct_value.fields["mimeType"].string_value = "text/plain"
        instances.append(instance)

    response = prediction_client.predict(endpoint=endpoint, instances=instances)

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(list(prediction["embeddings"]["values"]))
    
    return embeddings

if __name__ == '__main__':
    # Example usage (replace with your actual project ID and desired location)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    LOCATION = "us-central1"  # e.g., "us-central1"

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        segments_to_embed = [
            "Hello world.",
            "This is a test sentence.",
            "Another sentence for embedding.",
        ]

        print(f"Embedding {len(segments_to_embed)} text segments...")
        try:
            result_embeddings = embed_text_segments(PROJECT_ID, LOCATION, segments_to_embed)
            for i, embedding in enumerate(result_embeddings):
                print(f"Embedding for segment {i+1}: {embedding[:5]}...") # Print first 5 dimensions
        except Exception as e:
            print(f"An error occurred: {e}")
