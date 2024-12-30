# Fourier Transform, Beamforming Toolkit, and Fingerprinting Application

## Introduction
This project consists of three major components: a Fourier Transform (FT) Magnitude/Phase Mixer, a Beamforming Simulator, and a Signal Fingerprinting Application. Together, these tools provide a comprehensive understanding of signal decomposition, beamforming, and signal identification techniques for real-time applications in fields such as communications, medical imaging, and music recognition.

---

## Features

### Part A: FT Magnitude/Phase Mixer or Emphasizer

#### **1. Image Viewers**
- **Grayscale Images**:
  - Open and view up to four grayscale images, each in its own viewport.
  - Automatically convert colored images to grayscale.
- **Unified Image Size**:
  - Automatically resize all images to match the smallest dimensions among them.
- **FT Components**:
  - For each image, display the following components via a dropdown menu:
    1. FT Magnitude
    2. FT Phase
    3. FT Real
    4. FT Imaginary
- **Easy Browsing**:
  - Replace any image by double-clicking its viewport to browse and load a new image.

*(Insert image/video showcasing image viewers and component selection)*

#### **2. Two Output Ports**
- Display the mixer results in one of two dedicated output viewports.
- Each viewport operates independently and mirrors the functionality of input viewports.

#### **3. Brightness/Contrast Adjustments**
- Modify brightness and contrast of any image or FT component via mouse drag:
  - Up/Down: Adjust brightness
  - Left/Right: Adjust contrast

*(Insert image demonstrating brightness/contrast adjustment)*

#### **4. Components Mixer**
- Combine FT components from the four input images using weighted averages.
- Customize weights for:
  - Magnitude and phase
  - Real and imaginary components
- Intuitive slider-based UI for setting component weights.

*(Insert image of component mixing interface with sliders)*

#### **5. Regions Mixer**
- Define a rectangular region on each FT component:
  - Inner region (low frequencies)
  - Outer region (high frequencies)
- Options to include either region in the output.
- Highlight the selected region with semi-transparent coloring or hashing.
- Unified region size across all four images, adjustable via sliders or resize handles.

*(Insert image showing region selection and highlighting)*

#### **6. Real-Time Mixing**
- Perform Inverse FFT (iFFT) to generate output images in real time.
- Features include:
  - Progress bar to indicate the status of the operation.
  - Thread management to cancel ongoing operations and prioritize new requests.

*(Insert video of real-time mixing with progress bar)*

---

### Part B: Beamforming Simulator

#### **1. Real-Time Beam Steering**
- Customize parameters to steer the beam direction dynamically:
  - Number of transmitters/receivers
  - Applied delays/phase shifts
  - Number of operating frequencies (with real-time updates)

#### **2. Array Geometry**
- Support for linear and curved array geometries:
  - Adjustable curvature parameters for curved arrays.

#### **3. Visualization**
- Display constructive/destructive interference maps and beam profiles in synchronized viewers.

*(Insert image/video of beamforming maps and profiles)*

#### **4. Multi-Array Support**
- Add multiple phased array units to the system.
- Customize location and parameters of each unit.

#### **5. Scenario Management**
- Include at least three predefined scenarios inspired by:
  - 5G communications
  - Ultrasound imaging
  - Tumor ablation
- Load, visualize, and fine-tune scenarios via parameter settings files.

*(Insert video showcasing scenarios and parameter customization)*

---

### Part C: Signal Fingerprinting Application

#### **1. Song Repository Creation**
- Each group contributes one song split into:
  - Full song, music, and vocals.
- Files are uploaded to a shared repository in the format:
  - `GroupX_SongName_Full`
  - `GroupX_SongName_Music`
  - `GroupX_SongName_Vocals`
- A shared sheet ensures no song duplication.

#### **2. Spectrogram Generation**
- Generate spectrograms for the first 30 seconds of each file (full, music, vocals).
- Output files saved locally.

#### **3. Feature Extraction and Fingerprinting**
- Extract key spectrogram features and save them alongside the spectrogram.
- Hash features using perceptual hashing for compact fingerprints.

#### **4. Similarity Matching**
- Given any sound file (full, music, or vocals):
  - Generate its spectrogram and features.
  - Match it against the repository and display results in a sorted table with similarity indices.

*(Insert image of similarity table output)*

#### **5. File Mixing and Matching**
- Combine two files using weighted averages:
  - Use a slider to adjust weights.
  - Treat the resulting file as new and perform similarity matching.

*(Insert image/video of file mixing and matching)*

---

## Project Structure

### Directories
- **src/**: Source code for FT mixer, beamforming simulator, and fingerprinting application.
- **data/**: Sample images, songs, and parameter files.
- **docs/**: Documentation and user guides.

### Files
- **README.md**: Project overview and setup instructions.
- **requirements.txt**: List of dependencies.
- **ft_mixer.py**: Implementation of the FT Magnitude/Phase Mixer.
- **beamforming_simulator.py**: Implementation of the Beamforming Simulator.
- **fingerprinting.py**: Implementation of the Signal Fingerprinting Application.
- **ui_design.ui**: Qt Designer file for the graphical user interface.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/signal-processing-toolkit.git
   cd signal-processing-toolkit
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

## Usage

1. **FT Mixer**:
   - Open and manipulate grayscale images.
   - Explore FT components and perform real-time mixing.

2. **Beamforming Simulator**:
   - Adjust array geometry and parameters to visualize beam patterns.
   - Load predefined scenarios or create custom setups.

3. **Fingerprinting Application**:
   - Generate fingerprints for sound files and match them to a shared repository.
   - Combine files and search for matches based on the weighted mix.

---

## License
This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments
- Tutorials and inspiration from [relevant links].
- Contributions by [Team Name/Group].

