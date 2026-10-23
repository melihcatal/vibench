import vertexai
from vertexai.language_models import TextGenerationModel

def invoke_model():
    vertexai.init(project="your-project-id", location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict("Hello, world!")
    print(response.text)