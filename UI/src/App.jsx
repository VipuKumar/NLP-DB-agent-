import { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [mode, setMode] = useState("read");
  const [generated, setGenerated] = useState(null);
  const [approvedBy, setApprovedBy] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const generate = async () => {
    setError(null);
    setResult(null);
    setGenerated(null);

    const res = await fetch("http://127.0.0.1:8000/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question, mode }),
    });

    const data = await res.json();
    if (!res.ok) {
      setError(data.detail || "Generate failed");
      return;
    }

    setGenerated(data);
  };

  const execute = async () => {
    setError(null);

    const res = await fetch("http://127.0.0.1:8000/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sql: generated.sql,
        write_set_hash: generated.write_set_hash,
        approved_by: approvedBy,
      }),
    });

    const data = await res.json();
    if (!res.ok) {
      setError(data.detail || "Execution failed");
      return;
    }

    setResult(data);
  };

  return (
    <div
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        minHeight: "100vh",
        width: "100vw",
        alignItems: "center",
        justifyContent: "center",
        padding: "40px 20px",
        fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
      }}
    >
      <div style={{
        maxWidth: 800,
        margin: "0 auto",
        background: "#ffffff",
        borderRadius: 16,
        padding: 40,
        boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
      }}>
      <h2 style={{ 
        color: "#667eea", 
        marginBottom: 8,
        fontSize: "2rem",
        fontWeight: 700,
      }}>SQL Agent v1</h2>
      <p style={{
        color: "#718096",
        marginBottom: 24,
        fontSize: "0.9rem"
      }}>Generate and execute SQL queries with AI assistance</p>

      <textarea
        rows={4}
        style={{
          width: "100%",
          background: "#f7fafc",
          color: "#2d3748",
          border: "2px solid #e2e8f0",
          borderRadius: 12,
          padding: "14px",
          fontSize: "1rem",
          marginBottom: 20,
          boxSizing: "border-box",
          boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
          transition: "all 0.2s",
          outline: "none",
        }}
        placeholder="Enter your SQL query prompt here..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onFocus={(e) => e.target.style.borderColor = "#667eea"}
        onBlur={(e) => e.target.style.borderColor = "#e2e8f0"}
      />

      <div style={{ marginBottom: 24, display: "flex", alignItems: "center", gap: 12 }}>
        <select
          value={mode}
          onChange={(e) => setMode(e.target.value)}
          style={{
            background: "#f7fafc",
            color: "#2d3748",
            border: "2px solid #e2e8f0",
            borderRadius: 10,
            padding: "10px 14px",
            fontSize: "1rem",
            boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
            cursor: "pointer",
            outline: "none",
          }}
        >
          <option value="read">Read</option>
          <option value="write">Write</option>
        </select>

        <button
          onClick={generate}
          style={{
            background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            color: "#fff",
            border: "none",
            borderRadius: 10,
            padding: "10px 24px",
            fontSize: "1rem",
            fontWeight: 600,
            cursor: "pointer",
            boxShadow: "0 4px 12px rgba(102, 126, 234, 0.4)",
            transition: "all 0.2s",
          }}
          onMouseOver={(e) => e.target.style.transform = "translateY(-2px)"}
          onMouseOut={(e) => e.target.style.transform = "translateY(0)"}
        >
          Generate SQL
        </button>
      </div>

      {generated && (
        <div
          style={{
            background: "linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)",
            borderRadius: 12,
            padding: 24,
            marginBottom: 20,
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            border: "1px solid #e2e8f0"
          }}
        >
          <h3 style={{ 
            color: "#667eea", 
            marginTop: 0,
            marginBottom: 16,
            fontSize: "1.2rem",
            fontWeight: 600 
          }}>Generated SQL</h3>
          <pre
            style={{
              background: "#2d3748",
              color: "#a0aec0",
              border: "none",
              borderRadius: 8,
              padding: "16px",
              fontSize: "0.9rem",
              marginBottom: 16,
              overflowX: "auto",
              boxShadow: "inset 0 2px 4px rgba(0,0,0,0.2)",
            }}
          >
            {generated.sql}
          </pre>

          {/* INSERT: already executed */}
          {generated.status === "inserted" && (
            <div style={{ 
              background: "#c6f6d5",
              color: "#22543d",
              padding: "12px 16px",
              borderRadius: 8,
              marginBottom: 16,
              fontWeight: 500,
              border: "1px solid #9ae6b4"
            }}>
              ✅ Insert executed successfully
            </div>
          )}

          {/* READ results */}
          {generated.rows && (
            <>
              <h3 style={{ 
                color: "#667eea",
                marginBottom: 12,
                fontSize: "1.1rem",
                fontWeight: 600 
              }}>Results ({generated.rows.length} row{generated.rows.length !== 1 ? 's' : ''})</h3>
              <div style={{ overflowX: "auto", marginBottom: 16 }}>
                <table style={{
                  width: "100%",
                  borderCollapse: "collapse",
                  background: "#ffffff",
                  borderRadius: 8,
                  overflow: "hidden",
                  boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
                }}>
                  <thead>
                    <tr style={{ background: "#667eea" }}>
                      {(Array.isArray(generated.rows[0]) 
                        ? generated.rows[0].map((_, i) => `Column ${i + 1}`)
                        : Object.keys(generated.rows[0] || {})
                      ).map((key, idx) => (
                        <th key={idx} style={{
                          padding: "12px 16px",
                          textAlign: "left",
                          color: "#ffffff",
                          fontWeight: 600,
                          fontSize: "0.9rem",
                          borderBottom: "2px solid #5568d3",
                          whiteSpace: "nowrap"
                        }}>
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {generated.rows.map((row, idx) => (
                      <tr key={idx} style={{
                        background: idx % 2 === 0 ? "#f7fafc" : "#ffffff",
                        transition: "background 0.2s"
                      }}
                      onMouseOver={(e) => e.currentTarget.style.background = "#edf2f7"}
                      onMouseOut={(e) => e.currentTarget.style.background = idx % 2 === 0 ? "#f7fafc" : "#ffffff"}
                      >
                        {(Array.isArray(row) ? row : Object.values(row)).map((val, i) => (
                          <td key={i} style={{
                            padding: "12px 16px",
                            color: "#2d3748",
                            fontSize: "0.9rem",
                            borderBottom: "1px solid #e2e8f0",
                            whiteSpace: "nowrap"
                          }}>
                            {val !== null && val !== undefined ? String(val) : <span style={{ color: "#a0aec0", fontStyle: "italic" }}>null</span>}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}

          {/* UPDATE / DELETE */}
          {generated.write_set_hash && (
            <>
              <div style={{
                background: "#fff3cd",
                border: "1px solid #ffc107",
                borderRadius: 8,
                padding: "12px 16px",
                marginBottom: 16,
                color: "#856404"
              }}>
                <b>Write-set hash:</b> {generated.write_set_hash}
              </div>

              <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                <input
                  placeholder="Approved by"
                  style={{
                    flex: 1,
                    background: "#ffffff",
                    color: "#2d3748",
                    border: "2px solid #e2e8f0",
                    borderRadius: 10,
                    padding: "10px 14px",
                    fontSize: "1rem",
                    boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
                    outline: "none",
                  }}
                  value={approvedBy}
                  onChange={(e) => setApprovedBy(e.target.value)}
                  onFocus={(e) => e.target.style.borderColor = "#667eea"}
                  onBlur={(e) => e.target.style.borderColor = "#e2e8f0"}
                />

                <button
                  onClick={execute}
                  style={{
                    background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    color: "#fff",
                    border: "none",
                    borderRadius: 10,
                    padding: "10px 24px",
                    fontSize: "1rem",
                    fontWeight: 600,
                    cursor: "pointer",
                    boxShadow: "0 4px 12px rgba(102, 126, 234, 0.4)",
                    transition: "all 0.2s",
                  }}
                  onMouseOver={(e) => e.target.style.transform = "translateY(-2px)"}
                  onMouseOut={(e) => e.target.style.transform = "translateY(0)"}
                >
                  Execute
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {result && (
        <div
          style={{
            background: "linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)",
            borderRadius: 12,
            padding: 24,
            marginBottom: 20,
            boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            border: "1px solid #e2e8f0"
          }}
        >
          <h3 style={{ 
            color: "#667eea",
            marginTop: 0,
            marginBottom: 16,
            fontSize: "1.2rem",
            fontWeight: 600 
          }}>Execution Result</h3>
          <pre
            style={{
              background: "#ffffff",
              color: "#2d3748",
              border: "1px solid #e2e8f0",
              borderRadius: 8,
              padding: "16px",
              fontSize: "0.9rem",
              marginBottom: 0,
              overflowX: "auto",
              boxShadow: "0 1px 3px rgba(0,0,0,0.05)",
            }}
          >
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}

      {error && (
        <div style={{ 
          background: "#fed7d7",
          color: "#c53030",
          borderRadius: 8,
          padding: "12px 16px",
          marginTop: 16,
          fontWeight: 500,
          border: "1px solid #fc8181"
        }}>
          ⚠️ Error: {error}
        </div>
      )}
      </div>
    </div>
  );
}