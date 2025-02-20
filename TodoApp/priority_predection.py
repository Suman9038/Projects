
from google import genai
from dotenv import load_dotenv
import os
from .config import settings

api_key= str(settings.GEMINI_API_KEY)
client=genai.Client(api_key="api_key")

def predict_priority(description: str) :
    prompt = f"""
    You are an AI assistant that categorizes tasks into three priority levels: HIGH, MEDIUM, and LOW. 
    Analyze the urgency of the following task description and return only the priority level.
    Task: "{description}"
    Respond with only one word: HIGH, MEDIUM, or LOW.
    """
    response =client.models.generate_content(model="gemini-pro", contents=prompt)
    return response.text.strip().upper()
 