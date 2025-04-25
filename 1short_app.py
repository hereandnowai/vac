import gradio as gr
import os
import google.generativeai as genai
import pathlib

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment secrets!") # Fail fast if key is missing

try:
    context_path = os.path.join(os.path.dirname(__file__), "prospectus-context.txt")
    prospectus_context = pathlib.Path(context_path).read_text(encoding="utf-8")
except FileNotFoundError:
    prospectus_context = "Error: Prospectus context file not found. Cannot answer questions."

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    model = None # Allow app to load, but function will return error

def get_response(user_query, chat_history): # chat_history is required by ChatInterface but not used here
    if not model or "Error:" in prospectus_context:
        return prospectus_context if "Error:" in prospectus_context else "AI model not initialized."

    prompt = f"""Context: {prospectus_context}\n\nQuestion: {user_query}\n\nAnswer based only on context:"""

    try:
        response = model.generate_content(prompt)
        # Basic check if response has text, otherwise return generic message
        return response.text if hasattr(response, 'text') and response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "An error occurred while contacting the AI."

iface = gr.ChatInterface(
            fn=get_response,
            title="Simple FAQ Bot",
            description="Ask questions based on the course info.")

if __name__ == "__main__":
    iface.launch() # Launch the minimal interface