from openai import OpenAI

def qso2text(QSO_text):

    # instruction = "Please do not use enumeration in the answer, and do not act Translate briefly the following ham radio QSO message into human-readable plain text (like a chat message)"
    # content = f'{instruction} : {QSO_text}'

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
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


