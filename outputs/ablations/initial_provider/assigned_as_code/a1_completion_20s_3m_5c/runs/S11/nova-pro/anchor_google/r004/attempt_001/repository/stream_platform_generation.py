import os
from google.cloud import aiplatform

def stream_platform_generation(model):
    parameters = {
        'temperature': 0.2,
        'max_output_tokens': 256,
    }
    response = model.predict(instances=["Write a story about a robot."], params=parameters)
    for prediction in response.predictions:
        yield prediction['output']

model = select_platform_resource()
for output in stream_platform_generation(model):
    print(output)