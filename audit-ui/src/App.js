import React, { useState } from "react";
import AuditForm from "./component/AuditForm";
import Home from "./component/Home";
import "./App.css";

function App() {
  const [page, setPage] = useState("home");

  return (
    <div className="App">
      <div className="App-header">
        {page === "home" ? (
          <Home onStart={() => setPage("audit")} />
        ) : (
          <AuditForm onBack={() => setPage("home")} />
        )}
      </div>
    </div>
  );
}

export default App;
