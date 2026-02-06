import streamlit as st

st.set_page_config(
    page_title="Holistic Interview Intelligence",
    layout="wide"
)

# ---------- HERO ----------
st.markdown("""
# 🤖 Holistic Interview Intelligence

### AI-Powered Mock Interview Simulator
Offline • Voice • Behavior • AI Feedback
""")

st.markdown("---")

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("""
### 🎯 What You Get

✅ AI interviewer asks smart questions  
✅ Voice answer recording  
✅ Whisper transcription  
✅ AI feedback per answer  
✅ DroidCam nervousness detection  
✅ Fully offline system  

---

### 🧠 Interview Flow

1️⃣ Enter role  
2️⃣ Answer by voice  
3️⃣ AI evaluates  
4️⃣ Nervousness report generated  

""")

    st.markdown("")

    if st.button("🚀 Start Interview", use_container_width=True):
        st.switch_page("pages/1_Interview_Room.py")

with col2:
    st.image(
        "https://api.dicebear.com/7.x/bottts/png?seed=interview-ai",
        width=380
    )

st.markdown("---")

st.info("Tip: Allow microphone + camera permissions in browser for best experience.")