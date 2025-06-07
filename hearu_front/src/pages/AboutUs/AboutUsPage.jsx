import { useNavigate } from "react-router-dom";
import styles from './AboutUsPage.module.css';

function AboutUsPage() {
  console.log('AboutUsPage rendered');
  const navigate = useNavigate();

  return(
    <div className={styles.container}>

      <div className = {styles.logoContainer}>
        <img src='images/logo.png' alt="logo" className = {styles.logo} />
      </div>
      
      <div className={styles.pageContent}>

        <div className={styles.aboutUsCard}>

          <p className={styles.aboutUsTextHeading}>
            About
          </p>
          <p className={styles.aboutText}>
            As an AI-powered platform that listens not just to what you say - but how you say it, 
            hearU is a space where emotions are seen and heard.
          </p>

          <p className={styles.aboutText}>
          Using audio file, hearU analyzes speech tone, pace, emotion, and expression. 
          It helps users uncover their emotional patterns and visualizes them through transcripts, word clouds, scores. 
          Meanwhile, gentle and personalized insights are provided.
          </p>

        </div>

        <div className={styles.aboutUsCard2}>
          <p className={styles.aboutUsTextHeading}>
            Human-Centered Product
          </p>

          <p className={styles.hcHeading}>Sense Like A Human</p>
          <p className={styles.hcText}>Not just what you say, but how you say.</p>
          <p className={styles.hcHeading}>Empathy Goes Both Ways</p>
          <p className={styles.hcText}>Bridging the emotional gap between listeners and speakers.</p>
          <p className={styles.hcHeading}>Listen to Every Voice</p>
          <p className={styles.hcText}>Built for all voices. Don't need perfect words to be understood.</p>
          <p className={styles.hcHeading}>Privacy, Trust and Ethical AI</p>
          <p className={styles.hcText}>Prioritizing user consent and data protection.</p>
        </div>

        <div className={styles.aboutUsCard3}>
          
          <p className={styles.aboutUsTextHeading}>
            The Team
          </p>

          <p className={styles.teamName}>Aoi Minamoto</p>
          <p className={styles.teamRole}>Data Scientist</p>
          <p className={styles.teamEmail}>startasleader@gmail.com</p>

          <p className={styles.teamName}>Yufei Song</p>
          <p className={styles.teamRole}>Designer & Developer</p>
          <p className={styles.teamEmail}>yufeison@andrew.cmu.edu</p>

        </div>

      </div>

      <button className = {styles.backButton} onClick={() => navigate(-1)}> - Back to home page - </button>

    </div>
  )


}
export default AboutUsPage;