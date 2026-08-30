# Enterprise AI Chatbot 🤖

> An intelligent, multi-LLM workspace assistant designed to query internal company protocols, streamline HR operations, and act as a unified knowledge base.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=flat&logo=google&logoColor=white)

## 🌟 Overview

This GenAI Assistant is built on a robust Django backend architecture. It allows enterprise employees to interact seamlessly with advanced Large Language Models (including OpenAI, Google Gemini, and Grok) to retrieve accurate organizational data, policy explanations, and operational insights in real-time.

## ✨ Key Features

- **Multi-LLM Integration:** Easily toggle and query between OpenAI, Gemini, and Grok depending on the complexity of the task.
- **Dynamic FAQ Engine:** Automatically parses and incorporates sample company FAQs for context-aware responses.
- **Secure Backend:** Powered by Django with a lightweight SQLite database for rapid prototyping and local chat logging.
- **Environment Management:** Highly secure, `.env` driven configuration for managing API keys and service accounts.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **APIs:** OpenAI API, Google Generative AI API
- **Database:** SQLite3

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Django 5.x
- API Keys for OpenAI and Gemini

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Satyam3se/GenAI_Chatbot.git
   cd GenAI_Chatbot
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install required packages:**
   ```bash
   pip install django openai google-generativeai python-dotenv
   ```

4. **Environment Configuration:**
   Create a `.env` file in the root directory and add your API credentials:
   ```ini
   OPENAI_API_KEY=your_openai_key
   GEMINI_API_KEY=your_gemini_key
   ```

5. **Run Migrations & Start Server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
   Navigate to `http://127.0.0.1:8000/` in your browser.

## 👨‍💻 Developer
**Satyam Kumar Raj**
- [Portfolio](https://satyam3se.github.io/Portfolio/)
- [LinkedIn](https://www.linkedin.com/in/satyam-kumar-a72baa345/)
- [GitHub](https://github.com/Satyam3se)
