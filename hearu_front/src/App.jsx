import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/Login/LoginPage';
import SignupPage from './pages/Signup/SignupPage';
import MainPage from './pages/Main/MainPage';
import AboutUsPage from './pages/AboutUs/AboutUsPage';

function App() {
  console.log('App rendered');
  return (
    <Router>
      <Routes>
        <Route path="/" element={<SignupPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path = "/login" element={<LoginPage />} />
        <Route path = "/main" element={<MainPage />} />
        <Route path = "/aboutus" element={<AboutUsPage />} />
      </Routes>
    </Router>
  );
}

export default App;
