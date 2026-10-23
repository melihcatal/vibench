"""
[SAME-SCENARIO] describe_image.py - generates a short visual description for an image
"""

import os
import google.generativeai as genai
from PIL import Image

def describe_image(image_path: str) -> str:
    """
    Generates a description for an image using Google Gemini.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        img = Image.open(image_path)
        prompt = "Describe this image in one sentence."
        
        response = model.generate_content([prompt, img])
        
        return response.text.strip()
    except Exception as e:
        print(f"Error generating description: {e}")
        return ""
