import streamlit as st
import time
from datetime import datetime

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Tangerine 🍊",
    page_icon="🍊",
    layout="centered"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = 0

# -----------------------------------
# THEMES
# -----------------------------------
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
    "🎨 Select Theme",
    list(themes.keys())
)

theme = themes[selected_theme]

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown(f"""
<style>
.stApp {{
    background-color: {theme["background"]};
    color: {theme["text"]};
}}

h1, h2, h3 {{
    color: {theme["primary"]};
    text-align: center;
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
    box-shadow: 0 0 40px rgba(0,0,0,0.2);
}}

.todo-box {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
}}

.streak-box {{
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin-top: 20px;
}}

.task {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
}}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("🍊 Tangerine")
st.subheader("Pomodoro Study App")

# -----------------------------------
# POMODORO SETTINGS
# -----------------------------------
study_minutes = st.slider(
    "⏳ Study Time (minutes)",
    1,
    60,
    25
)

break_minutes = st.slider(
    "☕ Break Time (minutes)",
    1,
    30,
    5
)

# -----------------------------------
# TIMER DISPLAY
# -----------------------------------
timer_placeholder = st.empty()

timer_placeholder.markdown(
    f"""
    <div class="tangerine">
        {study_minutes}:00
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# START TIMER
# -----------------------------------
if st.button("▶️ Start Pomodoro"):

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

    st.success("🎉 Study Session Complete!")

    st.session_state.completed_sessions += 1
    st.session_state.streak += 1

    st.balloons()

# -----------------------------------
# STREAK SYSTEM
# -----------------------------------
st.header("🔥 Study Streak")

st.markdown(
    f"""
    <div class="streak-box">
        <h2>{st.session_state.streak} Day Streak 🔥</h2>
        <p>Completed Sessions: {st.session_state.completed_sessions}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# TO DO LIST
# -----------------------------------
st.header("📝 To-Do List")

new_task = st.text_input("Add Assignment or Task")

if st.button("➕ Add Task"):

    if new_task.strip() != "":
        st.session_state.tasks.append(new_task)

# Display tasks
st.markdown('<div class="todo-box">', unsafe_allow_html=True)

if len(st.session_state.tasks) == 0:
    st.write("No tasks added yet.")

for i, task in enumerate(st.session_state.tasks):

    col1, col2 = st.columns([8,1])

    with col1:
        st.markdown(f"<div class='task'>✅ {task}</div>",
                    unsafe_allow_html=True)

    with col2:
        if st.button("❌", key=i):
            st.session_state.tasks.pop(i)
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("---")
st.caption("🍊 Tangerine Pomodoro Study App")