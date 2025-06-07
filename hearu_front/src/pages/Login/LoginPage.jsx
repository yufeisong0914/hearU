import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './LoginPage.module.css';

function LoginPage() {
    console.log('LoginPage rendered');
    const navigate = useNavigate();
    
    const [email, setEmail] = useState('');

    const handleLogin = (e) => {
        // prevent the default form submission behavior
        e.preventDefault();

        // save the email to localStorage
        localStorage.setItem("hearuEmail", email);

        // successfully logged in, navigate to the main page
        navigate('/main');
    };

    return (

        <div className = {styles.container}>

            <div className = {styles.logoContainer}>
                <img src='images/logo.png' alt="logo" className = {styles.logo} />
            </div>

            <div className = {styles.loginCard}>
                <h1 className = {styles.loginTitle}> Welcome back! </h1>
                <p className={styles.loginWord}>Log in your account ⭐️</p>

            <form onSubmit = {handleLogin} className = {styles.loginForm}>
                <input
                    type = "email"
                    value = {email}
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
                
                
                <button type = "submit" className = {styles.login_loginButton}>✧ Log in ✧</button>
                <button type = "button" className = {styles.login_signupButton} onClick={() => navigate('/signup')}>New to hearU? Click to sign up</button>
                
            </form> 
            </div>

            <p className = {styles.aboutLink} onClick={() => navigate('/aboutus')}> - About Us - </p>
        
        </div>
    );
}
            
export default LoginPage; 