import { useNavigate } from 'react-router-dom';
import styles from './MainPage.module.css';
import React, { useState, useEffect } from 'react';


function MainPage() {

  console.log('MainPage rendered');
  const navigate = useNavigate();

  const [showLogoutConfirm, setShowLogoutConfirm] = useState(false);
  const [showPrivacyModal, setShowPrivacyModal] = useState(false);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [fileName, setFileName] = useState("");


  const email = localStorage.getItem("hearuEmail");

  console.log("📦 Analysis data: ", data);

  const handleAnalyze = async () => {
    if (!email) {
    alert("⚠️ Please sign up or log in again.");
    return;
    } else if (!file) {
    alert("⚠️ Please upload an audio file before analyzing.");
    return;
    } else {
      alert("✅ Start analyzing...");
    }


  const formData = new FormData();
  formData.append("email", email);
  formData.append("file", file);

  setLoading(true);

  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
      credentials: "include"
    });

    if (!response.ok) {
      const errorResult = await response.json();
      console.error("Backend returned error:", errorResult);
      alert("❌ Upload failed: " + (errorResult?.error || "Unknown error."));
      return;
    }

    const result = await response.json();
    console.log("Analysis result: ", result);
    setData(result); 
    alert("✅ Analysis complete! You can check the result now.");

  } catch (err) {
    console.error("Upload failed:", err);
    alert("❌ Upload failed, please try again.");
  }

}

const handleExport = () => {
  if (!data) {
    alert("⚠️ No data to export.");
    return;
  }

  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const link = document.createElement('a');
  link.href = url;
  link.download = `hearu_analysis_${new Date().toISOString()}.json`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  alert("✅ Successfully downloaded!");
  
};


  return (

    <div className={styles.container}>

      <header className={styles.topBar}>
        <img src='images/logo.png' alt="logo" className = {styles.logo} />

        <div className={styles.emailContainer}
          onClick={() => setShowLogoutConfirm(true)}
          title="Click to log out"
          style={{ cursor: 'pointer' }}>
          
          <img src="/images/avatar.png" alt="avatar" className={styles.avatarIcon} />

          <span className={styles.emailText}>
            {localStorage.getItem("hearuEmail") || "guest@example.com"}
          </span>

        </div>

      </header>

      <div className={styles.mainBox}>
        <div className={styles.buttonBar}>

          {fileName && (
              <span className={styles.fileNameText}>🎧 Current file: {fileName}</span>
            )}

          <div className={styles.buttonContainer}>
          
            
            <button className={styles.uploadButton} onClick={() => document.getElementById("fileInput").click()} >📂 Upload </button>
            <input
            type="file"
            accept="audio/*"
            style={{ display: 'none' }}
            id="fileInput"
            onChange={(e) => {
              const uploadedFile = e.target.files[0];
              if (uploadedFile) {
                console.log("📁 Selected file:", uploadedFile);
                setFile(uploadedFile);
                setFileName(uploadedFile.name);
                alert("✅ File uploaded. Now click 🧠 Analyze to analyze.");
              }
            }}
            />

            <button className={styles.analyzeButton} onClick={handleAnalyze}> 🧠 Analyze </button>

            <button className={styles.exportButton} onClick={handleExport}>📝 Export</button>

          </div>

          <p
            className={styles.privacy}
            onClick={() => setShowPrivacyModal(true)}
            style={{ cursor: 'pointer' }}
          >
            🔒 How is my data protected?
          </p>

          {showPrivacyModal && (
            <div className={styles.modalOverlay}>
              <div className={styles.modalContent2}>
                <p>
                  At hearU, your audio and analysis data are securely transmitted and stored.
                  We do not share your data with third parties.
                  All information is deleted after analysis unless you choose to export and save to your local device. <br/>
                </p>

                <div className={styles.modalButtons}>
                  <button onClick={() => setShowPrivacyModal(false)}>Close</button>
                </div>
              </div>
            </div>
          )}

          {showLogoutConfirm && (
            <div className={styles.modalOverlay}>
              <div className={styles.modalContent}>
                <p>Are you sure you want to log out? </p>
                
                <div className={styles.modalButtons}>
                  <button onClick={() => navigate('/login')}>Yes</button>
                  <button onClick={() => setShowLogoutConfirm(false)}>Cancel</button>
                </div>
              </div>
            </div>
          )}

        </div>

        <div className={styles.progressBar}></div>

        <div className={styles.box1}>
          <section className={styles.transcriptCard}>
            <h2 className={styles.title}>Transcript</h2>
            <div className={styles.transcriptScroll}>
              <p className={styles.transcriptContent}>
                {data?.transcribed_text || "Transcript not available."}
              </p>
            </div>
          </section>

          <section className={styles.analysisCard}>
            <h2 className={styles.title}>Analysis</h2>
            <div className={styles.analysisContainer}>
              <div className={styles.analysisContainer1}>
                <p className={styles.analysisModule}>💬 Basic</p>
                <p className={styles.analysisContent}>Timestamp: {data?.timestamp ? data.timestamp.split('.')[0].replace('T', ' ') : ''}</p>
                <p className={styles.analysisContent}>Total time: {data?.total_time}s</p>
                <p className={styles.analysisContent}>Total words: {data?.total_words}</p>
                <p className={styles.analysisContent}>Avg sentence length: {data?.avg_sentence_length}</p>
              </div>
              <div className={styles.analysisContainer2}>
                <p className={styles.analysisModule}>🗣️ Expression</p>
                <p className={styles.analysisContent}>Diversity score: {data?.diversity_score}</p>
                <p className={styles.analysisContent}>Lexical pattern: {data?.lexical_pattern}</p>
                <p className={styles.analysisContent}>Complexity feedback: {data?.complexity_feedback}</p>
                <p className={styles.analysisContent}>Conjunctions: {data?.conjunction_count}</p>
                <p className={styles.analysisContent}>Unique words: {data?.unique_words}</p>
              </div>
              <div className={styles.analysisContainer3}>
                <p className={styles.analysisModule}>🫧 Emotion</p>
                <p className={styles.analysisContent}>Speech rate: {data?.speech_rate}w/s</p>
                <p className={styles.analysisContent}>Polarity: {data?.polarity}</p>
                <p className={styles.analysisContent}>Subjectivity: {data?.subjectivity}</p>
                <p className={styles.analysisContent}>Disfluencies: {data?.disfluencies}</p>
                <p className={styles.analysisContent}>Emotion modeling: {data?.emotions}</p>
              </div>
            </div>
          </section>

          <section className={styles.aiCard}>
            <h2 className={styles.title}>AI HearU</h2>
            <div className={styles.aiScroll}>
              {data?.ai_feedback ? (
                data.ai_feedback.error ? (
                  <p className={styles.aiContent}>{data.ai_feedback.error}</p>
                ) : (
                  <div className={styles.aiContent}>
                    <p><b>Summary:</b> {data.ai_feedback.summary}</p>
                    {/* <p><b>Detected Emotions:</b> 
                      {data.ai_feedback.detected_emotions?.map((emotion, index) => (
                        <span key={index} className={styles.emotionTag}>{emotion}</span>
                      ))}
                    </p> */}
                    <p><b>Supportive Message:</b><br/> {data.ai_feedback.supportive_message}</p>
                  </div>
                )
              ) : (
                <p className={styles.aiContent}>Analyzing with AI...</p>
              )}
            </div>
          </section>

        </div>

      </div>
      
    </div>
  )
}

export default MainPage;