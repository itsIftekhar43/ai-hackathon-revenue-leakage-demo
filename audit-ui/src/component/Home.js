import React from "react";
import "./Home.css";

function Home({ onStart }) {
  return (
    <div className="home-container">
      <div className="home-card">
        <h1>Welcome to the AI Audit Engine</h1>
        <p>
          Quickly run audits on transactions and get AI-assisted explanations.
          This demo helps surface potential revenue leakage and rule violations.
        </p>
        <button className="start-btn" onClick={onStart}>
          Start Audit
        </button>
      </div>
    </div>
  );
}

export default Home;
