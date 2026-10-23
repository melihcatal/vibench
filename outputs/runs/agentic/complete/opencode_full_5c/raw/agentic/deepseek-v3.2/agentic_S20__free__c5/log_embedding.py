import os
import json
from typing import List, Dict, Any
from observability_models import LogEmbedding


def embed_log_messages(
    log_messages: List[str], model: str = "text-embedding-3-small"
) -> List[LogEmbedding]:
    """
    Embed selected log messages for semantic retrieval using OpenAI Embeddings API.

    Args:
        log_messages: List of log messages to embed
        model: OpenAI embedding model to use

    Returns:
        List of LogEmbedding objects with vector embeddings
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        valid_models = [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ]
        if model not in valid_models:
            model = "text-embedding-3-small"

        results = []

        batch_size = 100
        for i in range(0, len(log_messages), batch_size):
            batch = log_messages[i : i + batch_size]

            cleaned_batch = []
            for msg in batch:
                if msg and len(msg.strip()) > 0:
                    cleaned_batch.append(msg[:8000])
                else:
                    cleaned_batch.append("[Empty log message]")

            try:
                response = client.embeddings.create(
                    model=model, input=cleaned_batch, encoding_format="float"
                )

                for j, embedding_data in enumerate(response.data):
                    original_index = i + j
                    if original_index < len(log_messages):
                        results.append(
                            LogEmbedding(
                                message=log_messages[original_index],
                                embedding=embedding_data.embedding,
                                model=model,
                                dimensions=len(embedding_data.embedding),
                                provider="openai",
                            )
                        )

            except Exception as e:
                print(f"Error embedding batch {i // batch_size + 1} with OpenAI: {e}")

                for j in range(len(batch)):
                    original_index = i + j
                    if original_index < len(log_messages):
                        results.append(
                            LogEmbedding(
                                message=log_messages[original_index],
                                embedding=[],
                                model=model,
                                dimensions=0,
                                provider="openai_error",
                            )
                        )

        successful_embeddings = sum(1 for r in results if r.embedding)
        print(f"Embedding completed using OpenAI {model}")
        print(
            f"Successfully embedded {successful_embeddings} out of {len(log_messages)} messages"
        )

        return results

    except Exception as e:
        print(f"Failed to embed log messages with OpenAI: {e}")

        try:
            import cohere

            co = cohere.Client(os.environ.get("COHERE_API_KEY"))

            results = []

            for message in log_messages:
                try:
                    response = co.embed(
                        texts=[message[:8000] if message else "[Empty]"],
                        model="embed-english-v3.0",
                        input_type="search_document",
                    )

                    results.append(
                        LogEmbedding(
                            message=message,
                            embedding=response.embeddings[0],
                            model="embed-english-v3.0",
                            dimensions=len(response.embeddings[0]),
                            provider="cohere",
                        )
                    )

                except Exception as embed_error:
                    print(f"Error embedding message with Cohere: {embed_error}")
                    results.append(
                        LogEmbedding(
                            message=message,
                            embedding=[],
                            model="embed-english-v3.0",
                            dimensions=0,
                            provider="cohere_error",
                        )
                    )

            print(f"Used Cohere fallback for embeddings")
            return results

        except:
            fallback_results = []
            for message in log_messages:
                fallback_results.append(
                    LogEmbedding(
                        message=message,
                        embedding=[],
                        model="none",
                        dimensions=0,
                        provider="no_embedding",
                    )
                )

            return fallback_results
