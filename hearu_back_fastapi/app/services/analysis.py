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
import json
import requests
# ai
from transformers import pipeline

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyC8cubLmcGsqqXikEaNv8OBLX77djNQAGA"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

recognizer = sr.Recognizer()

def call_gemini_api(prompt, max_tokens=150):
    """Make a request to Gemini API"""
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Unable to generate response"
            
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return f"Error: {str(e)}"
    except KeyError as e:
        print(f"Unexpected response format: {e}")
        return "Error: Unexpected response format"

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

def generate_summary(text):
    """Generate summary using Gemini API"""
    short_text = text[:1000]  # Limit text length for API efficiency
    prompt = f"""Summarize the speaker's current problem and situation. Explain logically what happened and how they are feeling. Show that you understand the speaker, and they are seen, heard and recognized.

Text to analyze: "{short_text}"

Provide a compassionate and understanding summary in 2-3 sentences."""
    
    return call_gemini_api(prompt, max_tokens=150)

def generate_support(text):
    """Generate supportive response using Gemini API"""
    short_text = text[:1000]  # Limit text length for API efficiency
    prompt = f"""Give caring, empathetic and practical support to guide someone responding to this person's situation. Be supportive and constructive.

Text to analyze: "{short_text}"

Provide helpful and empathetic guidance in 2-3 sentences."""
    
    return call_gemini_api(prompt, max_tokens=100)

def get_emotion_analysis(text):
    """Analyze emotions using Gemini API"""
    prompt = f"""Analyze the emotions expressed in this text. Identify the top 3-5 emotions present and rate their intensity.

Text: "{text[:500]}"

Respond in JSON format like this:
{{"emotions": [{{"emotion": "sadness", "intensity": "high"}}, {{"emotion": "frustration", "intensity": "medium"}}]}}"""
    
    response = call_gemini_api(prompt, max_tokens=100)
    
    try:
        # Try to parse JSON response
        emotion_data = json.loads(response)
        return [e['emotion'].lower() for e in emotion_data.get('emotions', [])]
    except:
        # Fallback: extract emotions from text response
        common_emotions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust', 'neutral']
        detected_emotions = []
        response_lower = response.lower()
        
        for emotion in common_emotions:
            if emotion in response_lower:
                detected_emotions.append(emotion)
        
        return detected_emotions[:3] if detected_emotions else ['neutral']
    
def get_ai_analysis(text):
    """Get comprehensive AI analysis"""
    try:
        summary = generate_summary(text)
        support = generate_support(text)
        return {
            "summary": summary,
            "supportive_message": support
        }
    except Exception as e:
        return {
            "summary": f"⚠️ Summary generation failed: {str(e)}",
            "supportive_message": f"⚠️ Support generation failed: {str(e)}"
        }
      

async def analyze_audio(file, email):
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f_out:
        f_out.write(await file.read())

    audio = AudioSegment.from_file(temp_path)
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
    
    # emotions using Gemini
    emotion_analysis = get_emotion_analysis(text) if text and "Could not understand" not in text else ['neutral']

    # AI analysis using Gemini
    ai_feedback = {}
    if text and "Could not understand" not in text:
        ai_feedback = get_ai_analysis(text)
    else:
        ai_feedback = {
            "summary": "Unable to analyze due to transcription issues",
            "supportive_message": "Please try recording again with clearer audio"
        }


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
        "emotions": emotion_analysis,
        
        "ai_feedback": ai_feedback
    }

    # clear the temporary files
    os.remove(temp_path)
    os.remove("temp.wav")

    return result
