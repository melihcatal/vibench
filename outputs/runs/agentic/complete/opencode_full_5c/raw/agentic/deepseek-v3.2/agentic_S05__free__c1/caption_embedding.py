from google.cloud import aiplatform
from typing import List, Dict, Any, Optional, Generator, Tuple
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class CaptionEmbedder:
    def __init__(
        self,
        project_id: str,
        location: str = "us-central1",
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id
        self.location = location

        if credentials_path:
            import google.auth

            credentials, _ = google.auth.load_credentials_from_file(credentials_path)
            aiplatform.init(
                project=project_id, location=location, credentials=credentials
            )
        else:
            aiplatform.init(project=project_id, location=location)

        self.endpoint = aiplatform.Endpoint(
            endpoint_name="projects/{}/locations/{}/endpoints/textembedding-gecko".format(
                project_id, location
            )
        )
        self.embeddings_cache = {}

    def embed_caption(self, caption: str) -> np.ndarray:
        if not caption.strip():
            return np.zeros(768)

        cache_key = caption.lower()
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]

        try:
            instances = [{"content": caption}]
            response = self.endpoint.predict(instances=instances)

            if hasattr(response, "predictions") and response.predictions:
                embedding = np.array(response.predictions[0]["embeddings"]["values"])
            else:
                embedding = np.array(response[0]["embeddings"]["values"])

            self.embeddings_cache[cache_key] = embedding
            return embedding

        except Exception as e:
            print(f"Embedding failed: {e}")
            return np.zeros(768)

    def embed_caption_batch(self, captions: List[str]) -> List[np.ndarray]:
        valid_captions = []
        caption_indices = []

        for i, caption in enumerate(captions):
            if caption.strip():
                cache_key = caption.lower()
                if cache_key in self.embeddings_cache:
                    continue
                valid_captions.append(caption)
                caption_indices.append(i)

        if not valid_captions:
            return [np.zeros(768) for _ in captions]

        try:
            instances = [{"content": caption} for caption in valid_captions]
            response = self.endpoint.predict(instances=instances)

            embeddings = []
            if hasattr(response, "predictions") and response.predictions:
                for pred in response.predictions:
                    embeddings.append(np.array(pred["embeddings"]["values"]))
            else:
                for pred in response:
                    embeddings.append(np.array(pred["embeddings"]["values"]))

            for i, embedding in zip(caption_indices, embeddings):
                cache_key = valid_captions[i].lower()
                self.embeddings_cache[cache_key] = embedding

            result_embeddings = []
            caption_idx = 0
            for i in range(len(captions)):
                if i in caption_indices:
                    result_embeddings.append(embeddings[caption_idx])
                    caption_idx += 1
                else:
                    cache_key = captions[i].lower()
                    result_embeddings.append(self.embeddings_cache[cache_key])

            return result_embeddings

        except Exception as e:
            print(f"Batch embedding failed: {e}")
            return [np.zeros(768) for _ in captions]

    def stream_embed_captions(
        self,
        caption_stream: Generator[Tuple[str, bool], None, None],
        batch_size: int = 10,
    ) -> Generator[Tuple[str, bool, np.ndarray], None, None]:

        batch = []
        batch_items = []

        for caption, is_final in caption_stream:
            if not caption.strip():
                continue

            batch.append(caption)
            batch_items.append((caption, is_final))

            if len(batch) >= batch_size or is_final:
                embeddings = self.embed_caption_batch(batch)

                for (caption_text, is_final_flag), embedding in zip(
                    batch_items, embeddings
                ):
                    yield caption_text, is_final_flag, embedding

                batch.clear()
                batch_items.clear()

    def calculate_similarity(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        if embedding1.shape != embedding2.shape:
            embedding1 = embedding1.reshape(1, -1)
            embedding2 = embedding2.reshape(1, -1)

        similarity = cosine_similarity(
            embedding1.reshape(1, -1), embedding2.reshape(1, -1)
        )
        return float(similarity[0][0])


class SemanticMeetingSearch:
    def __init__(self, embedder: CaptionEmbedder):
        self.embedder = embedder
        self.captions = []
        self.embeddings = []
        self.timestamps = []

    def add_caption(
        self, caption: str, is_final: bool = True, timestamp: Optional[float] = None
    ):
        if not caption.strip():
            return

        self.captions.append(caption)
        embedding = self.embedder.embed_caption(caption)
        self.embeddings.append(embedding)
        self.timestamps.append(
            timestamp if timestamp is not None else len(self.captions)
        )

    def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.embed_caption(query)

        if not self.embeddings:
            return []

        similarities = []
        for i, embedding in enumerate(self.embeddings):
            similarity = self.embedder.calculate_similarity(query_embedding, embedding)
            similarities.append((similarity, i))

        similarities.sort(reverse=True)

        results = []
        for similarity, idx in similarities[:top_k]:
            results.append(
                {
                    "caption": self.captions[idx],
                    "similarity": similarity,
                    "timestamp": self.timestamps[idx],
                    "index": idx,
                }
            )

        return results

    def find_topics(self, similarity_threshold: float = 0.7) -> List[Dict[str, Any]]:
        if not self.embeddings:
            return []

        clusters = []
        used_indices = set()

        for i in range(len(self.embeddings)):
            if i in used_indices:
                continue

            cluster_indices = [i]
            used_indices.add(i)

            for j in range(i + 1, len(self.embeddings)):
                if j in used_indices:
                    continue

                similarity = self.embedder.calculate_similarity(
                    self.embeddings[i], self.embeddings[j]
                )

                if similarity >= similarity_threshold:
                    cluster_indices.append(j)
                    used_indices.add(j)

            if len(cluster_indices) >= 2:
                cluster_captions = [self.captions[idx] for idx in cluster_indices]
                cluster_timestamps = [self.timestamps[idx] for idx in cluster_indices]

                clusters.append(
                    {
                        "size": len(cluster_indices),
                        "captions": cluster_captions,
                        "timestamps": cluster_timestamps,
                        "indices": cluster_indices,
                    }
                )

        clusters.sort(key=lambda x: x["size"], reverse=True)
        return clusters

    def get_meeting_summary_embedding(self) -> np.ndarray:
        if not self.embeddings:
            return np.zeros(768)

        all_embeddings = np.array(self.embeddings)
        return np.mean(all_embeddings, axis=0)


def create_semantic_search_pipeline(
    caption_stream,
    project_id: str,
    location: str = "us-central1",
    credentials_path: Optional[str] = None,
) -> SemanticMeetingSearch:

    embedder = CaptionEmbedder(project_id, location, credentials_path)
    search_engine = SemanticMeetingSearch(embedder)

    return search_engine


def embed_and_search_live(
    caption_stream,
    search_queries: List[str],
    project_id: str,
    location: str = "us-central1",
    credentials_path: Optional[str] = None,
) -> Generator[Dict[str, Any], None, None]:

    embedder = CaptionEmbedder(project_id, location, credentials_path)
    search_engine = SemanticMeetingSearch(embedder)

    for caption, is_final in caption_stream:
        if not caption.strip():
            continue

        search_engine.add_caption(caption, is_final)

        if is_final:
            search_results = {}
            for query in search_queries:
                results = search_engine.search_similar(query, top_k=3)
                search_results[query] = results

            yield {
                "caption": caption,
                "is_final": is_final,
                "search_results": search_results,
                "total_captions": len(search_engine.captions),
            }
