from faster_whisper import WhisperModel
import ollama

# Load the model (use "base", "small", "medium", or "large")device="cuda"
#model = WhisperModel("base", compute_type="float16")
model = WhisperModel("base", device="cpu")

# Transcribe the audio file
segments, info = model.transcribe(
    "../output-ms1.wav",
    language="en",
    beam_size=5,
    vad_filter=True,
    temperature=0
)

print("Detected language:", info.language)

# Open a file in write mode
with open("transcription.txt", "w", encoding="utf-8") as f:
    for segment in segments:
        line = f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}\n"
        print(line, end='')  # print to console
        f.write(line)        # write to file

with open("transcription.txt", "r", encoding="utf-8") as f:
    text = f.read()


# Stream the response from Ollama model
    response = ollama.chat(
        model='deepseek-r1:1.5b',
        messages=[{
            'role': 'system', 'content': (
                "Use ONLY the given content to answer the user's question. "
                "Do NOT make assumptions or fabricate information. "
                "Use bullet points or numbered lists for clarity and readability. "
                "Avoid redundant explanations — if something is implied (e.g., no number means no call), don't restate it. "
                "Respond in a clear, concise, and well-formatted manner. "
                "Always respond with emojis to make it engaging 🧠✨. Be casual, friendly, and concise."
            )
        }, {
            'role': 'user', 'content': f"These are what someone said during a meeting and have the possibility of being impartial:\n\n{text} \n\n now summarize the notes"
        }],
        stream=True  # Set to True for streaming responses
    )

output = ""
# Print each chunk as it arrives
for chunk in response:
    content = chunk.get('message', {}).get('content', '')
    output += content
    print(content, end='', flush=True)