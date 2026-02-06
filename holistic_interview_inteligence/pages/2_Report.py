import streamlit as st
import camera_module as cam

st.title("📊 Final Interview Report")

score = cam.run_nervousness_analysis()

st.subheader("Nervousness Score")
st.write(score)