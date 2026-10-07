from google import genai
from config import config_obj

client = genai.Client(api_key=config_obj.gemini_api_key)


def get_answer_from_gemini(prompt: str):

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )
    return interaction.output_text