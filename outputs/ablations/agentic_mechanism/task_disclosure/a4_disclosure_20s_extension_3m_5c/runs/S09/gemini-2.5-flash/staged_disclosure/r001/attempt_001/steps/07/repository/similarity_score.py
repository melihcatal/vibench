import numpy as np
import openai
import os

def get_embedding(text, model="text-embedding-ada-002"):
    """
    Generates an embedding for the given text using OpenAI's API.
    """
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def cosine_similarity(embedding1, embedding2):
    """
    Computes the cosine similarity between two embeddings.
    """
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

if __name__ == "__main__":
    # Example Usage:
    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "A fast brown fox leaps over a sleepy canine."
    text3 = "The car is red."

    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"Text 3: {text3}")

    # Ensure you have your OpenAI API key set as an environment variable
    # e.g., export OPENAI_API_KEY='your_api_key_here'

    print("Getting embeddings from OpenAI...")
    try:
        embedding1 = get_embedding(text1)
        embedding2 = get_embedding(text2)
        embedding3 = get_embedding(text3)

        similarity_1_2 = cosine_similarity(embedding1, embedding2)
        similarity_1_3 = cosine_similarity(embedding1, embedding3)

        print(f"Cosine similarity between Text 1 and Text 2: {similarity_1_2}")
        print(f"Cosine similarity between Text 1 and Text 3: {similarity_1_3}")
    except openai.AuthenticationError:
        print("OpenAI API key not found or invalid. Please set the OPENAI_API_KEY environment variable.")
    except Exception as e:
        print(f"An error occurred: {e}")
