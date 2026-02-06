print("FILE STARTED")

import ollama_interview_engine as ai
from voice_analysis import record_until_enter, transcribe_audio

# ===============================
# START INTERVIEW
# ===============================

role = input("Enter job role: ")

print("\n🎤 Interview started!")
print("💡 Type 'exit' anytime to end interview.\n")

# First question
question = ai.generate_question(role)

# ===============================
# INTERVIEW LOOP
# ===============================
while True:

    print("\n🤖 Interviewer:", question)

    start = input("\nPress ENTER to start answering (or type 'exit'): ")
    if start.lower() == "exit":
        print("\n👋 Interview ended")
        break

    # 🎤 Record answer
    audio_file = record_until_enter()

    # 🧠 Speech → Text
    answer = transcribe_audio(audio_file)
    print("\n🧑 Your answer:", answer)

    # Allow exit by speaking too
    if answer.lower().strip() in ["exit", "quit", "stop"]:
        print("\n👋 Interview ended")
        break

    # 🤖 AI feedback
    print("\n🧠 Evaluating answer...")
    feedback = ai.analyse_answer(question, answer)
    print("\n📊 AI Feedback:\n", feedback)

    # Next question
    print("\n🎯 Generating next question...")
    question = ai.generate_question(role)
