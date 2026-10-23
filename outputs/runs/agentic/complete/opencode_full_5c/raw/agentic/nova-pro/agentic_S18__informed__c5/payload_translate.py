import boto3

# Create a Translate client
translate = boto3.client("translate")

# Define the text to translate
text = "Text to translate"

# Translate the text
result = translate.translate_text(
    Text=text, SourceLanguageCode="en", TargetLanguageCode="es"
)

# Print the translated text
print(result["TranslatedText"])
