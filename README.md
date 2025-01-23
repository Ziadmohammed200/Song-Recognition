# Signal Fingerprinting Application

---

## 🔍 Overview
The **Signal Fingerprinting Application** identifies sound files based on intrinsic features extracted from their spectrograms. This tool is useful in various fields, such as the music industry (identifying songs or singers) and medical diagnostics (recognizing arrhythmias in ECG signals).

---

## 🎷 Features

### **1. 🔬 Spectrogram Generation**
- Generate spectrograms for the **first 30 seconds** of each file (full, music, vocals).  
![Spectrogram Generation](./images/spectrogram_generation.png)

### **2. ✨ Feature Extraction and Fingerprinting**
- Extract key features from spectrograms.
- Use **perceptual hashing** to create compact fingerprints for fast comparisons.
- Save features and fingerprints in a structured file.  
![Feature Extraction](./images/feature_extraction.png)

### **3. 🔎 Similarity Matching**
- Input any sound file (**full, music, or vocals**) to:
  - Generate its spectrogram and extract features.
  - Compare it against the repository.
  - Display similarity scores in a **sorted table** within the GUI.  
![Similarity Matching](https://github.com/Ziadmohammed200/Song-Recognition/blob/4a08971465a80b44715aabcb8b9472700d64fa20/images/Audio%20Recognition%20and%20Mixing%20App%20original.png)

### **4. ⚖️ File Mixing and Matching**
- Combine two files using **weighted averages**:
  - Adjust weights via an interactive slider.
  - Treat the resulting file as a new input for similarity matching.  
![File Mixing](https://github.com/Ziadmohammed200/Song-Recognition/blob/4a08971465a80b44715aabcb8b9472700d64fa20/images/Audio%20Recognition%20and%20Mixing%20App%20mix1.png)

### **5. 🏃‍♂️ Song Train**
- Each file has one song and splits it into:
  - **Full song**
  - **Music**
  - **Vocals**  
![Song Repository](https://github.com/Ziadmohammed200/Song-Recognition/blob/4a08971465a80b44715aabcb8b9472700d64fa20/images/Audio%20Recognition%20and%20Mixing%20App%20train.png)
---



## 🔧 Installation

1. **Clone the Repository**:
   ```bash
   git clone (https://github.com/Ziadmohammed200/Song-Recognition.git)
   cd signal-fingerprinting-app
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

---

## 🔁 Usage

### **1. 🎵 Song Uploading**
- Upload a song split into **full, music, and vocals**.  
![Song Uploading](./images/song_uploading.png)

### **2. 🔬 Spectrogram Generation**
- Automatically generate spectrograms for uploaded files.  
![Spectrogram](./images/spectrogram_generation_gui.png)

### **3. ✨ Feature Extraction**
- Extract features and fingerprints for the spectrogram.  
![Feature Extraction](./images/feature_extraction_gui.png)

### **4. 🔎 Similarity Matching**
- Use extracted features and fingerprints to find the closest matches in the repository.  
![Similarity Matching GUI](https://github.com/Ziadmohammed200/Song-Recognition/blob/4a08971465a80b44715aabcb8b9472700d64fa20/images/Audio%20Recognition%20and%20Mixing%20App%20vocal.png)

### **5. ⚖️ File Mixing**
- Combine two files and match the resulting fingerprint to the database.  
![File Mixing GUI](https://github.com/Ziadmohammed200/Song-Recognition/blob/4a08971465a80b44715aabcb8b9472700d64fa20/images/Audio%20Recognition%20and%20Mixing%20App%20mix2.png)

---

## 💄 License
This project is licensed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

---

## 🙏 Acknowledgments
- Tutorials and inspiration from [relevant links].


---
## Contributors
- [Ziad Mohamed](https://github.com/Ziadmohammed200) 
- [Marcilino Adel](https://github.com/marcilino-adel)
- [Ahmed Etman](https://github.com/AhmedEtma)
- [Pavly Awad](https://github.com/PavlyAwad)
- [Ahmed Rafat](https://github.com/AhmeedRaafatt)


