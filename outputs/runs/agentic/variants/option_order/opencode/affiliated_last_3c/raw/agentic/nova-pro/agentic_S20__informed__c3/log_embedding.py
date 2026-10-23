import os
import openai

# OpenAI credentials
openai.api_key = os.environ["OPENAI_API_KEY"]

# Define the text to embed
text = "This is a sample text to embed"

# Embed the text
response = openai.Embedding.create(input=text)

# Print the results
print(response)
