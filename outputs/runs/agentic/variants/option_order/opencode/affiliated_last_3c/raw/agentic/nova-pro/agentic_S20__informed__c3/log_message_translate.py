import os
from google.cloud import translate_v2 as translate

# Google Cloud Translation credentials
client = translate.Client()

# Define the text to translate
text = "This is a sample text to translate"

# Translate the text
response = client.translate(text, target_language="es")

# Print the results
print(response)
