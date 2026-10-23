
import os
from openai import OpenAI

def stream_completion(prompt: str):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    stream = client.chat.completions.create(
        model="gpt-4", # Using a concrete model identifier
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")

if __name__ == "__main__":
    print("Streaming completion from OpenAI (gpt-4):")
    stream_completion("Write a short poem about the beauty of nature.")
