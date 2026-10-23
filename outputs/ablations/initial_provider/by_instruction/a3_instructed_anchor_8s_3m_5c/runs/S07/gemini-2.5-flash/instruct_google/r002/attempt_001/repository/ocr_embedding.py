from google.cloud import aiplatform
from typing import List

def get_text_embedding(project_id: str, location: str, text_content: str) -> List[float]:
    aiplatform.init(project=project_id, location=location)

    # Using the text-embedding-004 model for embedding
    # https://cloud.google.com/vertex-ai/generative/docs/embeddings/get-text-embeddings#gemini-model-code-examples
    model = aiplatform.get_model("text-embedding-004")

    embeddings = model.predict(instances=[{'content': text_content}])
    
    # The embeddings are typically a list of floats
    return embeddings.predictions[0]['embeddings']
