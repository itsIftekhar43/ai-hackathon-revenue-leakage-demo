import React, { useState } from "react";

function AuditForm() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const submitAudit = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        "https://animated-space-adventure-jxp4rpjq9g9hq5v6-8000.app.github.dev/audit",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            fare: 5000,
            tax: -20,
            commission: 6000,
            refund_amount: 4500,
          }),
        }
      );

      if (!res.ok) throw new Error(`Server error: ${res.status}`);
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      setResponse({ error: error.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Audit Engine Demo</h2>
      <button onClick={submitAudit} disabled={loading}>
        {loading ? "Running..." : "Run Audit"}
      </button>

      {response && (
        <pre style={{ marginTop: "20px" }}>
          {JSON.stringify(response, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default AuditForm;
