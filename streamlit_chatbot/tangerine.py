import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader
import random

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Tangerine 🍊",
    page_icon="🍊",
    layout="wide"
)

# ----------------------------
# THEMES
# ----------------------------
themes = {
    "Orange": "#ff914d",
    "Dark": "#1e1e1e",
    "Ocean": "#2196f3",
    "Forest": "#2e7d32"
}

selected_theme = st.sidebar.selectbox(
    "Choose Theme",
    list(themes.keys())
)

theme_color = themes[selected_theme]

# Apply custom styling
st.markdown(f"""
<style>
.stApp {{
    background-color: #f5f5f5;
}}

h1, h2, h3 {{
    color: {theme_color};
}}

.highlight {{
    background-color: yellow;
    padding: 2px;
    border-radius: 4px;
}}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("🍊 Tangerine")
st.subheader("AI-Powered Study & Note Simplifier")

# ----------------------------
# LOAD AI MODEL
# ----------------------------
@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )

summarizer = load_summarizer()

# ----------------------------
# INPUT OPTIONS
# ----------------------------
st.sidebar.header("Upload Notes")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

notes = ""

# Read PDF
if uploaded_file:
    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        notes += page.extract_text()

# Text input
typed_notes = st.text_area(
    "Or Paste Notes Here",
    height=250
)

if typed_notes:
    notes += typed_notes

# ----------------------------
# HIGHLIGHT FEATURE
# ----------------------------
st.subheader("📌 Highlight Text")

highlight_word = st.text_input(
    "Enter word to highlight"
)

if notes and highlight_word:
    highlighted_notes = notes.replace(
        highlight_word,
        f"<span class='highlight'>{highlight_word}</span>"
    )

    st.markdown(
        highlighted_notes,
        unsafe_allow_html=True
    )

# ----------------------------
# SIMPLIFY NOTES
# ----------------------------
st.header("📝 Simplified Notes")

if st.button("Simplify Notes"):

    if notes.strip() == "":
        st.warning("Please upload or paste notes.")
    else:

        with st.spinner("Simplifying..."):

            summary = summarizer(
                notes[:2000],
                max_length=150,
                min_length=40,
                do_sample=False
            )

            simplified = summary[0]["summary_text"]

            sentences = simplified.split(".")

            for sentence in sentences:
                sentence = sentence.strip()

                if sentence:
                    st.markdown(f"✅ {sentence}")

# ----------------------------
# FLASHCARDS
# ----------------------------
st.header("🃏 Flashcards")

if st.button("Generate Flashcards"):

    if notes.strip() == "":
        st.warning("Please upload notes first.")

    else:

        sentences = notes.split(".")[:10]

        for i, sentence in enumerate(sentences):

            sentence = sentence.strip()

            if len(sentence) > 20:

                st.markdown(f"""
                ### Flashcard {i+1}

                **Question:**  
                What is the meaning of:

                "{sentence[:80]}..."

                **Answer:**  
                {sentence}
                """)

# ----------------------------
# QUIZ FEATURE
# ----------------------------
st.header("🎯 Quiz Yourself")

if st.button("Generate Quiz"):

    if notes.strip() == "":
        st.warning("Please upload notes first.")

    else:

        sentences = notes.split(".")[:5]

        score = 0

        for i, sentence in enumerate(sentences):

            sentence = sentence.strip()

            if len(sentence) > 20:

                words = sentence.split()

                if len(words) > 5:

                    answer = words[-1]

                    question = sentence.replace(
                        answer,
                        "______"
                    )

                    st.write(f"Q{i+1}: {question}")

                    user_answer = st.text_input(
                        f"Your answer {i+1}",
                        key=i
                    )

                    if user_answer.lower() == answer.lower():
                        score += 1

        st.success(f"Quiz Completed!")

# ----------------------------
# NOTES DISPLAY
# ----------------------------
with st.expander("📚 View Original Notes"):
    st.write(notes)