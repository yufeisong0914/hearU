import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './SignupPage.module.css';

function SignupPage() {
    console.log('SignupPage rendered');
    const navigate = useNavigate();

    const [email, setEmail] = useState('');


    const handleSignup = (e) => {
        // prevent the default form submission behavior
        e.preventDefault();

        // save the email to localStorage
        localStorage.setItem("hearuEmail", email);

        // successfully signed up, navigate to the main page
        navigate('/main');
    };

    return (

        <div className = {styles.container}>
            
            <div className = {styles.logoContainer}>
                <img src='images/logo.png' alt="logo" className = {styles.logo} />
            </div>

            <div className = {styles.signupCard}>
                <h1 className = {styles.signupTitle}> Hello! </h1>
                <p className={styles.signupWord}>Sign up to get started ❤️</p>

                <form onSubmit = {handleSignup} className = {styles.signupForm}>
                    <input
                        type = "email"
                        value={email}
                        placeholder = "Email"
                        className = {styles.input}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    
                    <input
                        type = "password"
                        placeholder = "Password"
                        className = {styles.input}
                        required
                    />
                
                    <button type = "submit" className = {styles.signup_signupButton} > ✧ Sign up ✧ </button>
                    <button type = "button" className = {styles.signup_loginButton} onClick={() => navigate('/login')}>Already have an account? Click to log in</button>
                    
                </form> 
            </div>

            <p className = {styles.aboutLink} onClick={() => navigate('/aboutus')}> - About Us - </p>
        
        </div>
    );
}

export default SignupPage;