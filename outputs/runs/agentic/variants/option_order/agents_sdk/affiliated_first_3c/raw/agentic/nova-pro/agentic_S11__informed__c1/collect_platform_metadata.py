from vertexai.language_models import TextGenerationModel

def collect_platform_metadata():
    model = TextGenerationModel.from_pretrained('text-bison@001')
    response = model.predict('Hello, world!')
    return response, response.metadata