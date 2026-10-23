import os
from google.cloud import aiplatform

def collect_platform_metadata(model):
    parameters = {
        'temperature': 0.2,
        'max_output_tokens': 256,
    }
    response = model.predict(instances=["Write a story about a robot."], params=parameters)
    return {
        'output': response.predictions[0]['output'],
        'metadata': response.metadata,
    }

model = select_platform_resource()
metadata = collect_platform_metadata(model)
print(metadata)