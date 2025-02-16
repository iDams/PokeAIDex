# Pokémon Identification API

This API uses FastAPI to identify a Pokémon from an image and retrieve its details. It integrates with Gemini (for image analysis) and Pokebase (for fetching Pokémon data). The API supports language translation for error messages via Google Translate.

## Features

- **Identify Pokémon from Images:**  
  Send an image to the `/identify_pokemon` endpoint, and the API will use Gemini to analyze the image and return the Pokémon's ID.

- **Retrieve Pokémon Details:**  
  Once the Pokémon ID is obtained, details such as name, description, types, stats, and images are fetched from Pokebase.

- **Language Support:**  
  Error messages and descriptions can be translated based on a provided language code (default is English).

## Requirements

- Python 3.10 or higher
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) (for running the ASGI server)
- [Pokebase](https://github.com/PokeAPI/pokebase)
- [googletrans==4.0.0rc1](https://pypi.org/project/googletrans/)
- [google-generativeai](https://pypi.org/project/google-generativeai/) (or the correct package name for Gemini integration)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>


## Installation

   > python -m venv venv
source venv/bin/activate