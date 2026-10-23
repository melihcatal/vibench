from google.cloud import translate_v3

def translate_html(html, target_language_code):
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('my-project-id', 'us-central1')
    response = client.translate_text(parent, [html], target_language_code)
    return response.translations[0].translated_text

if __name__ == '__main__':
    html = '<html><body><h1>Hello, World!</h1></body></html>'
    translated_html = translate_html(html, 'es')
    print(translated_html)