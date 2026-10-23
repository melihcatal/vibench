from google.cloud import aiplatform
from typing import List
import numpy as np


def embed_script(
    script: str, model_id: str = "textembedding-gecko@latest"
) -> List[float]:
    aiplatform.init(project=aiplatform.default_project())

    model = aiplatform.Model(model_name=model_id)
    endpoint = model.deployed_endpoints[0]

    response = endpoint.predict(instances=[{"content": script}])

    return response.predictions[0]


def batch_embed_scripts(
    scripts: List[str], model_id: str = "textembedding-gecko@latest"
) -> List[List[float]]:
    aiplatform.init(project=aiplatform.default_project())

    model = aiplatform.Model(model_name=model_id)
    endpoint = model.deployed_endpoints[0]

    response = endpoint.predict(instances=[{"content": script} for script in scripts])

    return response.predictions
