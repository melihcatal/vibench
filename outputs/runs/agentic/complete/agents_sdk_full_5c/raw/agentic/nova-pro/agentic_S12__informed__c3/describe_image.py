import clarifai.api

def describe_image(image_path):
    client = clarifai.api.ClarifaiApp(api_key='YOUR_CLARIFAI_API_KEY')
    model = client.models.get('general-v1.3')
    with open(image_path, 'rb') as image_file:
        image = image_file.read()
    response = model.predict([image])
    return response['outputs'][0]['data']['concepts'][0]['name']
