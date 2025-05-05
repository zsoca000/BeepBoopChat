import wave
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


def process_wav(input_wav, threshold=0.1):
    # Open the WAV file
    with wave.open(input_wav, 'rb') as wav_file:
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        
        # Read the frames
        frames = wav_file.readframes(n_frames)
        
        # Convert to numpy array
        dtype = np.int16 if sample_width == 2 else np.uint8
        audio_data = np.frombuffer(frames, dtype=dtype)
        
        # Normalize to range -1 to 1 if 16-bit
        if sample_width == 2:
            audio_data = audio_data / 32768.0
        elif sample_width == 1:
            audio_data = (audio_data - 128) / 128.0  # Convert unsigned 8-bit to range -1 to 1
        
        # Apply thresholding
        binary_output = (np.abs(audio_data) > threshold).astype(int)
        
        # Convert to string
        output_string = ''.join(map(str, binary_output))
        
    return output_string

def adjust_binary_string(binary_string, min_zero_length=1000):
    modified_string = list(binary_string)
    
    start = 0
    while start < len(modified_string):
        if modified_string[start] == '0':
            end = start
            while end < len(modified_string) and modified_string[end] == '0':
                end += 1
            
            if (end - start) < min_zero_length:
                for i in range(start, end):
                    modified_string[i] = '1'
            
            start = end
        else:
            start += 1
    
    return ''.join(modified_string)

def calculate_segment_lengths(binary_string):
    segment_lengths = []
    start = 0
    
    while start < len(binary_string):
        end = start
        while end < len(binary_string) and binary_string[end] == binary_string[start]:
            end += 1
        
        segment_lengths.append((binary_string[start], end - start))
        start = end
    
    return segment_lengths

def convert_to_morse(segment_lengths):
    morse_code = ""
    for seg_type, length in segment_lengths:
        if seg_type == '1':
            if 1000 <= length <= 4000:
                morse_code += '.'
            elif 6000 <= length <= 10000:
                morse_code += '-'
        elif seg_type == '0':
            if 1000 <= length <= 4000:
                morse_code += ''
            elif 7000 <= length <= 10000:
                morse_code += ' '
            elif 15000 <= length:
                morse_code += ' / '
    return morse_code

def wav2morse(input_wav, threshold=0.1, min_zero_length=1000):
    binary_string = process_wav(input_wav, threshold)
    adjusted_string = adjust_binary_string(binary_string, min_zero_length)
    segment_lengths = calculate_segment_lengths(adjusted_string)
    morse_code = convert_to_morse(segment_lengths)
    return morse_code

def morse2qso(morse_code):
    MORSE_DICT = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
        '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
        '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
        '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
        '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
        '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
        '---..': '8', '----.': '9', '.-.-.': '='
    }
    words = morse_code.strip().split(' / ')
    decoded_message = ''
    for word in words:
        letters = word.split()
        decoded_message += ''.join(MORSE_DICT.get(letter, '?') for letter in letters) + ' '
    return decoded_message.strip()

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
                "content": "You are a translator who converts QSO code - english translator. You return just the translated messages, without explanations and notes."
            },
            {
                "role": "user",
                "content": f"Please translate the following message into detailed human-readable prose. Please do not explain it. {QSO_text}"
            }
        ]
    )
    return completion.choices[0].message.content

def text2qso(text,partner_name,your_name,watt,antenna,location,readability,strength,tone):
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
                "content": "You are a english-QSO translator. You return just the translated messages, without explanations and notes."
            },
            {
                "role": "user",
                "content": f"Please translate the following message into CW-style QSO code. Please do not explain it. Message: Dear {partner_name}. My name is {your_name}, my location is {location}, I'm running {watt} watt of power with a {antenna} antenna. The recived signal readability was {readability}, strength was {strength} and tone was {tone}. {text}"
            }
        ]
    )
    return completion.choices[0].message.content

def qso2morse(text):
    morse_code_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..',
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
        'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
        'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
        's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
        'y': '-.--', 'z': '--..',
        '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
        '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
        '.': '.-.-.-', ',': '--..--', '?': '..--..', "'": '.----.', '!': '-.-.--',
        '/': '-..-.', '(': '-.--.', ')': '-.--.-', '&': '.-...', ':': '---...',
        ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-', '_': '..--.-',
        '"': '.-..-.', '$': '...-..-', '@': '.--.-.', ' ': '/'
    }
    morse_code = ' '.join(morse_code_dict[char] for char in text if char in morse_code_dict)
    return morse_code

def morse2wav(morse_code, filename='output.wav', wpm=20, freq=600, sample_rate=44100):
    # Timing based on WPM
    dot_duration = 1.2 / wpm           # in seconds
    dash_duration = 3 * dot_duration
    intra_char_space = dot_duration
    inter_char_space = 3 * dot_duration
    inter_word_space = 7 * dot_duration

    def tone(duration):
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        return 0.5 * np.sin(2 * np.pi * freq * t)

    def silence(duration):
        return np.zeros(int(sample_rate * duration))

    audio = np.array([], dtype=np.float32)
    for word in morse_code.strip().split(' / '):
        for char in word.split(' '):
            for symbol in char:
                if symbol == '.':
                    audio = np.concatenate((audio, tone(dot_duration)))
                elif symbol == '-':
                    audio = np.concatenate((audio, tone(dash_duration)))
                audio = np.concatenate((audio, silence(intra_char_space)))
            audio = np.concatenate((audio, silence(inter_char_space - intra_char_space)))
        audio = np.concatenate((audio, silence(inter_word_space - inter_char_space)))

    # Normalize and save
    audio = np.int16(audio * 32767)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())


if __name__ == '__main__':
   
    # input_path = 'src/examples/2.wav'
    # morse_code = wav2morse(input_path)
    # print(f"Decoded Morse Code: {morse_code}") 
    # qso = morse2qso(morse_code)
    # print(f"Qso Code: {qso}") 
    # text = qso2text(qso)
    # print(f"Plain Text: {text}") 

    
    partner_name = 'Gábor'
    your_name = 'Zsolt'
    location = 'Budapest'
    watt = 10
    antenna = 'W3DZZ'
    readability, strength, tone = 5, 9, 9

    text = 'My family is fine, how is your wife and your children?'

    print('TEXT:', text,'\n')
    qso = text2qso(text,partner_name,your_name,watt,antenna,location,readability,strength,tone)
    print('QSO :', qso,'\n')
    text = qso2text(qso)
    print('TEXT:', text,'\n')



