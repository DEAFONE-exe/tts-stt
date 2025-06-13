import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

def record_audio(filename="output.wav", duration=5, sample_rate=16000):
    print(f"Recording for {duration} seconds...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    write(filename, sample_rate, audio)
    print(f"Saved recording to {filename}")


from faster_whisper import WhisperModel

def transcribe_audio(filename="output.wav", model_size="base"):
    model = WhisperModel(model_size, device="cpu")  # or "float16" / "int8_float16"
    segments, _ = model.transcribe(filename)

    print("Transcription:")
    with open("transcription2.txt", "a", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}\n")



record_audio("mic_input.wav", duration=10)
transcribe_audio("mic_input.wav", model_size="base")
