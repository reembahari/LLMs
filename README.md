# Flask PDF Information Extractor

This Flask web application allows users to upload PDF files, extract text content, and retrieve specific information using the OpenAI API (GPT-3.5-turbo or GPT-4).

## Features

- Upload and process PDF files to extract text using PyMuPDF (`fitz`).
- Extracts specific information from the text using the OpenAI API.
- Provides output as a structured JSON object with keys like "Paper Title," "Abstract," "Author Names," "Author Emails," and "Summary of the Conclusion."

## Requirements

- Python 3.6+
- Flask
- PyMuPDF (`fitz`)
- Requests library
- OpenAI API key
- `python-dotenv` for managing environment variables

## Installation
Create a virtual environment:python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
Set up environment variables:OPENAI_API_KEY=your_openai_api_key
Run the Flask app:python app.py







