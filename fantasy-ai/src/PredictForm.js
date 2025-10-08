import React, { useState } from "react";

function PredictForm() {
  const [playerName, setPlayerName] = useState("");  // Player input
  const [position, setPosition] = useState("WR");    // Position input
  const [year, setYear] = useState(new Date().getFullYear()); // Year input
  const [result, setResult] = useState(null);       // Store API response

  const handleSubmit = async (e) => {
    e.preventDefault();  // Prevent page reload

    const body = { player_name: playerName };

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/predict?position=${position}&year=${year}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );

      const data = await response.json();
      setResult(data);  // Save API response
    } catch (error) {
      setResult({ error: error.message });
    }
  };

  return (
    <div>
      <h1>Fantasy Player Predictor</h1>

      <form onSubmit={handleSubmit}>
        <label>
          Player Name:
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            required
          />
        </label>
        <br />

        <label>
          Position:
          <select
            value={position}
            onChange={(e) => setPosition(e.target.value)}
          >
            <option value="WR">WR</option>
            <option value="RB">RB</option>
            <option value="QB">QB</option>
            <option value="TE">TE</option>
          </select>
        </label>
        <br />

        <label>
          Year:
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            required
          />
        </label>
        <br />

        <button type="submit">Predict</button>
      </form>

      {result && (
        <div>
          <h2>Result:</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default PredictForm;