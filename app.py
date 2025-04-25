# app.py
import gradio as gr
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY")
CONTEXT_FILE = "prospectus-context.txt"

if not API_KEY:
    print("Error: GEMINI_API_KEY not found. Please set it in secrets or .env file.")
    # raise ValueError("API Key not configured")

# Load Prospectus Context
try:
    context_path = os.path.join(os.path.dirname(__file__), CONTEXT_FILE)
    with open(context_path, "r", encoding="utf-8") as f:
        prospectus_context = f.read()
    print("Prospectus context loaded successfully.")
except FileNotFoundError:
    print(f"Error: Context file '{CONTEXT_FILE}' not found at expected path: {context_path}")
    prospectus_context = "Error: Course context is unavailable. Cannot answer questions accurately."
except Exception as e:
    print(f"Error loading context file: {e}")
    prospectus_context = "Error: Failed to load course context."

# --- Gemini API Setup ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
    )
    print("Gemini model initialized successfully.")
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None

# --- Core Chat Logic ---
def get_gemini_response(user_query, chat_history):
    if not model:
        return "Sorry, the AI model is not available at the moment. Please try again later."
    if "Error: Course context is unavailable" in prospectus_context:
         return prospectus_context

    full_prompt = f"""
You are a helpful and concise FAQ assistant for HERE AND NOW AI. Your primary goal is to answer questions based *only* on the provided course prospectus information below. Do not invent information or answer questions outside this context. If the answer isn't in the text, clearly state that you don't have the information and suggest contacting the institute via info@hereandnowai.com. Keep responses brief and clear.

**Prospectus Context:**
---
{prospectus_context}
---

**User Question:** {user_query}

**Answer:**"""

    try:
        response = model.generate_content(full_prompt)
        ai_response_text = "Sorry, I encountered an issue generating a response. Please try asking differently or contact support."

        if hasattr(response, 'text') and response.text:
            ai_response_text = response.text
        elif hasattr(response, 'prompt_feedback') and response.prompt_feedback and hasattr(response.prompt_feedback, 'block_reason'):
             ai_response_text = f"Your request was blocked: {response.prompt_feedback.block_reason}. Please rephrase."
        elif hasattr(response, 'candidates') and response.candidates and hasattr(response.candidates[0], 'finish_reason') and response.candidates[0].finish_reason != 'STOP':
             ai_response_text = f"The response was incomplete ({response.candidates[0].finish_reason}). Please try again."

        lc = ai_response_text.lower()
        if "don't know" in lc or "don't have information" in lc or "not mentioned" in lc or "cannot answer" in lc:
             if "info@hereandnowai.com" not in ai_response_text:
                ai_response_text += " For more details, please contact info@hereandnowai.com."

        return ai_response_text.strip()

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return "An error occurred while contacting the AI service. Please try again."

# --- Gradio Interface ---
chatbot_interface = gr.ChatInterface(
    fn=get_gemini_response,
    chatbot=gr.Chatbot(height=400, label="Chat Window"),
    textbox=gr.Textbox(placeholder="Ask about our AI courses...", container=False, scale=7),
    title="HERE AND NOW AI Course FAQ Bot",
    description="Ask me questions about the Business Analytics with AI or Full-Stack AI Developer programs (based on the 2025-2026 prospectus).",
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="purple"),
    examples=[
        "What prerequisites are needed for the Business Analytics course?",
        "Tell me about the Full-Stack AI Developer curriculum.",
        "Who is the CEO?",
        "What is the fee for the full-stack program?",
        "Do you offer placement assistance?",
    ],
    cache_examples=False,
    # Removed clear_btn="Clear Chat"
    # Still recommend adding type="messages" to handle the UserWarning if needed
    # type="messages",
 )

# --- Launch the App ---
if __name__ == "__main__":
    chatbot_interface.launch(server_name="0.0.0.0")