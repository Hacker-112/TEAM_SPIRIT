import gemini_interview_engine as ai

print("\n🎤 Generating interview question...\n")

question = ai.generate_question("Python Developer")
print("QUESTION:")
print(question)

user_answer = input("\nType your answer:\n")

print("\n📊 ANALYSIS:")
print(ai.analyze_answer(question, user_answer))

print("\n✨ IDEAL ANSWER:")
print(ai.improve_answer(question, user_answer))
