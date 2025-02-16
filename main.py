"""
Created by: Marco Astorga
Email: marcoastorga.g@gmail.com
Date: 2025-02-15
Description: This module handles integration with the Gemini API for Pokémon identification.
License: MIT License
"""
# main.py
import os
from fastapi import FastAPI, File, HTTPException, UploadFile
import pokebase as pb
from pokebase import cache 
from gemini import identify_pokemon_from_image 
from googletrans import Translator

app = FastAPI()
translator = Translator()
POKEMON_NOT_FOUND_DETAIL = "Pokémon not found"

def get_pokemon(pokemon_id: int, lang: str = "en"):
    try:
        # Get the Pokémon and species data
        pokemon = pb.pokemon(pokemon_id)
        species = pb.pokemon_species(pokemon_id)
    except Exception:
        # Return a 404 error if the Pokémon is not found
        raise HTTPException(status_code=404, detail=POKEMON_NOT_FOUND_DETAIL)
    
    # Search for the description in the specified language; fallback to English if necessary
    description = None
    for entry in species.flavor_text_entries:
        if entry.language.name == lang:
            description = entry.flavor_text.replace("\n", " ").replace("\f", " ")
            break
    if not description:
        for entry in species.flavor_text_entries:
            if entry.language.name == "en":
                description = entry.flavor_text.replace("\n", " ").replace("\f", " ")
                break

    # Prepare the response with Pokémon details
    return {
        "id": pokemon.id,
        "name": pokemon.name,
        "description": description,
        "types": [t.type.name for t in pokemon.types],
        "height": pokemon.height,
        "weight": pokemon.weight,
        "stats": {stat.stat.name: stat.base_stat for stat in pokemon.stats},
        "abilities": [ability.ability.name for ability in pokemon.abilities],
        "images": {
            "front_default": pokemon.sprites.front_default,
            "back_default": pokemon.sprites.back_default,
            "front_shiny": pokemon.sprites.front_shiny,
            "back_shiny": pokemon.sprites.back_shiny,
        }
    }

@app.post("/identify_pokemon")
async def identify_pokemon_endpoint(file: UploadFile = File(...), lang: str = "en"):
    """
    Endpoint to identify a Pokémon from an image using Gemini.
    """
    # Save the uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    try:
        # Use Gemini to get the Pokémon id
        pokemon_id = identify_pokemon_from_image(temp_path, file.content_type)
        if pokemon_id == 0:
            translation = translator.translate(POKEMON_NOT_FOUND_DETAIL, src="en", dest=lang)
            raise HTTPException(status_code=404, detail=translation.text or POKEMON_NOT_FOUND_DETAIL)
        # Return Pokémon information
        return get_pokemon(pokemon_id, lang) # get_pokemon function
    finally:
        # Remove the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)


# Example  

# class Item(BaseModel):
#     text: str
#     is_done: bool = False
    
# items = [] # store items in memory
        

# @app.post("/items/")
# async def create_item(item: Item):
#     items.append(item) # add item to list
#     return item # return item

# @app.get("/items/",response_model=list[Item] )
# async def list_items(limit: int = 10): # limit the number of items to return
#     return items[0:limit] # return items up to limit

# @app.get("/items/{item_id}", response_model=Item)
# async def get_items(item_id: int) -> Item:
#    if item_id < len(items):
#        return items[item_id]
#    else:
#          raise HTTPException(status_code=404, detail=f"Item {item_id} not found")