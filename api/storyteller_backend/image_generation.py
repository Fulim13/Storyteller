import base64
from django.contrib.messages import api
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage
import getpass
import os
import requests
import uuid

# Stability API configuration
# engine_id = "stable-diffusion-xl-1024-v1-0"
# api_host = os.getenv("API_HOST", "https://api.stability.ai")


def generate_character_image(name, appearance, biography, genre="realistic",):
    """
    Generate a detailed character image using Stability AI's text-to-image model.

    Args:
        name (str): The name of the character.
        appearance (str): Physical description of the character.
        biography (str): Backstory of the character.
        genre (str): The style of the character illustration.

    Returns:
        list: Paths to the generated image files.
    """
    # 1. Create the model:
    chat = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

    # 2. Generate the image prompt:
    image_prompt = chat.invoke(
        [
            SystemMessage(
                content=f"""
                A highly detailed character portrait in {genre} style.
                The character is {name}, described as {appearance}.
                They have a background in {biography}.
                Focus on their distinctive traits and emotional depth,
                creating a realistic and lifelike image with rich textures and lighting.
                """
            )
        ]
    ).content

    # 3. Generate the image using Stability API:
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        timeout=60,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
        },
        json={
            "text_prompts": [{"text": image_prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception(f"Non-200 response: {response.text}")

    # 4. Save and return the generated images:
    data = response.json()
    image_paths = []

    for i, image in enumerate(data["artifacts"]):
        filename = f"{uuid.uuid4().hex[:7]}.png"
        with open(filename, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
        image_paths.append(filename)

    return image_paths
