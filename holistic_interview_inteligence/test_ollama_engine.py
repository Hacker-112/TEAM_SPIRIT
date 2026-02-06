import ollama_interview_engine as ai

print("🎤 Generating question...")
q = ai.generate_question("Python Developer")
print("\nQuestion:", q)

print("\n🧑 Candidate answer test...\n")
analysis = ai.analyse_answer(q, "Python is a programming language.")
print(analysis)
