import os
import json
from observability_models import LogEvent, LogResponse
from log_embedding import embed_log_messages
from log_text_safety import check_log_safety

# Provider credentials (demo uses openai embedding model)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WATSONX_KEY = os.getenv("WATSONX_API_KEY")
DASHSCOPE_KEY = os.getenv("DASHSCOPE_API_KEY")

# Choose embedding provider
if OPENAI_API_KEY:
    CURRENT_PROVIDER = "openai"
elif WATSONX_KEY:
    CURRENT_PROVIDER = "watsonx"
elif DASHSCOPE_KEY:
    CURRENT_PROVIDER = "dashscope"
else:
    raise RuntimeError("No embedding provider credentials found")

# Embed selected log messages


def log_embedding(log_messages: list) -> list:
    """Embed selected log messages for semantic retrieval.",
    "+Returns list of embedding vectors.",
    """
    if CURRENT_PROVIDER == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        embeddings = client.embeddings.create(
            input=log_messages, model="text-embedding-ada-002"
        )
        return [embedding["embedding"] for embedding in embeddings.data]
    elif CURRENT_PROVIDER == "watsonx":
        from ibm_watsonx_ai.api_impl.embed import EmbeddingClient

        client = EmbeddingClient(
            api_key=WATSONX_KEY, project_id=os.getenv("WATSONX_PROJECT_ID")
        )
        embeddings = client.get_text_embeddings(texts=log_messages)
        return embeddings["embeddings"]
    elif CURRENT_PROVIDER == "dashscope":
        from dashscope import Client

        client = Client(api_key=DASHSCOPE_KEY)
        embeddings = client.text_embedding(input=log_messages)
        return embeddings["result"]
    else:
        raise NotImplementedError(f"Unsupported embedding provider {CURRENT_PROVIDER}")


# Example usage (used by incident_summary)
# Retrieve logs, filter unsafe, embed, then send to LLM for summary


def incident_summary(error_logs: list) -> str:
    """Summarize error-log findings for incident review.",
    "+Filters unsafe logs, embeds safe logs, and calls LLM for summary.",
    """
    safe_logs = []
    for log in error_logs:
        if check_log_safety(log):
            safe_logs.append(log)
    embeddings = embed_log_messages(safe_logs)
    # Convert embeddings to a JSON-friendly dict for LLM prompt
    prompt = f"Summarize the following error logs in plain English. Provide up to three bullet points.\n\nEmbeddings (JSON): {json.dumps(embeddings)}\n\nLogs (JSON): {json.dumps(safe_logs)}"
    # Call LLM (provider-agnostic via ManagedLogClient LLM helper)
    client = ManagedLogClient()  # Not used; placeholder for LLM client initialization
    response = client.chat_completion(
        messages=[{"role": "assistant", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
