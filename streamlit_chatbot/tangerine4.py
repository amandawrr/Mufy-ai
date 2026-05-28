
import streamlit as st
import time
import random
from transformers import pipeline
from PyPDF2 import PdfReader

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Tangerine 🍊",
    page_icon="🍊",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATES
# ---------------------------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = 0

# ---------------------------------------------------
# THEMES
# ---------------------------------------------------
themes = {
    "Orange": {
        "primary": "#ff914d",
        "background": "#fff5eb",
        "text": "#000000"
    },
    "Dark": {
        "primary": "#ff914d",
        "background": "#121212",
        "text": "#ffffff"
    },
    "Ocean": {
        "primary": "#2196f3",
        "background": "#e3f2fd",
        "text": "#000000"
    },
    "Forest": {
        "primary": "#2e7d32",
        "background": "#e8f5e9",
        "text": "#000000"
    }
}

selected_theme = st.sidebar.selectbox(
    "🎨 Choose Theme",
    list(themes.keys())
)

theme = themes[selected_theme]

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown(f"""
<style>

.stApp {{
    background-color: {theme["background"]};
    color: {theme["text"]};
}}

h1, h2, h3 {{
    color: {theme["primary"]};
}}

.stButton > button {{
    background-color: {theme["primary"]};
    color: white;
    border-radius: 12px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}}

.stButton > button:hover {{
    background-color: #ff6f00;
    transform: scale(1.03);
}}

.tangerine {{
    width: 260px;
    height: 260px;
    background: linear-gradient(145deg, #ff914d, #ff6f00);
    border-radius: 50%;
    margin: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    font-weight: bold;
    color: white;
    box-shadow: 0 0 30px rgba(0,0,0,0.2);
}}

.flashcard {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}}

.todo-box {{
    background: white;
    padding: 20px;
    border-radius: 15px;
}}

.highlight {{
    background-color: yellow;
    padding: 2px;
    border-radius: 4px;
}}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🍊 Tangerine")
st.subheader("All-in-One Study Productivity App")

# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2 = st.tabs(["📝 Notes", "🍊 Pomodoro"])

# ===================================================
# NOTES TAB
# ===================================================
with tab1:

    st.header("📝 AI Note Simplifier")

    # -----------------------------------------------
    # LOAD AI MODEL
    # -----------------------------------------------
    @st.cache_resource
    def load_model():
        return pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    summarizer = load_model()

    # -----------------------------------------------
    # PDF UPLOAD
    # -----------------------------------------------
    uploaded_file = st.file_uploader(
        "📄 Upload PDF Notes",
        type=["pdf"],
        key="pdf_upload"
    )

    notes = ""

    if uploaded_file:
        pdf_reader = PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()

            if text:
                notes += text

    # -----------------------------------------------
    # PASTE NOTES
    # -----------------------------------------------
    typed_notes = st.text_area(
        "✍️ Paste Notes Here",
        height=250,
        key="notes_input"
    )

    if typed_notes:
        notes += typed_notes

    # -----------------------------------------------
    # HIGHLIGHT FEATURE
    # -----------------------------------------------
    st.subheader("📌 Highlight Text")

    highlight_word = st.text_input(
        "Enter word to highlight",
        key="highlight_input"
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

    # -----------------------------------------------
    # SIMPLIFY NOTES
    # -----------------------------------------------
    st.subheader("📝 Simplified Notes")

    if st.button("Simplify Notes", key="simplify_button"):

        if notes.strip() == "":
            st.warning("Please upload or paste notes.")

        else:

            with st.spinner("Simplifying notes..."):

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

    # -----------------------------------------------
    # FLASHCARDS
    # -----------------------------------------------
    st.subheader("🃏 Flashcards")

    if st.button("Generate Flashcards", key="flashcards_button"):

        if notes.strip() == "":
            st.warning("Please upload notes.")

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

    # -----------------------------------------------
    # QUIZ FEATURE
    # -----------------------------------------------
    st.subheader("🎯 Quiz Yourself")

    if st.button("Generate Quiz", key="quiz_button"):

        if notes.strip() == "":
            st.warning("Please upload notes.")

        else:

            sentences = notes.split(".")[:5]

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

                        st.write(f"### Question {i+1}")
                        st.write(question)

                        st.text_input(
                            "Your Answer",
                            key=f"quiz_{i}"
                        )

# ===================================================
# POMODORO TAB
# ===================================================
with tab2:

    st.header("🍊 Pomodoro Timer")

    # -----------------------------------------------
    # TIMER SETTINGS
    # -----------------------------------------------
    study_minutes = st.slider(
        "⏳ Study Minutes",
        1,
        60,
        25,
        key="study_slider"
    )

    break_minutes = st.slider(
        "☕ Break Minutes",
        1,
        30,
        5,
        key="break_slider"
    )

    # -----------------------------------------------
    # TIMER DISPLAY
    # -----------------------------------------------
    timer_placeholder = st.empty()

    timer_placeholder.markdown(
        f"""
        <div class="tangerine">
            {study_minutes}:00
        </div>
        """,
        unsafe_allow_html=True
    )

    # -----------------------------------------------
    # START TIMER
    # -----------------------------------------------
    if st.button("▶️ Start Pomodoro", key="pomodoro_button"):

        total_seconds = study_minutes * 60

        for remaining in range(total_seconds, 0, -1):

            mins = remaining // 60
            secs = remaining % 60

            timer_placeholder.markdown(
                f"""
                <div class="tangerine">
                    {mins:02}:{secs:02}
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(1)

        st.success("🎉 Session Completed!")

        st.session_state.completed_sessions += 1
        st.session_state.streak += 1

        st.balloons()

    # -----------------------------------------------
    # STREAK SYSTEM
    # -----------------------------------------------
    st.subheader("🔥 Study Streak")

    st.write(
        f"Current Streak: {st.session_state.streak} 🔥"
    )

    st.write(
        f"Completed Sessions: {st.session_state.completed_sessions}"
    )

    # -----------------------------------------------
    # TO DO LIST
    # -----------------------------------------------
    st.subheader("📝 To-Do List")

    new_task = st.text_input(
        "Add Assignment",
        key="task_input"
    )

    if st.button("➕ Add Task", key="add_task_button"):

        if new_task.strip() != "":
            st.session_state.tasks.append(new_task)

    st.markdown("<div class='todo-box'>",
                unsafe_allow_html=True)

    if len(st.session_state.tasks) == 0:
        st.write("No tasks added.")

    for i, task in enumerate(st.session_state.tasks):

        col1, col2 = st.columns([8,1])

        with col1:
            st.write(f"✅ {task}")

        with col2:
            if st.button("❌", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.caption("🍊 Tangerine Study App")

# 📁 `requirements.txt`


streamlit
transformers
torch
sentencepiece
PyPDF2


# 📁 `.streamlit/config.toml`


[theme]
primaryColor="#ff914d"
backgroundColor="#fff5eb"
secondaryBackgroundColor="#ffffff"
textColor="#000000"
font="sans serif"