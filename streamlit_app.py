import streamlit as st
import openai
from gtts import gTTS
from io import BytesIO
import pandas as pd
import PyPDF2
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

openai_api_key = st.secrets["api_key"]
client = openai.OpenAI(api_key = openai_api_key)

def translate_text(text, target_language):
    prompt = f"Translate the following text to {target_language}:\n{text}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file


def extract_text_from_file(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    elif file.type == "text/plain":
        return str(file.read(), "utf-8")
    elif file.type in ["application/vnd.ms-excel", "text/csv"]:
        df = pd.read_csv(file)
        return df.to_string(index=False)
    elif file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file)
        return df.to_string(index=False)
    else:
        return "Unsupported file format."

def main():
    st.title("Multilingual Storytelling with Accents")

    st.write("Enter text or upload a file to translate and convert to speech.")

    text_input = st.text_area("Enter text here")
    uploaded_file = st.file_uploader("Or upload a file", type=["pdf", "txt", "csv", "xls", "xlsx"])

    if uploaded_file is not None:
        text_input = extract_text_from_file(uploaded_file)

    target_languages = {
        "Kannada": "kn",
        "Telugu": "te",
        "French": "fr",
        "English":"en"
        # Add more languages as needed
    }

    target_language = st.selectbox("Select target language", list(target_languages.keys()))
    translated_text = translate_text(text_input, target_language)
    if st.button("Translate"):
        if text_input:
            st.write(f"Translated text ({target_language}):")
            st.write(translated_text)

        else:
            st.write("Please enter text or upload a file.")
    if st.button("Generate Speech"):
        audio_file = text_to_speech(translated_text, target_languages[target_language])
        st.audio(audio_file, format='audio/mp3')
        st.download_button("Download Audio", data=audio_file, file_name="output.mp3", mime="audio/mp3")

if __name__ == '__main__':
    main()

