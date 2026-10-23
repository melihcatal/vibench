import os
from ibm_watsonx_ai import watsonxai
from ibm_watsonx_ai.embeddings import EmbeddingsV1

class CaptionEmbedder:
    def __init__(self):
        api_key = os.getenv('WATSONX_API_KEY')
        project_id = os.getenv('WATSONX_PROJECT_ID')
        self.client = EmbeddingsV1(api_key=api_key, service_url='https://api.ibm.com/watsonx/v1/embeddings', project_id=project_id)

    def embed(self, text):
        """Embed a caption chunk using watsonx.ai Slate embeddings."""
        response = self.client.create_embeddings(model_id='slate.125m.blue.If12', text=text)
        embeddings = response.get('embeddings')
        return embeddings[0]['values'] if embeddings else []

if __name__ == '__main__':
    embedder = CaptionEmbedder()
    vec = embedder.embed('Meeting recap: discussed Q1 targets and roadmap.",
    print('Caption embedding:', vec)
