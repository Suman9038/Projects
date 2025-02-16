# import google.generativeai as genai
from google import genai
from dotenv import load_dotenv
import os



# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY") 
# if not api_key:
#     raise ValueError("⚠️ OPENAI_API_KEY not found in environment variables!")

# print(f"API Key Found: {api_key[:5]}**********") 
client=genai.Client(api_key="AIzaSyBI31vzusPl4hblZg6Rih6qN15lvcnns5Q")

def predict_priority(description: str) :
    prompt = f"""
    You are an AI assistant that categorizes tasks into three priority levels: HIGH, MEDIUM, and LOW. 
    Analyze the urgency of the following task description and return only the priority level.
    Task: "{description}"
    Respond with only one word: HIGH, MEDIUM, or LOW.
    """
    response =client.models.generate_content(model="gemini-pro", contents=prompt)
    return response.text.strip().upper()

# TEST FOR CHECHKING
# task = "Finish the project report before the deadline."
# priority = predict_priority(task)
# print(priority)  
