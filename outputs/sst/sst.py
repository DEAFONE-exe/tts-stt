from faster_whisper import WhisperModel
import ollama
import re

# Load the model (use "base", "small", "medium", or "large")device="cuda"
#model = WhisperModel("base", compute_type="float16")
model = WhisperModel("base", device="cpu")

# Transcribe the audio file
segments, info = model.transcribe(
    "../yt-video.mp3",
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
            #'role': 'user', 'content': f"This is a transcript of what someone said during a meeting and have the possibility of being impartial:\n\n{text} \n\n You should ignore the timestamps. Now summarize it"
            'role': 'user', 'content': f"This is a transcript from an online video guide from youtube:\n\n{text} \n\n You should ignore the timestamps. Now summarize it"
        }],
        stream=True  # Set to True for streaming responses
    )

output = ""
# Print each chunk as it arrives
for chunk in response:
    content = chunk.get('message', {}).get('content', '')
    output += content
    print(content, end='', flush=True)

final_answer = re.sub(r'<think>.*?</think>', # We're searching for think tags
                          '', # We'll replace them with empty spaces
                          output, # In response_content
                          flags=re.DOTALL).strip() # (dot) should match newlines (\n) as well.

final_answer = re.sub(r'\*{2}(.*?)\*{2}', r'\1', final_answer)  # Remove **bold** formatting

with open("finalnotes.txt", "w", encoding="utf-8") as f:
    f.write(final_answer)        # write to file
