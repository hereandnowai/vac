# app.py - Ultra Minimal Version (Approx. 16-18 lines)
import gradio as gr
import os, requests
import google.generativeai as genai
from bs4 import BeautifulSoup

# 1. Setup API Key & Gemini Model (Assumes API_KEY is set in HF Secrets)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")

# 2. Fetch Website Content (Assumes Success)
WEBSITE_URL = "https://hereandnowai.github.io/vac/" # Corrected URL
response = requests.get(WEBSITE_URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')
# Extract text directly from body - simplistic, might get junk
website_context = soup.body.get_text(separator='\n', strip=True) if soup.body else "Could not get website body."

# 3. Define Response Logic (Assumes Success)
def get_response(query, history): # history needed by ChatInterface
    prompt = f"Context from {WEBSITE_URL}:\n{website_context}\n\nQuestion: {query}\n\nAnswer based only on context:"
    # Directly return response text, no detailed error handling
    response = model.generate_content(prompt)
    return response.text

# 4. Create and Launch Gradio UI (Minimal)
if __name__ == "__main__":
    gr.ChatInterface(fn=get_response, title="Website FAQ Bot (Minimal)").launch()