from faster_whisper import WhisperModel

def transcribe_audio(filename="mic_input.wav", model_size="base"):
    model = WhisperModel(model_size, device="cuda")  # or "float16" / "int8_float16"
    segments, _ = model.transcribe(filename)

    print("Transcription:")
    with open("transcription2.txt", "w", encoding="utf-8") as f:
        for segment in segments:
            f.write(f"[{segment.start:.2f} -> {segment.end:.2f}] {segment.text}\n")
transcribe_audio("mic_input.wav", model_size="medium")
