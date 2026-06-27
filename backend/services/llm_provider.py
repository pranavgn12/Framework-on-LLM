import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)


def generate_response(

    contents,

    system_instruction=None

):

    messages = []

    if system_instruction:

        messages.append({

            "role": "system",

            "content": system_instruction

        })

    if isinstance(contents, str):

        messages.append({

            "role": "user",

            "content": contents

        })

    else:

        messages.extend(contents)

    response = client.chat.completions.create(

        model=os.getenv(

            "GROQ_MODEL",

            "llama-3.1-8b-instant"

        ),

        messages=messages,

        temperature=0.3,

        max_completion_tokens=1024,

        top_p=1

    )

    return response.choices[0].message.content