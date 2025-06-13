import os
import shutil
from faster_whisper import WhisperModel
import ollama
import re
from mutagen.mp3 import MP3
from pydub import AudioSegment

# --- Configuration ---
AUDIO_FILE_PATH = "../yt-video.mp3"
MODEL_SIZE = "base"
DEVICE = "cuda"  # "cuda" or "cpu"
COMPUTE_TYPE = "float16" # "float16" for GPU, "int8" for CPU
LANGUAGE = "en"
BEAM_SIZE = 5
TEMPERATURE = 0
CHUNK_DURATION_MINUTES = 10

# --- Helper Function to get Audio Duration ---
def get_audio_duration(filepath):
    """Returns the duration of an audio file in minutes."""
    try:
        audio = MP3(filepath)
        return audio.info.length / 60
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0

# --- Main Processing Logic ---
def process_audio(file_path):
    """
    Transcribes and summarizes an audio file. If the file is longer than
    CHUNK_DURATION_MINUTES, it splits it into chunks and processes each chunk.
    """
    # Load the Whisper model
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)

    audio_duration = get_audio_duration(file_path)
    print(f"Audio duration: {audio_duration:.2f} minutes")

    if audio_duration <= CHUNK_DURATION_MINUTES:
        # Process the entire file if it's short enough
        print("Audio is less than 10 minutes, processing as a single file. 🎧")
        transcribe_and_summarize(model, file_path)
    else:
        # Slice the audio into chunks if it's too long
        print("Audio is longer than 10 minutes, slicing into chunks... ✂️")
        chunk_files = slice_audio(file_path, CHUNK_DURATION_MINUTES)

        for i, chunk_file in enumerate(chunk_files):
            print(f"\n--- Processing Chunk {i+1}/{len(chunk_files)} ---")
            transcribe_and_summarize(model, chunk_file, i + 1)

        # Clean up temporary chunk files
        shutil.rmtree("temp_chunks")

def slice_audio(file_path, chunk_duration_min):
    """
    Slices an audio file into chunks of a specified duration.
    """
    if not os.path.exists("temp_chunks"):
        os.makedirs("temp_chunks")

    audio = AudioSegment.from_mp3(file_path)
    chunk_length_ms = chunk_duration_min * 60 * 1000
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_name = f"temp_chunks/chunk_{i}.mp3"
        chunk.export(chunk_name, format="mp3")
        chunk_files.append(chunk_name)

    return chunk_files

def transcribe_and_summarize(model, file_path, chunk_num=None):
    """
    Performs transcription and summarization for a given audio file.
    """
    # Transcribe the audio file
    print(f"Transcribing {file_path}...")
    segments, info = model.transcribe(
        file_path,
        language=LANGUAGE,
        beam_size=BEAM_SIZE,
        vad_filter=True,
        temperature=TEMPERATURE
    )
    print("Detected language:", info.language)

    # Save transcription
    transcription_filename = f"transcription_{chunk_num}.txt" if chunk_num else "transcription.txt"
    text = ""
    with open(transcription_filename, "w", encoding="utf-8") as f:
        for segment in segments:
            line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
            print(line, end='')
            f.write(line)
            text += segment.text + " "

    # Summarize with Ollama
    print(f"\nSummarizing {transcription_filename}...")
    response = ollama.chat(
        model='deepseek-r1:7b',
        messages=[{
            'role': 'system', 'content': (
                "Use ONLY the given content to answer the user's question. "
                "Do NOT make assumptions or fabricate information. "
                "Use bullet points or numbered lists for clarity and readability. "
                "Avoid redundant explanations. "
                "Respond in a clear, concise, and well-formatted manner. "
                "Always respond with emojis to make it engaging 🧠✨. Be casual, friendly, and concise."
            )
        }, {
            'role': 'user', 'content': f"This is a transcript from an online video guide from youtube:\n\n{text} \n\n You should ignore the timestamps. Now summarize it"
        }],
        stream=True
    )

    output = ""
    print("\n--- Summary ---")
    for chunk in response:
        content = chunk.get('message', {}).get('content', '')
        output += content
        print(content, end='', flush=True)

    final_answer = re.sub(r'<think>.*?</think>', '', output, flags=re.DOTALL).strip()
    final_answer = re.sub(r'\*{2}(.*?)\*{2}', r'\1', final_answer)

    summary_filename = f"summary_{chunk_num}.txt" if chunk_num else "finalnotes.txt"
    with open(summary_filename, "w", encoding="utf-8") as f:
        f.write(final_answer)
    print(f"\nSummary saved to {summary_filename}")



process_audio(AUDIO_FILE_PATH)