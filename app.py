from flask import Flask, request, render_template
import fitz  # PyMuPDF
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                text += page.get_text()
    except fitz.FileDataError:
        return "Error: Invalid PDF file."
    return text

def extract_information(text):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = (
        "Extract the following information from the text below. If a piece of information is not found, return 'N/A'.\n"
        "Provide the output as a JSON object with the following keys:\n"
        "- 'Paper Title'\n"
        "- 'Abstract'\n"
        "- 'Author Names' (as a comma-separated list)\n"
        "- 'Author Emails' (as a comma-separated list)\n"
        "- 'Summary of the Conclusion'\n\n"
        "Example JSON Output:\n"
        "{\n"
        "  \"Paper Title\": \"Example Title\",\n"
        "  \"Abstract\": \"Example Abstract...\",\n"
        "  \"Author Names\": \"John Doe, Jane Smith\",\n"
        "  \"Author Emails\": \"john.doe@example.com, jane.smith@example.com\",\n"
        "  \"Summary of the Conclusion\": \"The study concluded...\"\n"
        "}\n\n"
        f"Text:\n{text}"
    )

    try:
        response = requests.post(api_url, headers=headers, json={
            "model": "gpt-3.5-turbo",  # Or "gpt-4" if you have access
            "messages": [{"role": "user", "content": prompt}]
        })
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        print("Raw OpenAI Response:", response.json()["choices"][0]["message"]["content"])
        extracted_info = json.loads(response.json()["choices"][0]["message"]["content"])
        return extracted_info

    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
        return {"error": f"API Request Error: {e}"}  # Return an error dictionary
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"JSON Parsing Error: {e}")
        return {"error": f"JSON Parsing Error: {e}"}

@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_info = {}
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and file.filename.endswith('.pdf'):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            text = extract_text_from_pdf(file_path)
            if "Error:" in text: #Handle PDF Error
                extracted_info = {"error": text}
            else:
                extracted_info = extract_information(text)
            os.remove(file_path) #Delete file after use
            return render_template('result.html', extracted_info=extracted_info)
    return render_template('index.html', extracted_info=extracted_info)


if __name__ == '__main__':
    app.run(debug=True)