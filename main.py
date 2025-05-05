import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QLineEdit, QComboBox, QSpinBox, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from src.utils import wav2morse, morse2qso, qso2text, text2qso, qso2morse, morse2wav

import json

def decode_morse_from_audio(file_path):
    if file_path.endswith('.wav'):
        
        decode_steps = {}
        decode_steps['wav_path'] = file_path
        
        print('\t - wav -> morse')
        morse_code = wav2morse(file_path)
        decode_steps['morse'] = morse_code
        
        print('\t - morse -> qso')
        qso_code = morse2qso(morse_code)
        decode_steps['qso'] = qso_code
        
        print('\t - qso -> text')
        text = qso2text(qso_code)
        decode_steps['text'] = text 
        
        with open('log/last_decode.json', 'w') as json_file:
            json.dump(decode_steps, json_file, indent=4)
        
        return text
    else:
        return 'Error: Unsupported file format. Please upload a .wav file.'

def encode_text_to_morse_audio(text, partner_name, your_name, watt, antenna, location, readability, strength, tone, output_path):
    encode_steps = {}
    
    encode_steps['text'] = {}
    encode_steps['text']['message'] = text
    encode_steps['text']['partner_name'] = partner_name
    encode_steps['text']['your_name'] = your_name
    encode_steps['text']['watt'] = watt
    encode_steps['text']['antenna'] = antenna
    encode_steps['text']['location'] = location
    encode_steps['text']['readability'] = readability
    encode_steps['text']['strength'] = strength
    encode_steps['text']['tone'] = tone

    print('\t - QSO -> text')
    qso_text = text2qso(text, partner_name, your_name, watt, antenna, location, readability, strength, tone)
    encode_steps['qso'] = qso_text

    print('\t - text -> morse')
    morse_code = qso2morse(qso_text)
    encode_steps['morse'] = morse_code

    print('\t - morse -> wav')
    morse2wav(morse_code, output_path)
    encode_steps['wav_path'] = output_path

    with open('log/last_encode.json', 'w') as json_file:
        json.dump(encode_steps, json_file, indent=4)

    return output_path

class MorseCodeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.uploadButton = QPushButton("Upload Morse Audio")
        self.uploadButton.clicked.connect(self.load_audio)
        layout.addWidget(self.uploadButton)
        
        self.decodedText = QTextEdit()
        layout.addWidget(QLabel("Decoded Text:"))
        layout.addWidget(self.decodedText)
        
        self.replyText = QTextEdit()
        layout.addWidget(QLabel("Your Reply:"))
        layout.addWidget(self.replyText)

        # Add "Your name" and "Partner name" text boxes
        nameLayout = QHBoxLayout()
        self.yourNameInput = QLineEdit()
        self.yourNameInput.setText("Joe")  # Set default value for "Your name"

        self.partnerNameInput = QLineEdit()
        self.partnerNameInput.setText("John")  # Set default value for "Partner name"
        nameLayout.addWidget(QLabel("Your name:"))
        nameLayout.addWidget(self.yourNameInput)
        nameLayout.addWidget(QLabel("Partner name:"))
        nameLayout.addWidget(self.partnerNameInput)
        layout.addLayout(nameLayout)

        # Add "Location" text box and "Antenna" dropdown
        locationAntennaLayout = QHBoxLayout()
        self.locationInput = QLineEdit()
        self.locationInput.setText("Budapest")  # Set default value for "Location"
        self.antennaDropdown = QComboBox()
        self.antennaDropdown.addItem("W3DZZ")
        locationAntennaLayout.addWidget(QLabel("Location:"))
        locationAntennaLayout.addWidget(self.locationInput)
        locationAntennaLayout.addWidget(QLabel("Antenna:"))
        locationAntennaLayout.addWidget(self.antennaDropdown)
        layout.addLayout(locationAntennaLayout)

        # Add integer inputs for "Antenna", "Readability", "Strength", and "Tone"
        signalLayout = QHBoxLayout()
        self.watt = QSpinBox()
        self.watt.setRange(0, 1000)  # Set range for watt (0 to 1000)
        self.watt.setValue(10)  # Set default value for watt to 10

        self.readabilityInput = QSpinBox()
        self.readabilityInput.setRange(1, 5)  # Set range for readability (1 to 5)
        self.readabilityInput.setValue(5)  # Set default value for readability to max (5)

        self.strengthInput = QSpinBox()
        self.strengthInput.setRange(1, 9)  # Set range for strength (1 to 9)
        self.strengthInput.setValue(9)  # Set default value for strength to max (9)

        self.toneInput = QSpinBox()
        self.toneInput.setRange(1, 9)  # Set range for tone (1 to 9)
        self.toneInput.setValue(9)  # Set default value for tone to max (9)

        signalLayout.addWidget(QLabel("Watt:"))
        signalLayout.addWidget(self.watt)
        signalLayout.addWidget(QLabel("Readability:"))
        signalLayout.addWidget(self.readabilityInput)
        signalLayout.addWidget(QLabel("Strength:"))
        signalLayout.addWidget(self.strengthInput)
        signalLayout.addWidget(QLabel("Tone:"))
        signalLayout.addWidget(self.toneInput)
        layout.addLayout(signalLayout)
        
        self.encodeButton = QPushButton("Generate Morse Audio")
        self.encodeButton.clicked.connect(self.generate_morse_audio)
        layout.addWidget(self.encodeButton)
        
        self.playButton = QPushButton("Play Morse Audio")
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.play_audio)
        layout.addWidget(self.playButton)
        
        self.downloadButton = QPushButton("Download Morse Audio")
        self.downloadButton.setEnabled(False)
        self.downloadButton.clicked.connect(self.download_audio)
        layout.addWidget(self.downloadButton)
        
        self.audioPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.audioPlayer.setAudioOutput(self.audioOutput)
        
        self.setLayout(layout)
        self.setWindowTitle("BeepBoopChat")
    
    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3)")
        if file_path:
            print('Decode the wav file into text...')
            decoded_text = decode_morse_from_audio(file_path)
            self.decodedText.setPlainText(decoded_text)
    
    def generate_morse_audio(self):
        text = self.replyText.toPlainText()
        if text:
            self.output_path = "log/OUTPUT.wav"
            
            # get the necessary values
            print('Read the form elements...')
            your_name = self.yourNameInput.text()
            partner_name = self.partnerNameInput.text()
            location = self.locationInput.text()
            antenna = self.antennaDropdown.currentText()
            watt = self.watt.value()
            readability = self.readabilityInput.value()
            strength = self.strengthInput.value()
            tone = self.toneInput.value()
            
            print('Encode the text into morse...')
            encode_text_to_morse_audio(text,partner_name,your_name,watt,antenna,location,readability,strength,tone,self.output_path)
            self.playButton.setEnabled(True)
            self.downloadButton.setEnabled(True)
    
    def play_audio(self):
        self.audioPlayer.setSource(QUrl.fromLocalFile(self.output_path))
        self.audioPlayer.play()
    
    def download_audio(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Morse Audio", "", "WAV Files (*.wav)")
        if save_path:
            os.rename(self.output_path, save_path)
            self.playButton.setEnabled(True)
            self.downloadButton.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MorseCodeApp()
    window.show()
    sys.exit(app.exec())
