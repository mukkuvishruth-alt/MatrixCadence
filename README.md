# MatrixCadence 🎼🧮

MatrixCadence is a platform-independent Python project bridging linear algebra and music theory. It models chord progressions as vectors inside pitch-class matrices, extracts symbolic kernels (null spaces) using SymPy, maps the result to modulo-12 pitch variations, and outputs playable auditory streams.

## 📁 File Structure
```text
MatrixCadence/
├── requirements.txt
├── README.md
└── src/
    └── MatrixCadence/
        └── main.py
```

## 🛠️ Setup & Execution

### 1. Install Dependencies
Open your terminal (macOS) or Command Prompt (Windows) and install the requirement packages:
```bash
pip install -r requirements.txt
```

### 2. Navigate to Script Folder
```bash
cd src/MatrixCadence
```

### 3. Execution
```bash
python main.py
```

## 🧠 Core Methodology
1. **Pitch Class Transformation:** Chords are encoded as linear column arrays.
2. **Null Space Parsing:** Resolves $Ax = 0$ using symbolic mathematics to find structural musical inverses.
3. **Synthesis Engine:** Maps integers natively into a physical MIDI output array (`.mid`) and plays it using a hardware audio connection device stream natively.