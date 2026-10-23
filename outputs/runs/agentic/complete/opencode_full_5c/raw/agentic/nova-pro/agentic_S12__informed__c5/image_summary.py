import google.generativeai as genai


def image_summary(image_path):
    genai.configure(api_key="GOOGLE_API_KEY")
    model = genai.GenerativeModel("gemini-pro-vision")
    with open(image_path, "rb") as image:
        image_data = image.read()
    response = model.generate_content([image_data])
    return response.text
