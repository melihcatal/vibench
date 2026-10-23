from embed_text import embed_text
from embeddings_models import cosine_similarity

def compute_embedding_similarity(text1: str, text2: str, model_name: str = "models/text-embedding-004") -> float:
    """
    Embeds two texts and computes the cosine similarity between their embeddings.
    """
    embedding1 = embed_text(text1, model_name=model_name)
    embedding2 = embed_text(text2, model_name=model_name)
    return cosine_similarity(embedding1, embedding2)

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # To run:
    # export GOOGLE_API_KEY='your_api_key_here'
    # python similarity_score.py
    text_a = "The cat sat on the mat."
    text_b = "A feline rested on the rug."
    text_c = "The car drove down the road."

    try:
        similarity_ab = compute_embedding_similarity(text_a, text_b)
        similarity_ac = compute_embedding_similarity(text_a, text_c)
        print(f"Similarity between \'{text_a}\' and \'{text_b}': {similarity_ab:.4f}")
        print(f"Similarity between \'{text_a}\' and \'{text_c}': {similarity_ac:.4f}")

        text_d = "Artificial intelligence is a rapidly growing field."
        text_e = "AI is advancing quickly."
        similarity_de = compute_embedding_similarity(text_d, text_e)
        print(f"Similarity between \'{text_d}\' and \'{text_e}': {similarity_de:.4f}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
