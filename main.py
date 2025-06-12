import pyttsx3
import gradio as gr
import os

def clean_text_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Combine lines while preserving paragraph breaks
    cleaned_paragraphs = []
    paragraph = ""

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if paragraph:
                cleaned_paragraphs.append(paragraph.strip())
                paragraph = ""
        else:
            if paragraph:
                paragraph += " " + stripped
            else:
                paragraph = stripped

    # Add the last paragraph if any
    if paragraph:
        cleaned_paragraphs.append(paragraph.strip())

    # Join paragraphs with a single newline
    cleaned_text = "\n\n".join(cleaned_paragraphs)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

    print(f"Cleaned text saved to: {output_file}")


# Example usage
clean_text_file("testtext.txt", "cleaned_text.txt")


def tts_microsoft(text, output_path="outputs/output-ms1.wav", voice_name="Microsoft Zira Desktop"):
    os.makedirs("outputs", exist_ok=True)
    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        if voice_name.lower() in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    return output_path

# Optional test outside Gradio
if __name__ == "__main__":
    with open("cleaned_text.txt", "r", encoding="utf-8") as f:
        content = f.read()
    print(tts_microsoft(content))

# Gradio app
# demo = gr.Interface(
#     fn=tts_microsoft, 
#     inputs=[gr.Text(label='Text')],
#     outputs=[gr.Audio(label='Audio', type="filepath")]
# )

# demo.launch()


