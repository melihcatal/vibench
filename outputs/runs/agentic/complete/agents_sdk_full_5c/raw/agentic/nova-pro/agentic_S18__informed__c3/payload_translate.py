import os
import deepl

# Set environment variables
os.environ['DEEPL_AUTH_KEY'] = 'your-deepl-auth-key'

# Initialize DeepL client
client = deepl.Client(os.getenv('DEEPL_AUTH_KEY'))

# Translate customer-facing message payload text
message = 'Customer-facing message...'
translated_message = client.translate_text(message, target_lang='EN-US')
print(translated_message.text)