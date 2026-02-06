import streamlit as st
import ollama_interview_engine as ai
import voice_record_and_transcribe as voice
import camera_module as cam

st.set_page_config(layout="wide")

# ---------- SESSION STATE ----------
defaults = {
    "role": "",
    "qnum": 0,
    "question": None,
    "transcript": "",
    "feedback": None,
    "audio_path": None,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ---------- HEADER ----------
st.title("🎤 AI Interview Room")

colA, colB = st.columns([3, 1])
with colB:
    if st.button("🏠 Home"):
        st.switch_page("app_streamlit.py")

st.markdown("---")


# ---------- ROLE INPUT ----------
if st.session_state.qnum == 0:

    st.subheader("Enter Target Job Role")

    role = st.text_input("Example: Data Analyst, Python Developer")

    if st.button("🚀 Start Interview Session", use_container_width=True):

        cam.start_camera_session()   # ✅ START CAMERA

        with st.spinner("Preparing first question..."):
            q = ai.generate_question(role)

        st.session_state.role = role
        st.session_state.question = q
        st.session_state.qnum = 1
        st.rerun()


# ---------- INTERVIEW MODE ----------
if st.session_state.qnum > 0:

    left, right = st.columns([1, 1.2])

    with left:
        st.subheader("📷 Camera Status")
        st.success("System camera active for nervousness tracking")

    with right:

        st.subheader("🤖 AI Interviewer")

        st.image(
            "https://api.dicebear.com/7.x/bottts/png?seed=ai-interviewer",
            width=200
        )

        st.markdown(f"### Question {st.session_state.qnum}")
        st.info(st.session_state.question)

        st.markdown("---")

        # ---------- RECORD ----------
        if st.button("🎙️ Record Answer (20 sec)", use_container_width=True):

            with st.spinner("Recording..."):
                path = voice.record_fixed_duration(20)

            st.session_state.audio_path = path
            st.success("Recording finished")

        # ---------- TRANSCRIBE ----------
        if st.session_state.audio_path:

            if st.button("📝 Transcribe", use_container_width=True):

                with st.spinner("Transcribing..."):
                    st.session_state.transcript = voice.transcribe_audio(
                        st.session_state.audio_path
                    )

        # ---------- SHOW ----------
        if st.session_state.transcript:
            st.markdown("### Transcript")
            st.write(st.session_state.transcript)

            if st.button("🧠 Analyze Answer", use_container_width=True):

                with st.spinner("Analyzing..."):
                    st.session_state.feedback = ai.analyse_answer(
                        st.session_state.question,
                        st.session_state.transcript
                    )

        # ---------- FEEDBACK ----------
        if st.session_state.feedback:
            st.success(st.session_state.feedback)

            c1, c2 = st.columns(2)

            with c1:
                if st.button("➡️ Next Question", use_container_width=True):
                    st.session_state.question = ai.generate_question(
                        st.session_state.role
                    )
                    st.session_state.qnum += 1
                    st.session_state.transcript = ""
                    st.session_state.feedback = None
                    st.session_state.audio_path = None
                    st.rerun()

            with c2:
                if st.button("🏁 Finish Interview", use_container_width=True):

                    cam.stop_camera_session()   # ✅ STOP CAMERA

                    st.switch_page("pages/2_Report.py")