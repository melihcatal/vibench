import vision_client

def describe_image(image_path):
    # Use Google Cloud Vision to generate a short description of the image content
    # Google Cloud Vision's `image_properties` provides a `description` field
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.image_properties(image=image)
    # The description is in the `latent_semantic_description` field
    description = response.latent_semantic_description or ""
    return description.strip()
