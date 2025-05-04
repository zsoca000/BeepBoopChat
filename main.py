import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QLineEdit, QComboBox, QSpinBox, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from src.utils import wav2morse, morse2qso, qso2text, text2qso, qso2morse, morse2wav


def decode_morse_from_audio(file_path):
    if file_path.endswith('.wav'):
        morse_code = wav2morse(file_path)
        qso_code = morse2qso(morse_code)
        text = qso2text(qso_code)
        return text
    else:
        return 'Error: Unsupported file format. Please upload a .wav file.'

def encode_text_to_morse_audio(text,partner_name,your_name,watt,antenna,location,readability,strength,tone,output_path):
    qso_text = text2qso(text,partner_name,your_name,watt,antenna,location,readability,strength,tone)
    morse_code = qso2morse(qso_text)
    morse2wav(morse_code,output_path=output_path)
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
        self.partnerNameInput = QLineEdit()
        nameLayout.addWidget(QLabel("Your name:"))
        nameLayout.addWidget(self.yourNameInput)
        nameLayout.addWidget(QLabel("Partner name:"))
        nameLayout.addWidget(self.partnerNameInput)
        layout.addLayout(nameLayout)

        # Add "Location" text box and "Antenna" dropdown
        locationAntennaLayout = QHBoxLayout()
        self.locationInput = QLineEdit()
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
        self.readabilityInput = QSpinBox()
        self.strengthInput = QSpinBox()
        self.toneInput = QSpinBox()
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
            decoded_text = decode_morse_from_audio(file_path)
            self.decodedText.setPlainText(decoded_text)
    
    def generate_morse_audio(self):
        text = self.replyText.toPlainText()
        if text:
            self.output_path = "OUTPUT.wav"
            
            # get the necessary values
            your_name = self.yourNameInput.text()
            partner_name = self.partnerNameInput.text()
            location = self.locationInput.text()
            antenna = self.antennaDropdown.currentText()
            watt = self.watt.value()
            readability = self.readabilityInput.value()
            strength = self.strengthInput.value()
            tone = self.toneInput.value()

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
