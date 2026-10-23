"""
script_embedding.py - Embed narration scripts for voice-asset search using Google Cloud Vertex AI.

Uses the Vertex AI text-embedding API to generate embeddings for narration
scripts, enabling semantic search and similarity matching across voice
asset libraries. Supports batch embedding generation and vector comparison.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


@dataclass
class ScriptEmbedding:
    """Embedding result for a single narration script."""

    script_text: str
    embedding: List[float]
    dimensions: int

    def cosine_similarity(self, other: "ScriptEmbedding") -> float:
        """
        Compute cosine similarity between this embedding and another.

        Args:
            other: Another ScriptEmbedding to compare against.

        Returns:
            Cosine similarity score in range [-1.0, 1.0].
        """
        if len(self.embedding) != len(other.embedding):
            raise ValueError("Embedding dimensions must match.")

        dot_product = sum(a * b for a, b in zip(self.embedding, other.embedding))
        mag_a = sum(a * a for a in self.embedding) ** 0.5
        mag_b = sum(b * b for b in other.embedding) ** 0.5

        if mag_a == 0 or mag_b == 0:
            return 0.0

        return dot_product / (mag_a * mag_b)


@dataclass
class VoiceAssetEmbedding:
    """Stored embedding for a voice asset in the search index."""

    asset_id: str
    script_text: str
    voice_name: str
    language_code: str
    embedding: ScriptEmbedding
    metadata: Dict[str, str] = field(default_factory=dict)


class ScriptEmbedder:
    """
    Generates embeddings for narration scripts using Google Cloud Vertex AI.

    Provider: Google Cloud Vertex AI via vertexai SDK.
    Model: textembedding-gecko (latest version).
    API endpoint: aiplatform.googleapis.com / us-central1-aiplatform.googleapis.com
    """

    DEFAULT_MODEL = "textembedding-gecko@latest"
    DEFAULT_DIMENSIONS = 768

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: str = "us-central1",
        credentials_path: Optional[str] = None,
        model_name: str = DEFAULT_MODEL,
    ):
        """
        Initialize Vertex AI text embedding client.

        Args:
            project_id: Google Cloud project ID. Falls back to GOOGLE_CLOUD_PROJECT env.
            location: GCP region (e.g. "us-central1").
            credentials_path: Path to Google service account JSON file.
            model_name: Vertex AI embedding model name.
        """
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        self.model_name = model_name
        self.location = location

        init_kwargs = {
            "project": self.project_id,
            "location": location,
        }
        if credentials_path:
            import google.auth

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        aiplatform.init(**init_kwargs)

        self.model = TextEmbeddingModel.from_pretrained(model_name)

    def embed_text(
        self,
        text: str,
        dimensionality: Optional[int] = None,
    ) -> ScriptEmbedding:
        """
        Generate an embedding for a single narration script.

        Provider: Google Cloud Vertex AI textembedding-gecko model.
        API endpoint: aiplatform.googleapis.com

        Args:
            text: Narration script text to embed.
            dimensionality: Optional output dimensionality (up to 768).

        Returns:
            ScriptEmbedding with vector values.

        Raises:
            ValueError: If text is empty.
            google.api_core.exceptions.GoogleAPIError: On Vertex AI failure.
        """
        if not text or not text.strip():
            raise ValueError("Text must not be empty.")

        params: Dict = {}
        if dimensionality:
            params["dimensionality"] = dimensionality

        result = self.model.get_embeddings(
            texts=[text.strip()],
            **params,
        )

        if result and len(result) > 0:
            vector = result[0].values
            return ScriptEmbedding(
                script_text=text.strip(),
                embedding=vector,
                dimensions=len(vector),
            )

        raise RuntimeError("No embedding returned from Vertex AI model.")

    def embed_batch(
        self,
        texts: List[str],
        dimensionality: Optional[int] = None,
        batch_size: int = 5,
    ) -> List[ScriptEmbedding]:
        """
        Generate embeddings for a batch of narration scripts.

        Args:
            texts: List of narration script texts.
            dimensionality: Optional output dimensionality.
            batch_size: Number of texts per API call (max 250 for textembedding-gecko).

        Returns:
            List of ScriptEmbedding objects.
        """
        all_embeddings: List[ScriptEmbedding] = []
        cleaned_texts = [t.strip() for t in texts if t and t.strip()]

        for i in range(0, len(cleaned_texts), batch_size):
            batch = cleaned_texts[i:i + batch_size]
            params: Dict = {}
            if dimensionality:
                params["dimensionality"] = dimensionality

            results = self.model.get_embeddings(
                texts=batch,
                **params,
            )

            for j, result in enumerate(results):
                all_embeddings.append(
                    ScriptEmbedding(
                        script_text=batch[j],
                        embedding=result.values,
                        dimensions=len(result.values),
                    )
                )

        return all_embeddings

    def find_similar_scripts(
        self,
        query_text: str,
        indexed_assets: List[VoiceAssetEmbedding],
        top_k: int = 5,
        threshold: float = 0.0,
    ) -> List[Tuple[VoiceAssetEmbedding, float]]:
        """
        Find the most similar narration scripts in the voice asset index.

        Args:
            query_text: Query narration script.
            indexed_assets: Pre-indexed VoiceAssetEmbedding objects.
            top_k: Number of top results to return.
            threshold: Minimum similarity score to include.

        Returns:
            List of (VoiceAssetEmbedding, similarity_score) tuples sorted by score.
        """
        query_embedding = self.embed_text(query_text)

        scored: List[Tuple[VoiceAssetEmbedding, float]] = []
        for asset in indexed_assets:
            similarity = query_embedding.cosine_similarity(asset.embedding)
            if similarity >= threshold:
                scored.append((asset, similarity))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]


def embed_narration_script(
    text: str,
    project_id: Optional[str] = None,
    location: str = "us-central1",
    credentials_path: Optional[str] = None,
    model_name: str = ScriptEmbedder.DEFAULT_MODEL,
) -> ScriptEmbedding:
    """
    Embed a narration script for voice-asset search using Vertex AI.

    Provider: Google Cloud Vertex AI via vertexai SDK.
    Model: textembedding-gecko@latest.
    API endpoint: aiplatform.googleapis.com

    Args:
        text: Narration script text.
        project_id: Google Cloud project ID.
        location: GCP region.
        credentials_path: Path to Google service account JSON.
        model_name: Vertex AI embedding model.

    Returns:
        ScriptEmbedding with vector representation.
    """
    embedder = ScriptEmbedder(
        project_id=project_id,
        location=location,
        credentials_path=credentials_path,
        model_name=model_name,
    )
    return embedder.embed_text(text)


def build_voice_asset_index(
    asset_data: List[Dict[str, str]],
    project_id: Optional[str] = None,
    location: str = "us-central1",
    credentials_path: Optional[str] = None,
) -> List[VoiceAssetEmbedding]:
    """
    Build a searchable index of voice assets by embedding their narration scripts.

    Args:
        asset_data: List of dicts with keys: asset_id, script_text, voice_name, language_code.
        project_id: Google Cloud project ID.
        location: GCP region.
        credentials_path: Path to Google service account JSON.

    Returns:
        List of VoiceAssetEmbedding objects with computed embeddings.
    """
    embedder = ScriptEmbedder(
        project_id=project_id,
        location=location,
        credentials_path=credentials_path,
    )

    texts = [a.get("script_text", "") for a in asset_data if a.get("script_text")]
    embeddings = embedder.embed_batch(texts)

    index: List[VoiceAssetEmbedding] = []
    embed_idx = 0

    for asset in asset_data:
        if not asset.get("script_text"):
            continue

        voice_asset = VoiceAssetEmbedding(
            asset_id=asset.get("asset_id", f"asset-{embed_idx}"),
            script_text=asset["script_text"],
            voice_name=asset.get("voice_name", ""),
            language_code=asset.get("language_code", "en-US"),
            embedding=embeddings[embed_idx],
            metadata={k: v for k, v in asset.items() if k not in ("asset_id", "script_text", "voice_name", "language_code")},
        )
        index.append(voice_asset)
        embed_idx += 1

    return index


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
    creds = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    embedder = ScriptEmbedder(
        project_id=project,
        credentials_path=creds,
    )

    emb = embedder.embed_text("Welcome to the daily news briefing.")
    print(f"Embedding dimensions: {emb.dimensions}")
    print(f"First 5 values: {emb.embedding[:5]}")

    batch_embs = embedder.embed_batch([
        "Breaking news: major developments today.",
        "Weather forecast for the weekend.",
        "Sports highlights from last night's game.",
    ])
    print(f"Batch embeddings: {len(batch_embs)}")
