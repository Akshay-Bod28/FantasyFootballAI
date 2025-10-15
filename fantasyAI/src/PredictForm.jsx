import React, { useState } from "react";
import "./PredictForm.css";

function PredictForm() {
  const [playerName, setPlayerName] = useState("");
  const [position, setPosition] = useState("WR");
  const [year, setYear] = useState(new Date().getFullYear());
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const body = { player_name: playerName };

    try {
      const response = await fetch(
        `/api/predict?position=${position}&year=${year}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ error: error.message });
    }
  };

  return (
    <div className="container">
      <h1>Fantasy Player Predictor</h1>
      <form onSubmit={handleSubmit} className="form">
        <label>
          Player Name:
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            required
          />
        </label>

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

        <label>
          Year:
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            required
          />
        </label>

        <button type="submit">Predict</button>
      </form>

      {result && (
        <div className="result">
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <>
              <h2>{result.player}</h2>
              <p>
                Probability Top 10:{" "}
                <span className="prob">
                  {(result.probability_top_10 * 100).toFixed(2)}%
                </span>
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default PredictForm;
