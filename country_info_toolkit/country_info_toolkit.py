# country_info_toolkit.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")

# === Runner Framework ===
class Agent:
    def run(self, input_text: str) -> str:
        raise NotImplementedError("Agent must implement run method.")

class Runner:
    @staticmethod
    def run(agent: Agent, input_text: str) -> str:
        return agent.run(input_text)

# === Tool Agent 1: Capital Finder ===
class CapitalAgent(Agent):
    def run(self, country: str) -> str:
        prompt = f"What is the capital city of {country}?"
        response = MODEL.generate_content(prompt)
        return response.text.strip()

# === Tool Agent 2: Language Finder ===
class LanguageAgent(Agent):
    def run(self, country: str) -> str:
        prompt = f"What is the official language spoken in {country}?"
        response = MODEL.generate_content(prompt)
        return response.text.strip()

# === Tool Agent 3: Population Finder ===
class PopulationAgent(Agent):
    def run(self, country: str) -> str:
        prompt = f"What is the approximate population of {country} as of the latest data?"
        response = MODEL.generate_content(prompt)
        return response.text.strip()

# === Orchestrator Agent ===
class OrchestratorAgent(Agent):
    def __init__(self):
        self.capital_agent = CapitalAgent()
        self.language_agent = LanguageAgent()
        self.population_agent = PopulationAgent()

    def run(self, country: str) -> str:
        try:
            capital = Runner.run(self.capital_agent, country)
            language = Runner.run(self.language_agent, country)
            population = Runner.run(self.population_agent, country)

            return (
                f"🌍 Country: {country.title()}\n"
                f"🏛 Capital: {capital}\n"
                f"🗣 Language: {language}\n"
                f"👥 Population: {population}"
            )
        except Exception as e:
            return f"❌ Failed to get info for {country}: {e}"

# === Main Program ===
if __name__ == "__main__":
    country_input = input("Enter a country name: ")
    orchestrator = OrchestratorAgent()
    result = Runner.run(orchestrator, country_input)
    print("\n" + result)
