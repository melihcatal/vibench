# Embed Moderation Rationales for Case Retrieval
from sentence_transformers import SentenceTransformer
from typing import List


class ModerationReasonEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_rationales(self, rationales: List[str]) -> List[List[float]]:
        """Embed moderation rationales using Sentence Transformers."""
        return self.model.encode(rationales, convert_to_tensor=False).tolist()