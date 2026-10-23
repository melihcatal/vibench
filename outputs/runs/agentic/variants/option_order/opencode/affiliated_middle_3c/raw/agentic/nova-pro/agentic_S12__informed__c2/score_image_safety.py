import os
import clarifai.rest

# Initialize the client
clarifai_pat = os.getenv("CLARIFAI_PAT")
client = clarifai.rest.ClarifaiApp(pat=clarifai_pat)


def score_image_safety(image_path):
    with open(image_path, "rb") as image_file:
        model = client.models.get("nsfw-v1.1")
        response = model.predict_by_bytes(image_file.read())
        return response["outputs"][0]["data"]["concepts"]
