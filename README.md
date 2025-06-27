hearU is a voice-based emotional insight tool that analyzes both the content and expression of your speech. It generates empathetic feedback and language-based metrics — helping users understand how they sound, not just what they say.

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

Acknowledgments

Google Gemini 1.5 API for LLM-powered summarization
