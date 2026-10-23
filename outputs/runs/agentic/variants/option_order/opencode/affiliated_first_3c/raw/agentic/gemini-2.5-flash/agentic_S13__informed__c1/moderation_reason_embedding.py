import os
import google.generativeai as genai


def moderation_reason_embedding(reason_text):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # The embedding model to use. For text embeddings, typically 'embedding-001' or similar.
    # Check Gemini API documentation for the most current and appropriate model name.
    model_name = "models/embedding-001"

    response = genai.embed_content(
        model=model_name, content=reason_text, task_type="RETRIEVAL_DOCUMENT"
    )
    return response["embedding"]


if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        reason = "The content was flagged due to high toxicity and profanity scores, exceeding the platform's safety thresholds."
        embedding = moderation_reason_embedding(reason)
        print(
            f"Embedding for reason '{reason}' (first 10 elements): {embedding[:10]}..."
        )

        reason_2 = "This message was allowed as it did not violate any safety policies."
        embedding_2 = moderation_reason_embedding(reason_2)
        print(
            f"Embedding for reason '{reason_2}' (first 10 elements): {embedding_2[:10]}..."
        )
