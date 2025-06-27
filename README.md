hearU is a voice-based emotional insight tool that analyzes both the content and expression of your speech. It generates empathetic feedback and language-based metrics — helping users understand how they sound, not just what they say.

---

Features

Audio Upload: Record or upload your voice directly from the browser
Multi-layered Analysis:
  - Basic: total words, sentence length, speech rate
  - Expression: lexical diversity, repetition, sentence complexity
  - Emotion: polarity, subjectivity, disfluency, modeled emotion
AI Feedback: Gemini-powered summaries and supportive messages
Exportable Results: Download analysis as a JSON file

---

Tech Stack

Frontend
- React + Vite
- CSS Modules

Backend
- FastAPI
- pydub, SpeechRecognition, TextBlob, WordCloud
- Google Gemini API for emotion modeling & summaries

No database is used. All processing happens in-memory.

---

Getting Started (Local Setup)

1. Clone the repository
git clone https://github.com/yufeisong0914/hearU.git
cd hearU

2. Start Backend
cd hearu_back_fastapi
pip install -r requirements.txt
uvicorn app.main:app --reload

3. Start Frontend
cd ../hearu_front
npm install
npm run dev

---

Project Structure

hearu/
├── hearu_front/       # React + Vite frontend
├── hearu_back_fastapi/  # FastAPI backend

---

Design Philosophy

- Human-centered design
- Empathy over classification

---

Acknowledgments

Google Gemini 1.5 API for LLM-powered summarization
