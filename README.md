# AI Study Buddy

AI Study Buddy is an AI-powered personal learning assistant built with Python and Streamlit. The application helps students study more effectively by providing AI-based explanations, question answering, summaries, quizzes, flashcards, personalized study plans, weak concept detection, progress tracking, and study reports.

The application supports Google Gemini Cloud AI for deployment and Ollama with Llama 3.2 for local development.

## Project Overview

AI Study Buddy combines Natural Language Processing, Machine Learning, and Large Language Model technologies to provide an interactive learning environment.

Students can upload study materials in PDF, TXT, or DOCX format and use the content to interact with the AI assistant.

The system analyzes quiz performance and identifies concepts that require additional practice. It also provides personalized recommendations based on learning performance.

## Key Features

### Study Material Management

* Upload PDF, TXT, and DOCX files
* Enter or edit study material manually
* Display word, character, and line statistics
* Clear study material when required

### AI Chat

* Ask questions based on uploaded study material
* Provides contextual answers using the student's notes
* Maintains previous questions during the session

### Concept Explainer

* Explain difficult concepts using AI
* Supports beginner, intermediate, and advanced explanation levels
* Provides examples, important points, and memory tips

### Smart Summary

* Generate AI-powered summaries
* Supports bullet-point and paragraph summaries
* Provides an additional TF-IDF extractive summarization method

### AI Quiz

* Generate multiple-choice questions from study material
* Supports configurable number of questions
* Automatically evaluates answers
* Displays correct answers and explanations
* Identifies concepts associated with incorrect answers
* Stores quiz performance

### AI Flashcards

* Generate revision flashcards from study material
* Organizes cards by concept
* Allows flashcards to be downloaded as a text file

### Weak Concept Detection

* Analyzes incorrect quiz answers
* Identifies frequently missed concepts
* Categorizes concepts according to practice priority

### Personalized Study Plan

* Uses weak concepts and available study hours
* Generates an AI-based study plan
* Provides revision and practice recommendations

### Progress Tracking

* Tracks quiz attempts
* Calculates latest, average, and best scores
* Tracks study time
* Displays quiz score history
* Calculates learning streaks and improvement

### Study Timer

* Records study session duration
* Tracks total study time

### Bookmarks

* Save important topics for later revision
* Remove topics when they are no longer required

### Study Report

* Generates a PDF report of learning performance
* Includes quiz scores, weak concepts, bookmarks, and study sessions
* Provides a downloadable study report

## AI Technologies

The project uses multiple AI and NLP techniques:

* Large Language Models
* Google Gemini Cloud AI
* Ollama Local AI
* Llama 3.2
* Natural Language Processing
* TF-IDF
* Cosine Similarity
* Text Summarization
* AI-based Question Generation
* AI-based Flashcard Generation
* Performance Analysis
* Personalized Recommendations

## AI Architecture

The application uses a dual AI architecture.

```text
                    AI Study Buddy
                          |
                          v
                   Streamlit Application
                          |
                          v
                     AI Engine
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Gemini Cloud AI          Ollama Local AI
              |                       |
              v                       v
     Google Gemini API          Llama 3.2 3B
              |
              v
       Cloud Deployment
```

When a Gemini API key is available, the application uses Google Gemini Cloud AI.

When a Gemini API key is not available, the application falls back to Ollama Local AI.

## Technology Stack

### Frontend and Application

* Python
* Streamlit

### Artificial Intelligence

* Google Gemini API
* Ollama
* Llama 3.2

### Machine Learning and NLP

* Scikit-learn
* TF-IDF
* Cosine Similarity

### Document Processing

* PyPDF2
* python-docx

### Data Processing

* Pandas

### Report Generation

* ReportLab

### API Communication

* Google GenAI
* Requests

## Project Structure

```text
AI-Study-Buddy/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
└── modules/
    ├── ai_engine.py
    ├── document_processor.py
    ├── summarizer.py
    ├── progress_tracker.py
    ├── study_planner.py
    └── report_generator.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/dineshkumar-user/AI-Study-Buddy.git
```

Navigate to the project directory:

```bash
cd AI-Study-Buddy
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```powershell
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running Locally

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at the local Streamlit address.

## Local AI with Ollama

For local AI usage, install Ollama and make sure the required model is available:

```bash
ollama pull llama3.2:3b
```

Start Ollama and run the application:

```bash
streamlit run app.py
```

The application can then communicate with the local Ollama server.

## Cloud AI Configuration

For cloud deployment, the application uses Google Gemini API.

Create a Gemini API key and configure it as an environment variable during local testing:

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

For Streamlit Cloud deployment, add the API key through the application's Secrets configuration.

Use:

```toml
GEMINI_API_KEY = "YOUR_API_KEY"
```

Do not add the API key directly to the source code or commit it to GitHub.

## Cloud Deployment

The application can be deployed using Streamlit Community Cloud.

Deployment configuration:

```text
Repository: dineshkumar-user/AI-Study-Buddy
Branch: main
Main file: app.py
```

After deployment, configure the `GEMINI_API_KEY` through Streamlit Cloud Secrets.

The deployed application uses Gemini Cloud AI instead of relying on a locally running Ollama server.

## Requirements

The project dependencies are listed in `requirements.txt`.

```text
streamlit
pandas
scikit-learn
PyPDF2
python-docx
reportlab
ollama
google-genai
requests
```

## Data and Privacy

Study material uploaded to the application is processed by the application features and, when Gemini Cloud AI is being used, relevant content may be sent to the configured AI service to generate responses.

Users should avoid uploading confidential, sensitive, or personally identifiable information.

API keys must be stored securely using environment variables or Streamlit Secrets.

## Future Enhancements

Potential future improvements include:

* User authentication
* Database-based user profiles
* Persistent cloud storage
* Voice-based AI interaction
* More advanced document formats
* Adaptive quiz difficulty
* Automated learning schedules
* More detailed analytics
* Multi-language learning support
* AI-generated practice exercises
* Mobile-friendly improvements

## Project Objective

The primary objective of AI Study Buddy is to provide students with an accessible AI-based learning assistant that combines study material processing, AI interaction, summarization, assessment, performance analysis, and personalized learning recommendations within a single application.

## Author

Dineshkumar S

## License

This project is developed for educational and internship purposes.
