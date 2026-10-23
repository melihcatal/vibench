from google.cloud import translate_v3

def translate_markup(input_markup, target_language_code):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/YOUR_PROJECT_ID/locations/global"

    # Split the input markup into text and tags
    text_content = ''
    tags = []
    current_tag = ''
    in_tag = False

    for char in input_markup:
        if char == '<':
            in_tag = True
            current_tag = ''
        elif char == '>':
            in_tag = False
            tags.append(current_tag)
        elif in_tag:
            current_tag += char
        else:
            text_content += char

    # Translate the text content
    response = client.translate_text(parent=parent, contents=[text_content], mime_type='text/plain', target_language_code=target_language_code)
    translated_text = response.translations[0].translated_text

    # Reconstruct the translated markup
    translated_markup = ''
    for tag in tags:
        translated_markup += tag
    translated_markup += translated_text

    return translated_markup

# Example usage
input_markup = '<p>Hello, world!</p>'
target_language_code = 'es'
translated_markup = translate_markup(input_markup, target_language_code)
print(translated_markup)