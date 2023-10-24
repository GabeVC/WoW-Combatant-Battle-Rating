import React, { useState, useEffect } from 'react';
import { useParams, Link} from 'react-router-dom';
import axios from 'axios';
import './styles.css';

function ResultsPage() {
  const { code } = useParams();
  const [data, setData] = useState(null);
  const [formattedData, setFormattedData] = useState({});
  const [selectedFight, setSelectedFight] = useState([]);
  const [selectedFightData, setSelectedFightData] = useState([]);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [loadingStates, setLoadingStates] = useState({}); // New state for loading
  const [expandedPlayer, setExpandedPlayer] = useState([]);
  const [searchCode, setSearchCode] = useState('');
  const handleSearchCodeChange = (event) => {
    setSearchCode(event.target.value);
  };
  const [noDataFound, setNoDataFound] = useState(false); // State for no data found message

  useEffect(() => {
    axios
      .post('http://194.163.44.136:8000/process_data', { reportCode: code })
      .then((response) => {
        console.log(response.data);
        if (response.data.error === "'NoneType' object has no attribute 'get'") {
          setNoDataFound(true);
        } else {
          setData(response.data);
          formatData(response.data.temp);
          setNoDataFound(false);
        }
      })
      .catch((error) => {
        console.error(error);
        if (error.response && error.response.data && error.response.data.error === "'NoneType' object has no attribute 'get'") {
          setNoDataFound(true);
        }
      });
  }, [code]);

  const formatData = (tempData) => {
    if (!Array.isArray(tempData)) {
      console.error("Invalid tempData format");
      return;
    }

    const formatted = {};
    tempData.forEach(([fightCode, stats]) => {
      formatted[fightCode] = stats;
    });
    setFormattedData(formatted);
  };

  const handleFightClick = async (fightCode, fightTitle) => {
    try {
      setSelectedFightData([])
      setLoadingStates((prevStates) => ({ ...prevStates, [fightCode]: true }));
      setSelectedFight(fightCode);

      const response = await axios.post('http://194.163.44.136:8000/process_data', {
        reportCode: code,
        id: fightCode,
        title: fightTitle,
        action: "BRUNT"
      });

      const responseData = response.data
      console.log(responseData)
      const players = response.data;
      console.log('Response Data:', players);
      setSelectedFightData(players);
      setSelectedFight(fightCode);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoadingStates((prevStates) => ({ ...prevStates, [fightCode]: false }));
      setDropdownOpen(false);
    }
  };


  
  return (
    <div>
      <head>
        <title>WoWCBR | ResultsPage</title>
        <link rel="icon" type="image/png" href="/public/wowcbr.png" />
      </head>
      <nav className="navbar">
        <Link to="/" className="navbar-title">
          WoW<span className="orange-text">CBR</span>
        </Link>
        <div className="navbar-links">
        <Link to="/about" className="navbar-link">About</Link>
        </div>
      </nav>
      
      <h1>Results</h1>
      
      {noDataFound ? (
        <p>There is no data for this report, please make sure the report is valid and public.</p>
      ) : (
        Object.keys(formattedData).map((fightCode) => (
          <div key={fightCode} className="fight-container">
            <button
              className={`button-style ${selectedFight === fightCode ? 'selected' : ''}`}
              onClick={() => handleFightClick(fightCode, formattedData[fightCode][1])}
              disabled={loadingStates[fightCode]}
            >
              <div className="box-style">
                <h2>{formattedData[fightCode][1]}</h2>
                {formattedData[fightCode][2] ? (
                  <p>KILL</p>
                ) : (
                  <p>WIPE
                    <h3>
                      {formattedData[fightCode][3]}%
                    </h3>
                  </p>
                )}
                
                <div className="progress-bar-container">
                  <div
                    className={`health-bar ${
                      formattedData[fightCode][2]
                        ? 'health-bar-color-killed'
                        : `health-bar-color-${getProgressBarColor(formattedData[fightCode][3])}`
                    }`}
                    style={{
                      width: `${100 - formattedData[fightCode][3]}%`,
                    }}
                  ></div>
                </div>
              </div>
            </button>
            {selectedFight === fightCode && (
              <div className="selected-fight-content">
                <h3>Selected Fight Data</h3>
                <p>Click for more info</p>
                {selectedFightData ? (
                  selectedFightData.map((player) => (
                    <div key={player.id}>
                      <div
                        className={`player-box ${player.expanded ? 'expanded' : ''}`}
                        onClick={() => {
                          const updatedData = selectedFightData.map((p) =>
                            p.id === player.id ? { ...p, expanded: !p.expanded } : p
                          );
                          setSelectedFightData(updatedData);
                        }}
                      >
                        <p>
                          {player.name} scored {player.score} points
                        </p>
                      </div>
                      {player.expanded && (
                        <div className="player-dropdown">
                          {player.dpoints > 0 ? (
                            <p>
                              {player.name} lost {player.dpoints} points from avoidable damage
                            </p>
                          ) : (
                            <p>{player.name} took an insignifcant amount of avoidable damage</p>
                          )}
                          {player.gpoints > 0 ? (
                            <p>
                              {player.name} gained {player.gpoints} from bonus activities
                            </p>
                          ) : (
                            <p>
                              {player.name} did not participate in any bonus actions
                            </p>
                          )}
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  loadingStates[fightCode] ? (
                    <p>Loading player info...</p>
                  ) : null
                )}
              </div>
            )}
          </div>
        ))
      )}
      
      {selectedFight && <p>Selected Fight ID: {selectedFight}</p>}
    </div>
  );
}


const getProgressBarColor = (healthPercentage) => {
  if (healthPercentage < 1) {
    return 'pink';
  } else if (healthPercentage < 5) {
    return 'orange';
  } else if (healthPercentage < 25) {
    return 'purple';
  } else if (healthPercentage < 50) {
    return 'blue';
  } else if (healthPercentage < 75) {
    return 'green';
  } else {
    return 'grey';
  }
};


export default ResultsPage;
