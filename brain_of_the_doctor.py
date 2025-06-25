# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup GROQ API key
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
import base64
from groq import Groq

# Function to base64 encode an image file
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Function to send multimodal query to the Groq LLM
def analyze_image_with_query(query, model, encoded_image=None):
    if not GROQ_API_KEY:
        raise ValueError("Missing GROQ_API_KEY. Set it in your environment.")

    client = Groq(api_key=GROQ_API_KEY)

    if encoded_image:
        # multimodal: text + image
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    }
                ],
            }
        ]
    else:
        # text only
        messages = [
            {
                "role": "user",
                "content": query  # just plain text
            }
        ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
