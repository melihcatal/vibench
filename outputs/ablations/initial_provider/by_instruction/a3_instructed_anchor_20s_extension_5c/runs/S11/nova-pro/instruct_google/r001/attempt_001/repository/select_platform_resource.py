from google.ai.generativelanguage import GenerativeLanguageServiceClient

def select_platform_resource():
    client = GenerativeLanguageServiceClient()
    model = 'models/text-bison-001'
    print(f'Selected model: {model}')