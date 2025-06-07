import os
import uuid
import base64
import io
from datetime import datetime
from pydub import AudioSegment
from collections import Counter
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import speech_recognition as sr
# ai
from transformers import pipeline

# initialize models
dialogue_model = pipeline("text2text-generation", model="google/flan-t5-large")
support_model = pipeline("text2text-generation", model="google/flan-t5-large")
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=5)

recognizer = sr.Recognizer()

def lexical_diversity(text):
    words = text.lower().split()
    total_words = len(words)
    unique_words = len(set(words))
    score = unique_words / total_words if total_words > 0 else 0
    return score, total_words, unique_words

def sentence_complexity(text):
    sentences = text.split(".")
    words = text.split()
    avg_len = len(words) / len(sentences) if sentences else 0
    conjunctions = ['and', 'but', 'or', 'because', 'although', 'since', 'while', 'if', 'when', 'though']
    conj_count = sum(text.lower().count(c) for c in conjunctions)
    feedback = "✅ Balanced complexity." if avg_len > 12 and conj_count >= len(sentences) else "⚠️ Simple or flat sentence structure."
    return avg_len, conj_count, feedback

# def generate_summary(text):
#     short_text = text[:1000]
#     prompt = f"Summarize the speaker's current problem and situation, explain in logic, what happened and how they are feeling. Show that you understand the speaker, and they are seen, heard and recognized: {short_text}"
#     response = dialogue_model(prompt, max_length=150, do_sample=True)[0]["generated_text"]
#     return response

# def generate_support(text):
#     short_text = text[:1000]
#     prompt = f"Give an caring, empathetic and practical support to guide the listener or the speaker to response to this person's situation: {short_text}"
#     result = support_model(prompt, max_length=100, do_sample=True)[0]['generated_text']
#     return result

def get_emotion_modeling(text):
    emotions = emotion_model(text)
    top_emotions = [e['label'].lower() for e in emotions[0]]

# def get_ai_analysis(text):
#     summary = generate_summary(text)
#     support = generate_support(text)
#     return {
#         "summary": summary,
#         "supportive_message": support
#     }


async def analyze_audio(file, email):
    filename = f"{uuid.uuid4()}.wav"
    file_path = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(16000)
    audio.export("temp.wav", format="wav")

    # total time
    duration_sec = round(len(audio) / 1000, 2)

    # transcript
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)

    # polarity, subjectivity
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    # others
    diversity_score, total_words, unique_words = lexical_diversity(text)
    avg_sentence_length, conjunction_count, complexity_feedback = sentence_complexity(text)
    lexical_pattern = "✅ Diverse vocabulary." if diversity_score > 0.5 else "⚠️ Repeated words or less variety."

    # disfluency words
    disfluency_words = ['um', 'uh', 'like', 'you know']
    disfluency_count = sum(text.lower().split().count(d) for d in disfluency_words)

    # speech rate
    words_per_second = round(total_words / duration_sec, 2) if duration_sec > 0 else 0


    # word cloud
    words = [w.lower() for w in text.split() if w.lower() not in STOPWORDS and len(w) > 1]
    freq = Counter(words).most_common(30)
    wc = WordCloud(width=600, height=400, background_color=None, mode="RGBA")
    wc.generate_from_frequencies(dict(freq))
    buf = io.BytesIO()
    wc.to_image().save(buf, format='PNG')
    wordcloud_base64 = base64.b64encode(buf.getvalue()).decode()

    # emotions
    emotion_modeling = get_emotion_modeling(text)

    # ai
    # ai_feedback = {}
    # try:
    #     ai_feedback = get_ai_analysis(text)
    # except Exception as e:
    #     ai_feedback = {"error": f"⚠️ AI analysis failed: {str(e)}"}


    result = {
        "email": email,
        "audio_file": file.filename,

        "transcribed_text": text,

        "timestamp": datetime.now().isoformat(),
        "total_time": duration_sec,
        "total_words": total_words,

        "unique_words": unique_words,
        "avg_sentence_length": round(avg_sentence_length, 2),
        "conjunction_count": conjunction_count,
        "complexity_feedback": complexity_feedback,
        "diversity_score": round(diversity_score, 2),
        "lexical_pattern": lexical_pattern,

        "speech_rate": words_per_second,
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2),
        "disfluencies": disfluency_count,
        "emotions": emotion_modeling,
        
        # "ai_feedback": ai_feedback
    }

    # clear the temporary files
    os.remove(file_path)
    os.remove("temp.wav")

    return result
