import ollama
with open("transcription.txt", "r", encoding="utf-8") as f:
    text = f.read()


# Stream the response from Ollama model
    response = ollama.chat(
        model='deepseek-r1:7b',
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
            'role': 'user', 'content': f"This text is a transcript from a meeting which have the possiblity of being impartial or incomplete:\n\n{text} \n\n You should ignore the timestamps. Now summarize it"
        }],
        stream=True  # Set to True for streaming responses
    )

output = ""
# Print each chunk as it arrives
for chunk in response:
    content = chunk.get('message', {}).get('content', '')
    output += content
    print(content, end='', flush=True)