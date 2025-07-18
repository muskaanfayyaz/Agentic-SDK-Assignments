# mood_handoff.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load the .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# Simulate Runner & Agent behavior
class Runner:
    @staticmethod
    def run(agent_func, *args, **kwargs):
        return agent_func(*args, **kwargs)

# Agent 1: Mood Detector
def mood_detector(user_message: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""What is the user's mood from this message? 
Respond with one word only: happy, sad, stressed, or neutral.

Message: "{user_message}" """

    response = model.generate_content(prompt)
    mood = response.text.strip().lower()

    allowed = ["happy", "sad", "stressed", "neutral"]
    for a in allowed:
        if a in mood:
            return a
    return "neutral"

# Agent 2: Activity Suggestion
def activity_suggester(mood: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Suggest a simple activity to someone who is feeling {mood}. Keep it short and friendly."
    response = model.generate_content(prompt)
    return response.text.strip()

# Main App
if __name__ == "__main__":
    message = input("How are you feeling today? ")

    mood = Runner.run(mood_detector, message)
    print(f"\n🧠 Detected Mood: {mood}")

    if mood in ["sad", "stressed"]:
        suggestion = Runner.run(activity_suggester, mood)
        print(f"💡 Suggested Activity: {suggestion}")
    else:
        print("✅ You're doing great! Keep it up. 😊")
