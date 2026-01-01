import streamlit as st
import numpy as np
import sounddevice as sd
from scipy.fft import fft
from scipy.signal import find_peaks
import time

# Standard tuning for 6-string acoustic guitar (from lowest to highest)
STANDARD_TUNING = {
    'E2': 82.41,   # Low E (6th string)
    'A2': 110.00,  # A (5th string)
    'D3': 146.83,  # D (4th string)
    'G3': 196.00,  # G (3rd string)
    'B3': 246.94,  # B (2nd string)
    'E4': 329.63   # High E (1st string)
}

STRING_NAMES = ['E2 (6th)', 'A2 (5th)', 'D3 (4th)', 'G3 (3rd)', 'B3 (2nd)', 'E4 (1st)']
STRING_FREQS = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63]

# Audio settings
SAMPLE_RATE = 44100
DURATION = 0.5  # Duration of audio capture in seconds
BUFFER_SIZE = int(SAMPLE_RATE * DURATION)

def find_frequency(audio_data, sample_rate):
    """
    Find the dominant frequency in the audio data using FFT
    """
    # Apply window function to reduce spectral leakage
    windowed = audio_data * np.hanning(len(audio_data))
    
    # Perform FFT
    fft_data = fft(windowed)
    fft_freq = np.fft.fftfreq(len(fft_data), 1/sample_rate)
    
    # Only look at positive frequencies
    positive_freqs = fft_freq[:len(fft_freq)//2]
    magnitude = np.abs(fft_data[:len(fft_data)//2])
    
    # Focus on guitar frequency range (80 Hz - 1000 Hz)
    valid_range = (positive_freqs > 70) & (positive_freqs < 1000)
    
    if not np.any(valid_range):
        return 0
    
    valid_freqs = positive_freqs[valid_range]
    valid_magnitude = magnitude[valid_range]
    
    # Find peaks in magnitude
    peaks, _ = find_peaks(valid_magnitude, height=np.max(valid_magnitude) * 0.1)
    
    if len(peaks) == 0:
        return 0
    
    # Get the frequency of the highest peak
    peak_index = peaks[np.argmax(valid_magnitude[peaks])]
    detected_freq = valid_freqs[peak_index]
    
    return detected_freq

def find_closest_string(frequency):
    """
    Find which guitar string the detected frequency is closest to
    """
    if frequency < 70 or frequency > 400:
        return None, None, None
    
    min_diff = float('inf')
    closest_string = None
    closest_freq = None
    closest_index = None
    
    for idx, (name, target_freq) in enumerate(zip(STRING_NAMES, STRING_FREQS)):
        diff = abs(frequency - target_freq)
        if diff < min_diff:
            min_diff = diff
            closest_string = name
            closest_freq = target_freq
            closest_index = idx
    
    return closest_string, closest_freq, closest_index

def cents_off(detected_freq, target_freq):
    """
    Calculate how many cents off the detected frequency is from target
    """
    if detected_freq <= 0:
        return 0
    return 1200 * np.log2(detected_freq / target_freq)

def get_tuning_status(cents):
    """
    Determine tuning status based on cents off
    """
    if abs(cents) < 5:
        return "✅ IN TUNE", "green"
    elif cents > 0:
        return "⬆️ TOO HIGH (tune down)", "orange"
    else:
        return "⬇️ TOO LOW (tune up)", "red"

def record_audio():
    """
    Record audio from microphone
    """
    try:
        audio_data = sd.rec(BUFFER_SIZE, samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        return audio_data.flatten()
    except Exception as e:
        st.error(f"Error recording audio: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="Guitar Tuner", page_icon="🎸", layout="wide")

st.title("🎸 Acoustic Guitar Tuner")
st.markdown("### Standard Tuning: E-A-D-G-B-E")

# Create columns for layout
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 📋 Instructions")
    st.write("1. Allow microphone access")
    st.write("2. Select the string you want to tune")
    st.write("3. Click 'Start Listening'")
    st.write("4. Play the string")
    st.write("5. Adjust until 'IN TUNE' shows")
    
    st.markdown("---")
    st.markdown("#### 🎯 Target Frequencies")
    for name, freq in zip(STRING_NAMES, STRING_FREQS):
        st.write(f"**{name}**: {freq:.2f} Hz")

with col2:
    # String selector
    selected_string_idx = st.selectbox(
        "Select String to Tune:",
        range(len(STRING_NAMES)),
        format_func=lambda x: STRING_NAMES[x]
    )
    
    target_string = STRING_NAMES[selected_string_idx]
    target_freq = STRING_FREQS[selected_string_idx]
    
    st.markdown(f"### Tuning: **{target_string}** ({target_freq:.2f} Hz)")
    
    # Create placeholders for dynamic updates
    status_placeholder = st.empty()
    freq_placeholder = st.empty()
    cents_placeholder = st.empty()
    progress_placeholder = st.empty()
    
    # Control buttons
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        start_button = st.button("🎤 Start Listening", type="primary", use_container_width=True)
    
    with col_btn2:
        stop_button = st.button("⏹️ Stop", use_container_width=True)
    
    # Initialize session state
    if 'listening' not in st.session_state:
        st.session_state.listening = False
    
    if start_button:
        st.session_state.listening = True
    
    if stop_button:
        st.session_state.listening = False
    
    # Main listening loop
    if st.session_state.listening:
        with st.spinner("🎵 Listening..."):
            while st.session_state.listening:
                # Record audio
                audio_data = record_audio()
                
                if audio_data is not None:
                    # Detect frequency
                    detected_freq = find_frequency(audio_data, SAMPLE_RATE)
                    
                    if detected_freq > 0:
                        # Calculate cents off from target
                        cents = cents_off(detected_freq, target_freq)
                        status_text, status_color = get_tuning_status(cents)
                        
                        # Update display
                        freq_placeholder.metric(
                            "Detected Frequency", 
                            f"{detected_freq:.2f} Hz",
                            f"{detected_freq - target_freq:.2f} Hz"
                        )
                        
                        cents_placeholder.metric(
                            "Cents Off", 
                            f"{cents:.1f} cents",
                            help="100 cents = 1 semitone"
                        )
                        
                        status_placeholder.markdown(
                            f"### :{status_color}[{status_text}]"
                        )
                        
                        # Visual tuning indicator
                        progress_value = max(0, min(100, 50 + cents))
                        progress_placeholder.progress(progress_value / 100)
                        
                    else:
                        freq_placeholder.info("🔇 No clear signal detected. Play the string louder.")
                
                time.sleep(0.1)
                
                # Check if stop button was pressed
                if stop_button:
                    st.session_state.listening = False
                    break

# Footer
st.markdown("---")
st.markdown("💡 **Tips:** Pluck the string firmly and let it ring. Tune in a quiet environment for best results.")
