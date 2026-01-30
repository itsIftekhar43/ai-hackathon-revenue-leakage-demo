import React, { useState, useEffect } from "react";

function AuditForm({ onBack }) {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ fare: 5000, tax: -20, commission: 6000, refund_amount: 4500 });
  const [error, setError] = useState(null);
  const [aiEnabled, setAiEnabled] = useState(true);

  useEffect(() => {
    fetch('/health')
      .then((r) => r.json())
      .then((j) => {
        setAiEnabled(Boolean(j.ai_enabled));
        setAiReal(Boolean(j.ai_real));
      })
      .catch(() => {
        setAiEnabled(false);
        setAiReal(false);
      });
  }, []);

  const [aiReal, setAiReal] = useState(true);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((p) => ({ ...p, [name]: value }));
  };

  const submitAudit = async () => {
    setError(null);

    const payload = {};
    for (const key of ["fare", "tax", "commission", "refund_amount"]) {
      const v = Number(form[key]);
      if (Number.isNaN(v)) {
        setError("Please enter valid numeric values for all fields.");
        return;
      }
      payload[key] = v;
    }

    setLoading(true);
    try {
      const res = await fetch(
        "/audit",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
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
      <div style={{ marginBottom: "12px", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <button onClick={onBack} style={{ marginRight: "10px" }}>
            ◀ Back
          </button>
        </div>
        <div>
          <button onClick={submitAudit} disabled={loading}>
            {loading ? "Running..." : "Run Audit"}
          </button>
        </div>
      </div>

      {!aiEnabled && (
        <div style={{ marginBottom: 12, color: '#fff', background: '#b00020', padding: 8, borderRadius: 6 }}>
          AI is turned off. To enable AI comments, add an `OPENAI_API_KEY` to your `.env` and set `USE_AI=true`.
        </div>
      )}

      {aiEnabled && !aiReal && (
        <div style={{ marginBottom: 12, color: '#333', background: '#fff3cd', padding: 8, borderRadius: 6 }}>
          <strong>AI is running in local mock mode</strong> — you will see helpful generated explanations but these are not from OpenAI. To use real OpenAI responses, set `OPENAI_API_KEY` in your `.env`.
        </div>
      )}

      <div className="form-row">
        <div className="form-group">
          <label>Fare</label>
          <input type="number" name="fare" value={form.fare} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Tax</label>
          <input type="number" name="tax" value={form.tax} onChange={handleChange} />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Commission</label>
          <input type="number" name="commission" value={form.commission} onChange={handleChange} />
        </div>
        <div className="form-group">
          <label>Refund Amount</label>
          <input type="number" name="refund_amount" value={form.refund_amount} onChange={handleChange} />
        </div>
      </div>

      {error && <div style={{ color: "#b00020", marginBottom: "12px" }}>{error}</div>}

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
                    <li key={idx} style={{ marginBottom: 8 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                          <strong>{i.message}</strong>
                          {i.field && (
                            <div style={{ fontSize: 12, color: '#666' }}>{`${i.field}: ${i.value}`}</div>
                          )}
                        </div>
                        <div>
                          <span
                            style={{
                              padding: '4px 8px',
                              borderRadius: 6,
                              background: i.severity === 'high' ? '#fee2e2' : i.severity === 'medium' ? '#fef3c7' : '#eef2ff',
                              color: i.severity === 'high' ? '#b91c1c' : i.severity === 'medium' ? '#92400e' : '#1e3a8a',
                              fontWeight: 700,
                              fontSize: 12,
                              textTransform: 'capitalize'
                            }}
                          >
                            {i.severity}
                          </span>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <div>No issues found</div>
              )}
            </div>

            <div style={{ flex: 1 }}>
              <h4>AI Comments {response.ai_real === false && <small style={{ color: '#666' }}>(mock)</small>}</h4>
              {response.ai_comments && response.ai_comments.length ? (
                <ol>
                  {response.ai_comments.map((c, idx) => (
                    <li key={idx} style={{ marginBottom: 8 }}>{c}</li>
                  ))}
                </ol>
              ) : (
                <div style={{ color: '#666' }}>{response.ai_real === false ? 'AI comments are mock-generated. Set OPENAI_API_KEY to use real OpenAI responses.' : 'No AI comments'}</div>
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
