# Signal Fingerprinting Application 


---

## 🔍 Overview
The **Signal Fingerprinting Application** identifies sound files based on intrinsic features extracted from their spectrograms. This tool is useful in various fields, such as the music industry (identifying songs or singers) and medical diagnostics (recognizing arrhythmias in ECG signals).

---

## 🎧 Features

### **1. 🏃‍♂️ Song Repository Creation**
- Each group contributes one song and splits it into:
  - **Full song**
  - **Music**
  - **Vocals**
- Files are uploaded to a shared repository with the following naming format:
  - `GroupX_SongName_Full`
  - `GroupX_SongName_Music`
  - `GroupX_SongName_Vocals`
- A shared sheet tracks song names to prevent duplication.

### **2. 🔬 Spectrogram Generation**
- Generate spectrograms for the **first 30 seconds** of each file (full, music, vocals).
- Save spectrograms locally for further processing.

### **3. ✨ Feature Extraction and Fingerprinting**
- Extract key features from spectrograms.
- Use **perceptual hashing** to create compact fingerprints for fast comparisons.
- Save features and fingerprints in a structured file.

### **4. 🔎 Similarity Matching**
- Input any sound file (**full, music, or vocals**) to:
  - Generate its spectrogram and extract features.
  - Compare it against the repository.
  - Display similarity scores in a **sorted table** within the GUI.

### **5. ⚖️ File Mixing and Matching**
- Combine two files using **weighted averages**:
  - Adjust weights via an interactive slider.
  - Treat the resulting file as a new input for similarity matching.

---

## 🔠 Project Structure

### **🛀 Directories**
- **`src/`**: Source code for the fingerprinting application.
- **`data/`**: Sample songs and generated spectrograms.
- **`docs/`**: Documentation and user guides.

### **🗂 Files**
- **`README.md`**: Project overview and setup instructions.
- **`requirements.txt`**: List of dependencies.
- **`fingerprinting.py`**: Implementation of the Signal Fingerprinting Application.
- **`ui_design.ui`**: Qt Designer file for the graphical user interface.

---

## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/signal-fingerprinting-app.git
   cd signal-fingerprinting-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python fingerprinting.py
   ```

---

## 🔁 Usage

### **1. 🎵 Song Repository Creation**
- Upload songs split into **full, music, and vocals**.
- Ensure unique song entries in the shared repository.

### **2. 🔬 Spectrogram Generation**
- Automatically generate and save spectrograms for uploaded files.

### **3. ✨ Feature Extraction**
- Extract features and fingerprints for all spectrograms.

### **4. 🔎 Similarity Matching**
- Input a sound file to find the closest matches in the repository.

### **5. ⚖️ File Mixing**
- Combine two files and match the resulting fingerprint to the repository.

---

## 🗄 License
This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## 🙏 Acknowledgments
- Tutorials and inspiration from [relevant links].
- Contributions by **[Team Name/Group]**.

---

![App Screenshot](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Example-QT-GUI.png/600px-Example-QT-GUI.png "App Screenshot")

