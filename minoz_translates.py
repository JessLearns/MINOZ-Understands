import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from deep_translator import GoogleTranslator
import streamlit as st

# Step 1: Extract Subtitles from YouTube Videos
def get_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    if "?v=" in youtube_url:
        return youtube_url.split("?v=")[1]
    elif "/v/" in youtube_url:
        return youtube_url.split("/v/")[1]
    else:
        raise ValueError("Invalid YouTube URL")

def fetch_subtitles(video_id, language_code="ko"):
    """Fetch subtitles using the YouTubeTranscriptApi for a specific language."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        return " ".join([entry['text'] for entry in transcript])
    except TranscriptsDisabled:
        return "Error: Subtitles are disabled for this video."
    except NoTranscriptFound:
        return f"Error: No subtitles found for the requested language ({language_code})."
    except Exception as e:
        return f"Error fetching subtitles: {str(e)}"

# Step 2: Translate Subtitles
def translate_text(text, target_language):
    """Translate text into the target language."""
    try:
        translator = GoogleTranslator(source="auto", target=target_language)
        return translator.translate(text)
    except Exception as e:
        return f"Error translating to {target_language}: {str(e)}"

# Streamlit App
st.title("Minoz Understands")

# Input for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:")

# Dropdown for Target Language
target_language = st.selectbox(
    "Select Language to Translate To:",
    ["en", "id", "hi", "es"],
    format_func=lambda x: {
        "en": "English",
        "id": "Indonesian",
        "hi": "Hindi",
        "es": "Spanish"
    }.get(x, x)
)

if st.button("Translate Subtitles"):
    try:
        video_id = get_video_id(youtube_url)
        st.write("Fetching subtitles...")
        subtitles = fetch_subtitles(video_id, language_code="ko")  # Use 'ko' for Korean

        if "Error" in subtitles:
            st.error(subtitles)
        else:
            st.write("Translating subtitles...")
            translation = translate_text(subtitles, target_language)

            if "Error" in translation:
                st.error(translation)
            else:
                st.success("Translation completed!")
                st.text_area("Translated Subtitles:", translation, height=300)

                # Option to download translation
                st.download_button(
                    label="Download Translation",
                    data=translation,
                    file_name=f"{video_id}_{target_language}.txt",
                    mime="text/plain"
                )
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
