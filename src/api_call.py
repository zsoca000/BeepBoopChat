from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


def qso2text(QSO_text):

    api_key = os.getenv("API_KEY")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )
    completion = client.chat.completions.create(
        model="deepseek/deepseek-chat-v3-0324:free",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You are a translator who converts ham radio messages into detailed human-readable prose, returning only the translated message."
            },
            {
                "role": "user",
                "content": QSO_text
            }
        ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    qso = 'HA5KDR DE HA5OGL = R DR Greg ES MNI TNX FER RPRT = UR RST IS 579 = MY QTH IS BUDAPEST = MY NAME IS Levente = PWR 10 WATT = ANT W3DZZ = WX COLD = NW QRU = TNX FER UFB QSO'
    
    print(qso2text(qso))


