import streamlit as st from transformers 
import pipeline from PyPDF2 
import PdfReader 
import random


# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Tangerine 🍊",
    page_icon="🍊",
    layout="wide"
)

# --------------------------------
# THEMES
# --------------------------------
themes = {
    "Orange": {
        "primary": "#ff914d",
        "background": "#fff7f0"
    },
    "Dark": {
        "primary": "#00c2ff",
        "background": "#121212"
    },
    "Ocean": {
        "primary": "#2196f3",
        "background": "#e3f2fd"
    },
    "Forest": {
        "primary": "#2e7d32",
        "background": "#e8f5e9"
    }
}

selected_theme = st.sidebar.selectbox(
    "🎨 Select Theme",
    list(themes.keys())
)

theme = themes[selected_theme]

# --------------------------------
# CUSTOM CSS
# --------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {theme["background"]};
}}

h1, h2, h3 {{
    color: {theme["primary"]};
}}

.highlight {{
    background-color: yellow;
    padding: 2px;
    border-radius: 4px;
}}

.flashcard {{
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}}

.quiz-box {{
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# TITLE
# --------------------------------
st.title("🍊 Tangerine")
st.subheader("AI Note Simplifier & Study Assistant")

# --------------------------------
# LOAD AI MODEL
# --------------------------------
@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )

summarizer = load_model()

# --------------------------------
# PDF UPLOAD
# --------------------------------
st.sidebar.header("📄 Upload Notes")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF File",
    type=["pdf"]
)

notes = ""

if uploaded_file is not None:
    pdf_reader = PdfReader(uploaded_file)

    for page in pdf_reader.pages:
        text = page.extract_text()

        if text:
            notes += text

# --------------------------------
# PASTE NOTES
# --------------------------------
typed_notes = st.text_area(
    "✍️ Paste Notes Here",
    height=250
)

if typed_notes:
    notes += typed_notes

# --------------------------------
# HIGHLIGHT FEATURE
# --------------------------------
st.header("📌 Highlight Text")

highlight_word = st.text_input(
    "Enter word to highlight"
)

if notes and highlight_word:

    highlighted_text = notes.replace(
        highlight_word,
        f"<span class='highlight'>{highlight_word}</span>"
    )

    st.markdown(
        highlighted_text,
        unsafe_allow_html=True
    )

# --------------------------------
# SIMPLIFY NOTES
# --------------------------------
st.header("📝 Simplified Notes")

if st.button("Simplify Notes"):

    if notes.strip() == "":
        st.warning("Please upload or paste notes.")

    else:

        with st.spinner("Generating summary..."):

            summary = summarizer(
                notes[:2000],
                max_length=150,
                min_length=40,
                do_sample=False
            )

            simplified = summary[0]["summary_text"]

            sentences = simplified.split(".")

            st.success("Summary Generated!")

            for sentence in sentences:

                sentence = sentence.strip()

                if sentence:
                    st.markdown(f"✅ {sentence}")

# --------------------------------
# FLASHCARDS
# --------------------------------
st.header("🃏 Flashcards")

if st.button("Generate Flashcards"):

    if notes.strip() == "":
        st.warning("Please upload or paste notes.")

    else:

        sentences = notes.split(".")[:10]

        for i, sentence in enumerate(sentences):

            sentence = sentence.strip()

            if len(sentence) > 25:

                st.markdown(
                    f"""
                    <div class='flashcard'>
                    <h4>Flashcard {i+1}</h4>

                    <b>Question:</b><br>
                    Explain the following:<br><br>

                    <i>{sentence[:100]}...</i>

                    <br><br>

                    <b>Answer:</b><br>
                    {sentence}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# --------------------------------
# QUIZ FEATURE
# --------------------------------
st.header("🎯 Quiz Yourself")

if st.button("Generate Quiz"):

    if notes.strip() == "":
        st.warning("Please upload or paste notes.")

    else:

        sentences = notes.split(".")[:5]

        score = 0

        for i, sentence in enumerate(sentences):

            sentence = sentence.strip()

            if len(sentence) > 30:

                words = sentence.split()

                if len(words) > 6:

                    answer = random.choice(words)

                    question = sentence.replace(
                        answer,
                        "______",
                        1
                    )

                    st.markdown(
                        f"""
                        <div class='quiz-box'>
                        <b>Question {i+1}</b><br><br>
                        {question}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    user_answer = st.text_input(
                        f"Answer for Question {i+1}",
                        key=i
                    )

                    if user_answer.lower() == answer.lower():
                        score += 1

        st.success("Quiz Generated!")

# --------------------------------
# ORIGINAL NOTES
# --------------------------------
with st.expander("📚 View Original Notes"):
    st.write(notes)

# 📁 File: `requirements.txt`


streamlit
transformers
torch
sentencepiece
PyPDF2

# 📁 File: `.streamlit/config.toml`


[theme]
primaryColor="#ff914d"
backgroundColor="#fff7f0"
secondaryBackgroundColor="#ffffff"
textColor="#000000"
font="sans serif"


