import sounddevice as sd
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QTextEdit, QProgressBar, QSlider, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from scipy.spatial.distance import euclidean
import os
import json
import hashlib
import librosa
import logging
from typing import Dict, Tuple, List, Optional
import numpy as np
import soundfile as sf
logging.basicConfig(level=logging.DEBUG)
class SongFingerprint:
    def __init__(self, database_file: str = "fingerprint_database.json",
                 sample_rate: int = 44100,
                 duration: float = 28):
        self.database_file = database_file
        self.sample_rate = sample_rate
        self.duration = duration
        self.database = self.load_database()

    def load_database(self) -> Dict:
        try:
            if os.path.exists(self.database_file):
                with open(self.database_file, "r") as f:
                    logging.debug(f"Loading database from {self.database_file}")
                    return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error loading database: {e}")
        return {}

    def save_database(self) -> None:
        try:
            with open(self.database_file, 'w') as db_file:
                logging.debug(f"Saving database to {self.database_file}")
                json.dump(self.database, db_file, indent=4)
        except IOError as e:
            logging.error(f"Error saving database: {e}")



    def extract_features(self, y: np.ndarray, sample_rate: int):

        spectrogram = librosa.stft(y, n_fft=2048, hop_length=512, win_length=1024)
        spectrogram_abs = np.abs(spectrogram)

        chroma = librosa.feature.chroma_stft(S=spectrogram_abs, sr=sample_rate)
        chroma_mean = np.mean(chroma, axis=1)

        spectral_contrast = librosa.feature.spectral_contrast(S=spectrogram_abs, sr=sample_rate)
        spectral_contrast_mean = np.mean(spectral_contrast, axis=1)

        mfccs = librosa.feature.mfcc(S=librosa.amplitude_to_db(spectrogram_abs), sr=sample_rate, n_mfcc=13)
        mfcc_mean = np.mean(mfccs, axis=1)

        pitches, magnitudes = librosa.core.piptrack(y=y, sr=sample_rate)
        pitch_mean = np.mean(pitches, axis=1)

        combined_features = np.concatenate([chroma_mean, spectral_contrast_mean, mfcc_mean, pitch_mean])

        return combined_features

    def calculate_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        try:
            distance = euclidean(features1, features2)

            max_distance = 2000
            min_distance = 0

            normalized_distance = (distance - min_distance) / (max_distance - min_distance)
            normalized_distance = np.clip(normalized_distance, 0, 1)  # Ensure it's between 0 and 1

            similarity = (1 - normalized_distance) * 100
            print(type(similarity))
            logging.debug(
                f"Distance: {distance}, Normalized Distance: {normalized_distance}, Similarity: {similarity}%")
            return similarity

        except Exception as e:
            logging.error(f"Error calculating similarity: {e}")
            return 0.0

    def generate_fingerprint(self, file_path: str) -> Tuple[Optional[np.ndarray], Optional[str]]:
        try:
            logging.debug(f"Generating fingerprint for {file_path}.")
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Audio file not found: {file_path}")

            try:
                y, sr = librosa.load(file_path, sr=self.sample_rate, duration=self.duration)
                if not isinstance(y, np.ndarray):
                    raise ValueError("Loaded audio is not of type numpy.ndarray")
            except Exception as e:
                logging.error(f"Error loading audio file: {e}")
                return None, None

            logging.debug(f"Loaded {file_path} with {len(y)} samples.")

            target_length = int(self.duration * self.sample_rate)
            if len(y) < target_length:
                y = np.pad(y, (0, target_length - len(y)))
            else:
                y = y[:target_length]

            if not isinstance(y, np.ndarray):
                raise ValueError(f"Expected numpy ndarray, but got {type(y)}")
            print(type(y))
            features = self.extract_features(y, self.sample_rate)

            if features.size == 0 or np.isnan(features).any() or np.isinf(features).any():
                raise ValueError("No valid features extracted or features contain NaN/Inf values.")

            hash_value = self.generate_hash(features)

            return features, hash_value

        except Exception as e:
            logging.error(f"Error generating fingerprint for {file_path}: {e}")
            return None, None

    def generate_hash(self, file_path: str) -> str:
        try:
            logging.debug("Loading audio file and extracting features.")
            # Load audio file
            y, sr = librosa.load(file_path, sr=self.sample_rate, duration=self.duration)

            # Extract perceptual features (MFCCs)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            logging.debug(f"MFCC shape: {mfcc.shape}")

            # Take mean of MFCCs across time
            mfcc_mean = np.mean(mfcc, axis=1)

            # Normalize the features
            normalized = (mfcc_mean - np.min(mfcc_mean)) / (np.max(mfcc_mean) - np.min(mfcc_mean) + 1e-7)

            # Threshold to generate binary string
            mean_val = np.mean(normalized)
            binary = ['1' if x > mean_val else '0' for x in normalized]

            # Generate hash from binary string
            hash_str = ''.join(binary)
            return hashlib.md5(hash_str.encode()).hexdigest()

        except Exception as e:
            logging.error(f"Error generating perceptual hash: {e}")
            return "0" * 32

    def match_song(self, file_path: str, threshold: float = 0.0):
        try:
            logging.debug(f"Matching song {file_path}.")
            feature, query_hash = self.generate_fingerprint(file_path)
            if query_hash is None:
                raise ValueError("Failed to generate fingerprint")

            results = {}

            for label, data in self.database.items():
                try:
                    similarity = self.calculate_similarity(feature, data["features"])

                    if similarity >= threshold:
                        results[label] = similarity

                except Exception as e:
                    logging.error(f"Error processing entry {label}: {e}")
                    continue

            return dict(list(sorted(results.items(), key=lambda item: item[1], reverse=True))[:5])


        except Exception as e:
            logging.error(f"Error matching song: {e}")
            return []

    def add_to_database(self, file_path: str, label: str) -> bool:
        try:
            logging.debug(f"Adding song {file_path} to database with label {label}.")
            features, hash_value = self.generate_fingerprint(file_path)
            if features is None or hash_value is None:
                raise ValueError("Failed to generate fingerprint")

            self.database[label] = {
                "features": features.tolist(),
                "hash": hash_value
            }
            self.save_database()
            return True

        except Exception as e:
            logging.error(f"Error adding song to database: {e}")
            return False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fingerprint_engine = SongFingerprint()
        self.audio1_path = None
        self.audio2_path = None
        self.audio1_data = None
        self.audio2_data = None
        self.blended_song =[]
        self.isPlaying = False
        self.sr = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Audio Recognition and Mixing App")
        self.setGeometry(550, 30, 800, 1000)

        main_layout = QVBoxLayout()
        # section 1
        recognition_group = QGroupBox("Song Recognition")
        recognition_layout = QVBoxLayout()

        self.upload_button = QPushButton()
        self.upload_button.setFixedSize(120, 120)

        # Set the normal icon
        normal_icon = QIcon("shazam.png")
        hover_icon = QIcon("shazam_lighter.png")

        self.upload_button.setIcon(normal_icon)
        self.upload_button.setIconSize(self.upload_button.size())

        # Styling the button
        self.upload_button.setStyleSheet("""
        QPushButton {
            background-color: #007AFF;
            border-radius: 60px;
            border: 3px solid #0056B3;
        }
        QPushButton:hover {
            background-color: #3399FF;  # Lighter blue when hovering
        }
        """)

        # Change icon on hover
        def on_hover_enter(event):
            self.upload_button.setIcon(hover_icon)

        def on_hover_leave(event):
            self.upload_button.setIcon(normal_icon)

        # Connect hover events to the button
        self.upload_button.enterEvent = on_hover_enter
        self.upload_button.leaveEvent = on_hover_leave

        self.upload_button.clicked.connect(lambda: self.match_song(0))

        self.train_button = QPushButton("Train Database")
        self.train_button.clicked.connect(self.train_database)

        self.clear_database_button = QPushButton("Clear Database")
        self.clear_database_button.clicked.connect(self.clear_database)

        recognition_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)
        recognition_layout.addWidget(self.train_button)
        recognition_layout.addWidget(self.clear_database_button)
        recognition_group.setLayout(recognition_layout)

        # section 2
        mixing_group = QGroupBox("Audio Mixing")
        mixing_layout = QVBoxLayout()

        self.load_audio1_button = QPushButton("Load Audio File 1")
        self.load_audio1_button.clicked.connect(self.load_audio1)

        self.load_audio2_button = QPushButton("Load Audio File 2")
        self.load_audio2_button.clicked.connect(self.load_audio2)

        self.mix_button = QPushButton("Mix and Save Audio")
        self.mix_button.clicked.connect(self.mix_audio)

        self.match_blended_song_button = QPushButton("Match Blended Song")
        self.match_blended_song_button.clicked.connect(lambda: self.match_song(1, self.blended_song))

        self.play_and_pause_button = QPushButton("Play Blended Song")
        self.play_and_pause_button.clicked.connect(self.play_and_pause)

        self.slider_label = QLabel("Mix Weight: 50% Audio 1, 50% Audio 2")
        self.mix_slider = QSlider(Qt.Horizontal)
        self.mix_slider.setMinimum(0)
        self.mix_slider.setMaximum(100)
        self.mix_slider.setValue(50)
        self.mix_slider.valueChanged.connect(self.update_slider_label)

        mixing_layout.addWidget(self.load_audio1_button)
        mixing_layout.addWidget(self.load_audio2_button)
        mixing_layout.addWidget(self.mix_button)
        mixing_layout.addWidget(self.match_blended_song_button)
        mixing_layout.addWidget(self.play_and_pause_button)
        mixing_layout.addWidget(self.slider_label)
        mixing_layout.addWidget(self.mix_slider)
        mixing_group.setLayout(mixing_layout)

        # section 3
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()

        self.result_label = QLabel("Results:")
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        results_layout.addWidget(self.result_label)
        results_layout.addWidget(self.result_display)
        results_layout.addWidget(QLabel("Training Progress:"))
        results_layout.addWidget(self.progress_bar)
        results_group.setLayout(results_layout)

        # making the groups into the layout
        main_layout.addWidget(recognition_group)
        main_layout.addWidget(mixing_group)
        main_layout.addWidget(results_group)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QGroupBox {
                color: black;
                border: 2px solid #0088FF;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #0088FF;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #3399FF;
            }
            QLabel {
                color: black;
            }
            QTextEdit {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #555;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #0088FF;
                border: 1px solid #0088FF;
                width: 14px;
                height: 14px;
                margin: -3px 0;
                border-radius: 7px;
            }
            QSlider::handle:horizontal:hover {
                background: #3399FF;
            }
            QProgressBar {
                background-color: #333;
                color: white;
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #0088FF;
                width: 20px;
            }
        """)

    def train_database(self):
        folder = QFileDialog.getExistingDirectory(self, "Select a Folder with Audio Files")
        if not folder:
            return

        # Supported audio extensions
        supported_extensions = (".mp3", ".wav")
        audio_files = [
            os.path.join(folder, file) for file in os.listdir(folder)
            if file.lower().endswith(supported_extensions)
        ]

        if not audio_files:
            self.result_display.append("No supported audio files found in the selected folder.\n")
            return

        self.progress_bar.setValue(0)
        step = 100 / len(audio_files)

        for i, file in enumerate(audio_files):
            label = os.path.basename(file)
            try:
                self.fingerprint_engine.add_to_database(file, label)
            except Exception as e:
                self.result_display.append(f"Error processing {label}: {e}\n")
            self.progress_bar.setValue(int((i + 1) * step))

        self.result_display.append(f"Added {len(audio_files)} songs to the database from folder '{folder}'.\n")

    def match_song(self, index, blended_song=None):

        if index == 0:  # Uploaded song
            self.result_display.clear()
            file, _ = QFileDialog.getOpenFileName(self, "Select an Audio File", "", "Audio Files (*.mp3 *.wav)")
            if not file:
                return
        elif index == 1:  # Blended song
            if blended_song is None or len(blended_song) == 0:
                self.result_display.append("No blended song to match.\n")
                return
            file = blended_song

        self.result_display.append(f"Matching song: {file}...\n")
        if index == 1:
            # Use the blended song data directly
            results = self.fingerprint_engine.match_song(file)
        else:
            # Use the file path for uploaded songs
            results = self.fingerprint_engine.match_song(file)

        if results:
            display_text = "\n".join([f"{song}: {similarity:.2f}%" for song, similarity in results.items()])
            self.result_display.append("Match Results:\n" + display_text + "\n")
        else:
            self.result_display.append("No match found.\n")

    def clear_database(self):
        self.fingerprint_engine.database = {}
        self.fingerprint_engine.save_database()
        self.result_display.clear()
        self.result_display.append("Database cleared.\n")


    def load_audio1(self):
        self.result_display.clear()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File 1", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.audio1_path = file_path
            self.audio1_data, self.sr = librosa.load(file_path, sr=None)
            self.result_display.append(f"Loaded Audio 1: {os.path.basename(file_path)}")

    def load_audio2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File 2", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.audio2_path = file_path
            self.audio2_data, _ = librosa.load(file_path, sr=self.sr)  # Match sample rate with audio 1
            self.result_display.append(f"Loaded Audio 2: {os.path.basename(file_path)}")

    def update_slider_label(self):
        value = self.mix_slider.value()
        self.slider_label.setText(f"Mix Weight: {value}% Audio 1, {100 - value}% Audio 2")

    def mix_audio(self):
        if self.audio1_data is None:
            self.result_display.append("Audio 1 is not loaded.")
            return

        if self.audio2_data is None:
            self.result_display.append("Audio 2 is not loaded.")
            return

        weight_audio1 = self.mix_slider.value() / 100
        weight_audio2 = 1 - weight_audio1

        if len(self.audio1_data) > len(self.audio2_data):
            self.audio2_data = np.pad(self.audio2_data, (0, len(self.audio1_data) - len(self.audio2_data)),
                                      mode='constant')
        else:
            self.audio1_data = np.pad(self.audio1_data, (0, len(self.audio2_data) - len(self.audio1_data)),
                                      mode='constant')

        mixed_audio = (weight_audio1 * self.audio1_data + weight_audio2 * self.audio2_data).astype(np.float32)

        # Define a fixed directory and file name
        fixed_directory = "mixed_audio"  # Ensure this folder exists or create it dynamically
        os.makedirs(fixed_directory, exist_ok=True)  # Create the directory if it doesn't exist
        save_path = os.path.join(fixed_directory, "mixed_audio.wav")

        # Save the mixed audio to the fixed path
        sf.write(save_path, mixed_audio, self.sr)
        self.result_display.append(f"Mixed audio saved to {save_path}")
        self.blended_song = save_path
    def play_and_pause(self):
        if self.blended_song:

            if self.isPlaying :
                sd.stop()
                self.play_and_pause_button.setText("Play Blended Song")
                self.isPlaying=False

            else:
                audio_path = self.blended_song
                y, sr = librosa.load(audio_path, sr=None)
                sd.play(y, sr)
                self.play_and_pause_button.setText("Pause Blended Song")
                self.isPlaying=True
        else:
             self.result_display.append("No bleded song.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
