import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './styles.css';

function HomePage() {
  const [code, setCode] = useState('');
  const navigate = useNavigate();

  const handleInputChange = (event) => {
    const input = event.target.value;
  
    // Extract the code from a direct input of size 16
    if (input.length === 16) {
      setCode(input);
      return;
    }
  
    // Extract the code from a URL
    const reportIndex = input.indexOf('reports/') + 'reports/'.length;
    const fightIndex = input.indexOf('#fight');
    
    if (reportIndex !== -1 && fightIndex !== -1) {
      const extractedCode = input.substring(reportIndex, fightIndex);
      setCode(extractedCode);
    }
  };

  const handleGoToResults = () => {
    navigate(`/results/${code}`);
  };

  return (
    <div className="home-page-container">
      <h1 className="home-page-title">
        WoW<span className="orange-text">CBR</span>
      </h1>
      <input
        type="text"
        placeholder="Enter link..."
        value={code}
        onChange={handleInputChange}
        className="input-field"
      />
      <button onClick={handleGoToResults} className="submit-button">Go to Results</button>
    </div>
  );
}

export default HomePage;