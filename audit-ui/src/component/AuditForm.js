import React, { useState } from "react";

function AuditForm({ onBack }) {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const submitAudit = async () => {
    setLoading(true);
    try {
      const res = await fetch(
        "/audit",
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
    <div className="audit-card" style={{ padding: "20px" }}>
      <div style={{ marginBottom: "12px" }}>
        <button onClick={onBack} style={{ marginRight: "10px" }}>
          ◀ Back
        </button>
        <button onClick={submitAudit} disabled={loading}>
          {loading ? "Running..." : "Run Audit"}
        </button>
      </div>

      {response && (
        <div className="response" style={{ marginTop: "20px" }}>
          <h3>Result</h3>

          {response.error && (
            <div style={{ color: "#b00020", marginBottom: "8px" }}>{response.error}</div>
          )}

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap" }}>
            <div style={{ flex: 1 }}>
              <h4>Issues</h4>
              {response.issues && response.issues.length ? (
                <ul>
                  {response.issues.map((i, idx) => (
                    <li key={idx}>{i}</li>
                  ))}
                </ul>
              ) : (
                <div>No issues found</div>
              )}
            </div>

            <div style={{ flex: 1 }}>
              <h4>AI Comments {response.ai_enabled === false && <small style={{ color: '#666' }}>(AI disabled)</small>}</h4>
              {response.ai_comments && response.ai_comments.length ? (
                <ol>
                  {response.ai_comments.map((c, idx) => (
                    <li key={idx} style={{ marginBottom: 8 }}>{c}</li>
                  ))}
                </ol>
              ) : (
                <div style={{ color: '#666' }}>{response.ai_enabled === false ? 'AI is disabled. Enable OPENAI_API_KEY and set USE_AI=true to get AI comments.' : 'No AI comments'}</div>
              )}

              <div style={{ marginTop: 12 }}>
                <strong>Anomaly:</strong> {response.anomaly_detected ? '⚠️ Suspicious' : 'No'}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default AuditForm;
