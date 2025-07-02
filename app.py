# 📱 Classroom Helper – AI Teaching Assistant (Mobile Ready)
import streamlit as st
import pytesseract
from PIL import Image
from io import BytesIO
from ollama import Client

# 📌 Tesseract path (update as per your installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 🤖 Ollama client (ensure Mistral is running)
client = Client(host='http://localhost:11434')

# 📤 OCR Function
def ocr_local_image(image):
    try:
        text = pytesseract.image_to_string(image)
        return text.strip() if text.strip() else "⚠️ No text detected. Try a clearer image."
    except Exception as e:
        return f"❌ Local OCR Error: {e}"

# 🧠 Ask Mistral via Ollama
def ask_local_llm(prompt):
    try:
        response = client.chat(
            model='mistral',
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"❌ LLM Error: {e}"

# 🚀 Page Config (Mobile-Friendly)
st.set_page_config(
    page_title="Classroom Helper",
    page_icon="📚",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>📚 Classroom Helper</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI Teaching Assistant – Optimized for Mobile</p>", unsafe_allow_html=True)

# 📸 Upload Section
uploaded_file = st.file_uploader("Upload a photo of your lesson notes", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Notes", use_container_width=True)

    st.info("🔍 Extracting text from image using offline OCR...")
    extracted_text = ocr_local_image(image)

    st.subheader("📝 Extracted Text")
    st.text_area("Text", extracted_text, height=200)

    # 👇 Task Selection for AI
    task = st.selectbox("What would you like the assistant to do?", [
        "Summary Only",
        "Summary + Quiz",
        "Full (Summary + Quiz + Activities)"
    ])

    if extracted_text and len(extracted_text.strip()) > 20:
        trimmed_text = ' '.join(extracted_text.split()[:200])  # speed boost

        if task == "Summary Only":
            full_prompt = f"""Summarize the following classroom notes in under 150 words. Be concise and highlight key points.\n\nContent:\n{trimmed_text}"""

        elif task == "Summary + Quiz":
            full_prompt = f"""Given the following classroom lesson content:\n\n1. Generate a short summary (max 150 words).\n2. Create 3 quiz questions with answers.\n\nContent:\n{trimmed_text}"""

        elif task == "Full (Summary + Quiz + Activities)":
            full_prompt = f"""You're a teaching assistant AI. Based on the following classroom content:\n\n1. Generate a short summary (max 150 words).\n2. Create 3 quiz questions with answers.\n3. Suggest 2 engaging classroom activity ideas.\n\nContent:\n{trimmed_text}"""

        st.info(f"🤖 Generating {task.lower()} using Mistral...")

        with st.spinner("✨ Thinking..."):
            output = ask_local_llm(full_prompt)

        st.subheader("🎓 AI-Generated Teaching Material")
        st.markdown(output)

        st.download_button("📥 Download Result", output, file_name="teaching_material.txt")

