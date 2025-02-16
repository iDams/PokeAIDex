"""
Created by: Marco Astorga
Email: marcoastorga.g@gmail.com
Date: 2025-02-15
Description: This module handles integration with the Gemini API for Pokémon identification.
License: MIT License
"""
# gemini.py
import os
import google.generativeai as genai

# Configure the Gemini API key from the environment variable
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Function to upload a file to Gemini
def upload_to_gemini(path: str, mime_type: str = None):
    """
    Upload the file to Gemini and return the file object.
    """
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

# Configuration for response generation
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Create the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    system_instruction=(
        "Just respond with the Pokémon id that you see in the image. "
        "If you don't recognize it, return an id of 0."
    ),
)

# Function to identify the Pokémon from an image
def identify_pokemon_from_image(file_path: str, mime_type: str) -> int:
    """
    Send the image to the Gemini model and return the Pokémon id.
    """
    gemini_file = upload_to_gemini(file_path, mime_type) # Upload the file to Gemini
    chat_session = model.start_chat(
        history=[
            {"role": "user", "parts": [gemini_file]},
            {"role": "model", "parts": ["1\n"]},
        ]
    )
    response = chat_session.send_message("Analyze the image and tell me the Pokémon ID.")
    try:
        return int(response.text.strip())
    except ValueError:
        return 0
