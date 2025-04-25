# app.py - Simplified Version with Web Scraping
import gradio as gr
import os
import google.generativeai as genai
import requests                 # Added
from bs4 import BeautifulSoup   # Added
import time                     # Optional: For adding a small delay if needed

# --- Configuration & Setup ---
# 1. Get API Key (Relies on Hugging Face Secrets)
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment secrets!")

# 2. Fetch and Parse Website Content
WEBSITE_URL = "https://hereandnowai.github.io/vac/" # Target website
website_context = f"Error: Could not fetch content from {WEBSITE_URL}" # Default error

try:
    print(f"Attempting to fetch content from {WEBSITE_URL}...")
    headers = {'User-Agent': 'Mozilla/5.0'} # Act like a browser
    response = requests.get(WEBSITE_URL, headers=headers, timeout=15) # Added headers and timeout
    response.raise_for_status() # Check for HTTP errors (4xx, 5xx)

    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Attempt to extract main content ---
    # Try finding specific tags first (Ideal, but requires knowing the site structure)
    # main_content = soup.find('main') or soup.find('article') or soup.find('div', id='content') # Examples
    main_content = soup.body # Simple fallback: get text from the whole body

    if main_content:
         # Extract text, separate paragraphs by newline, remove extra whitespace
         website_context = main_content.get_text(separator='\n', strip=True)
         # Optional: Clean up multiple blank lines
         website_context = "\n".join([line for line in website_context.split('\n') if line.strip()])
         print("Website content fetched and parsed successfully.")
    else:
        website_context = "Error: Could not find main content body on the page."
        print(website_context)

except requests.exceptions.RequestException as e:
    website_context = f"Error fetching website: {e}"
    print(website_context)
except Exception as e:
    website_context = f"Error parsing website: {e}"
    print(website_context)


# 3. Configure Gemini Model
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest")
    print("Gemini model initialized.")
except Exception as e:
    print(f"Error initializing Gemini: {e}")
    model = None

# --- Core Chat Logic ---
def get_response(user_query, chat_history):
    if not model:
        return "AI model is not available right now."
    if "Error:" in website_context: # Check if scraping failed
        return website_context

    # 4. Construct Prompt using website content
    prompt = f"""You are an FAQ assistant for HERE AND NOW AI answering questions about value-added courses described on their website.
Use ONLY the following text extracted from the website {WEBSITE_URL} to answer the question.
Do not make up information. If the answer isn't in the text, say you cannot find the answer in the website content and suggest contacting info@hereandnowai.com.

**Website Content:**
---
{website_context}
---

**Question:** {user_query}

**Answer:**"""

    # 5. Call API & Get Response
    try:
        response = model.generate_content(prompt)
        # Use response.text directly if available, otherwise provide a fallback
        return response.text if hasattr(response, 'text') and response.text else "Sorry, I couldn't formulate a response based on the website content."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "An error occurred while contacting the AI service."

# --- Gradio Interface (Minimal) ---
# 6. Create and Launch Interface
iface = gr.ChatInterface(
            fn=get_response,
            title="Website FAQ Bot",
            description=f"Ask questions about the content on {WEBSITE_URL}"
        )

if __name__ == "__main__":
    # Optional: Add a small delay before launch, sometimes helps ensure network is ready on startup
    # time.sleep(2)
    iface.launch()