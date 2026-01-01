# 🎸 Guitar Tuner App

A real-time guitar tuning application for 6-string acoustic guitar built with Python and Streamlit.

## Features

✨ **Real-time pitch detection** using FFT (Fast Fourier Transform)
🎯 **Standard tuning support** (E-A-D-G-B-E)
📊 **Visual feedback** with cents deviation
🎨 **User-friendly interface** with color-coded tuning status
🎵 **Accurate frequency detection** (70-1000 Hz range)

## Standard Tuning Reference

| String | Note | Frequency |
|--------|------|-----------|
| 6th (Lowest) | E2 | 82.41 Hz |
| 5th | A2 | 110.00 Hz |
| 4th | D3 | 146.83 Hz |
| 3rd | G3 | 196.00 Hz |
| 2nd | B3 | 246.94 Hz |
| 1st (Highest) | E4 | 329.63 Hz |

## Installation on Windows

### Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Working microphone** - Built-in or external

### Step-by-Step Setup

1. **Download the files**
   - Save `guitar_tuner.py` and `requirements.txt` to a folder (e.g., `C:\GuitarTuner`)

2. **Open Command Prompt**
   - Press `Win + R`
   - Type `cmd` and press Enter

3. **Navigate to your folder**
   ```cmd
   cd C:\GuitarTuner
   ```

4. **Create a virtual environment (recommended)**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

5. **Install required packages**
   ```cmd
   pip install -r requirements.txt
   ```

   If you encounter issues, install packages individually:
   ```cmd
   pip install streamlit numpy scipy sounddevice
   ```

## Running the App

1. **Make sure your virtual environment is activated**
   ```cmd
   venv\Scripts\activate
   ```

2. **Run the app**
   ```cmd
   streamlit run guitar_tuner.py
   ```

3. **The app will open in your default web browser** (usually at `http://localhost:8501`)

4. **Allow microphone access** when prompted by your browser

## How to Use

1. **Select the string** you want to tune from the dropdown menu
2. Click **"Start Listening"**
3. **Pluck the string** firmly and let it ring
4. Watch the tuning indicator:
   - 🟢 **Green "IN TUNE"** - Perfect! (within ±5 cents)
   - 🟠 **Orange "TOO HIGH"** - Turn tuning peg counter-clockwise to lower pitch
   - 🔴 **Red "TOO LOW"** - Turn tuning peg clockwise to raise pitch
5. Adjust the tuning peg slowly until you see "IN TUNE"
6. Click **"Stop"** when finished

## Understanding Cents

- **Cents** are a logarithmic unit of pitch measurement
- **100 cents = 1 semitone** (one fret on guitar)
- **±5 cents** is considered "in tune" for most purposes
- **±10 cents** is noticeable to most listeners

## Troubleshooting

### No audio detected
- Check microphone permissions in Windows settings
- Ensure microphone is not muted
- Try selecting a different microphone in Windows sound settings
- Position microphone closer to the guitar

### Inaccurate readings
- Tune in a quiet environment
- Pluck strings one at a time
- Let the string ring clearly
- Don't press frets while tuning open strings
- Check that your guitar is the only sound source

### App won't start
- Verify Python is installed: `python --version`
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`
- Make sure virtual environment is activated

### "Module not found" errors
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall missing package: `pip install [package-name]`

## Tips for Best Results

🎯 **Pluck firmly** - Give the string a good pluck to generate a clear signal
🔇 **Quiet environment** - Background noise can interfere with detection
🎸 **One string at a time** - Mute other strings while tuning
⏱️ **Be patient** - Let the string ring for 1-2 seconds
🔄 **Small adjustments** - Turn tuning pegs slowly for fine-tuning
🎵 **Tune up, not down** - Approach the target pitch from below for better stability

## Technical Details

- **Sample Rate**: 44,100 Hz
- **FFT Window**: Hanning window to reduce spectral leakage
- **Frequency Range**: 70-1000 Hz (optimized for guitar)
- **Buffer Duration**: 0.5 seconds
- **Accuracy**: ±1 Hz typical, ±5 cents for "in tune" threshold

## Future Enhancements (Optional)

- [ ] Alternative tunings (Drop D, DADGAD, Open G, etc.)
- [ ] Chromatic tuner mode
- [ ] Tuning history/log
- [ ] Visual waveform display
- [ ] Support for 7-string, 12-string guitars
- [ ] Bass guitar mode
- [ ] Save custom tunings

## System Requirements

- **OS**: Windows 10 or higher
- **RAM**: 4GB minimum
- **Microphone**: Any functional microphone (built-in or external)
- **Python**: 3.8 or higher
- **Browser**: Chrome, Firefox, or Edge (latest versions)

## License

Free to use and modify for personal use.

## Credits

Built with:
- **Streamlit** - Web framework
- **NumPy** - Numerical computing
- **SciPy** - Signal processing and FFT
- **sounddevice** - Audio recording

---

**Happy Tuning! 🎸🎵**
