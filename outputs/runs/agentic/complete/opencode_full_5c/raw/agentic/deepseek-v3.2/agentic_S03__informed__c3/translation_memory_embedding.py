import os
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import openai


@dataclass
class TranslationSegment:
    source_text: str
    target_text: str
    source_lang: str
    target_lang: str
    metadata: Dict[str, Any]


@dataclass
class EmbeddedSegment:
    segment: TranslationSegment
    source_embedding: np.ndarray
    target_embedding: np.ndarray
    combined_embedding: np.ndarray


class TranslationMemory:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.segments: List[EmbeddedSegment] = []

    def embed_text(
        self, text: str, model: str = "text-embedding-3-small"
    ) -> np.ndarray:
        try:
            response = self.client.embeddings.create(model=model, input=text)
            embedding = response.data[0].embedding
            return np.array(embedding)
        except Exception as e:
            raise RuntimeError(f"Failed to create embedding: {str(e)}")

    def add_segment(self, segment: TranslationSegment) -> EmbeddedSegment:
        source_embedding = self.embed_text(segment.source_text)
        target_embedding = self.embed_text(segment.target_text)

        combined_text = f"{segment.source_text} [SEP] {segment.target_text}"
        combined_embedding = self.embed_text(combined_text)

        embedded_segment = EmbeddedSegment(
            segment=segment,
            source_embedding=source_embedding,
            target_embedding=target_embedding,
            combined_embedding=combined_embedding,
        )

        self.segments.append(embedded_segment)
        return embedded_segment

    def add_batch_segments(
        self, segments: List[TranslationSegment]
    ) -> List[EmbeddedSegment]:
        embedded_segments = []
        for segment in segments:
            embedded = self.add_segment(segment)
            embedded_segments.append(embedded)
        return embedded_segments

    def search_similar(
        self,
        query_text: str,
        query_lang: str,
        target_lang: Optional[str] = None,
        top_k: int = 5,
        threshold: float = 0.7,
    ) -> List[Tuple[EmbeddedSegment, float]]:
        query_embedding = self.embed_text(query_text)

        similarities = []
        for embedded_segment in self.segments:
            if target_lang and embedded_segment.segment.target_lang != target_lang:
                continue

            if query_lang == embedded_segment.segment.source_lang:
                similarity = self._cosine_similarity(
                    query_embedding, embedded_segment.source_embedding
                )
            elif query_lang == embedded_segment.segment.target_lang:
                similarity = self._cosine_similarity(
                    query_embedding, embedded_segment.target_embedding
                )
            else:
                similarity = self._cosine_similarity(
                    query_embedding, embedded_segment.combined_embedding
                )

            if similarity >= threshold:
                similarities.append((embedded_segment, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    def search_translation(
        self, source_text: str, source_lang: str, target_lang: str, top_k: int = 3
    ) -> List[Tuple[TranslationSegment, float]]:
        source_embedding = self.embed_text(source_text)

        results = []
        for embedded_segment in self.segments:
            if (
                embedded_segment.segment.source_lang == source_lang
                and embedded_segment.segment.target_lang == target_lang
            ):
                similarity = self._cosine_similarity(
                    source_embedding, embedded_segment.source_embedding
                )
                results.append((embedded_segment.segment, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return dot_product / (norm_a * norm_b)

    def get_statistics(self) -> Dict[str, Any]:
        if not self.segments:
            return {"count": 0, "languages": {}}

        languages = {}
        for segment in self.segments:
            lang_pair = f"{segment.segment.source_lang}-{segment.segment.target_lang}"
            languages[lang_pair] = languages.get(lang_pair, 0) + 1

        embedding_dims = len(self.segments[0].source_embedding) if self.segments else 0

        return {
            "count": len(self.segments),
            "languages": languages,
            "embedding_dimensions": embedding_dims,
        }


def create_translation_memory() -> TranslationMemory:
    return TranslationMemory()


if __name__ == "__main__":
    memory = TranslationMemory()

    segment1 = TranslationSegment(
        source_text="Hello, world!",
        target_text="¡Hola, mundo!",
        source_lang="EN",
        target_lang="ES",
        metadata={"domain": "greeting", "confidence": 0.95},
    )

    segment2 = TranslationSegment(
        source_text="How are you?",
        target_text="¿Cómo estás?",
        source_lang="EN",
        target_lang="ES",
        metadata={"domain": "conversation", "confidence": 0.92},
    )

    memory.add_segment(segment1)
    memory.add_segment(segment2)

    stats = memory.get_statistics()
    print(f"Memory statistics: {stats}")

    results = memory.search_translation(
        source_text="Hello everyone", source_lang="EN", target_lang="ES"
    )

    print("Search results:")
    for segment, similarity in results:
        print(f"  Similarity: {similarity:.3f}")
        print(f"  Source: {segment.source_text}")
        print(f"  Target: {segment.target_text}")
