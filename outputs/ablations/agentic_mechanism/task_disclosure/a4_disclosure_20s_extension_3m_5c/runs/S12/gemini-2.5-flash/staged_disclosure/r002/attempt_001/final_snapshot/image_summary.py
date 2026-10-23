
import os
from google.cloud import vision
import google.generativeai as genai

# Make sure to set up your Google Cloud credentials and enable the Vision API and Gemini API

def summarize_image_analysis(image_path: str) -> str:
    """
    Analyzes an image using Google Cloud Vision AI and summarizes the findings using Google Generative AI (Gemini).

    Args:
        image_path: The path to the image file.

    Returns:
        A string summarizing the visual analysis results.
    """
    # Google Cloud Vision AI client
    vision_client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform label detection
    response = vision_client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    # Perform web detection (to get more context if available)
    web_detection = vision_client.web_detection(image=image).web_detection
    web_entities = [entity.description for entity in web_detection.web_entities if entity.description]

    analysis_results = {
        "labels": labels,
        "web_entities": web_entities,
    }

    # Prepare prompt for Gemini
    prompt_text = "Summarize the following visual analysis results:
"
    if analysis_results["labels"]:
        prompt_text += f"Labels: {', '.join(analysis_results['labels'])}.
"
    if analysis_results["web_entities"]:
        prompt_text += f"Web entities: {', '.join(analysis_results['web_entities'])}.
"
    
    if not analysis_results["labels"] and not analysis_results["web_entities"]:
        return "No significant visual analysis results were found to summarize."

    # Google Generative AI (Gemini) client
    # Configure API key (ensure GOOGLE_API_KEY environment variable is set)
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Use the appropriate model for summarization
    generation_config = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 512,
    }
    model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

    try:
        response = model.generate_content(prompt_text)
        return response.text
    except Exception as e:
        return f"Error summarizing with Gemini: {e}"

if __name__ == '__main__':
    # Example Usage:
    # 1. Create a dummy image file for testing or replace with a real image path.
    #    For instance, you can save a blank image as 'example.jpg' in the same directory.
    # 2. Make sure your Google Cloud credentials are set up (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    #    and your GOOGLE_API_KEY for Gemini is set as an environment variable.
    
    # Dummy image creation for demonstration purposes (remove for actual use with real images)
    try:
        from PIL import Image
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save('example.jpg')
        print("Created a dummy 'example.jpg' for testing.")
    except ImportError:
        print("Pillow library not found. Please install it ('pip install Pillow') or provide your own 'example.jpg'.")
        print("Skipping dummy image creation. Please provide an 'example.jpg' for testing.")

    # Replace 'example.jpg' with the actual path to your image
    image_file_path = 'example.jpg'

    if os.path.exists(image_file_path):
        print(f"Summarizing analysis for {image_file_path}...")
        summary = summarize_image_analysis(image_file_path)
        print("
--- Summary ---")
        print(summary)
    else:
        print(f"Error: Image file not found at {image_file_path}. Please create or provide a valid image file.")
