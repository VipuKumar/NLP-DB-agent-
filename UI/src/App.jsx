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
    <div style={{ padding: 30, fontFamily: "sans-serif", maxWidth: 800 }}>
      <h2>SQL Agent v1</h2>

      <textarea
        rows={3}
        style={{ width: "100%" }}
        placeholder="Ask something..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <div style={{ marginTop: 10 }}>
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="read">Read</option>
          <option value="write">Write</option>
        </select>

        <button onClick={generate} style={{ marginLeft: 10 }}>
          Generate
        </button>
      </div>

      {generated && (
        <>
          <h3>Generated SQL</h3>
          <pre>{generated.sql}</pre>

          {/* INSERT: already executed */}
          {generated.status === "inserted" && (
            <p style={{ color: "green" }}>✅ Insert executed successfully</p>
          )}

          {/* READ results */}
          {generated.rows && (
            <>
              <h3>Result</h3>
              <pre>{JSON.stringify(generated.rows, null, 2)}</pre>
            </>
          )}

          {/* UPDATE / DELETE */}
          {generated.write_set_hash && (
            <>
              <p><b>Write-set hash:</b> {generated.write_set_hash}</p>

              <input
                placeholder="Approved by"
                value={approvedBy}
                onChange={(e) => setApprovedBy(e.target.value)}
              />

              <button onClick={execute} style={{ marginLeft: 10 }}>
                Execute
              </button>
            </>
          )}
        </>
      )}

      {result && (
        <>
          <h3>Execution Result</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </>
      )}

      {error && (
        <p style={{ color: "red" }}>
          Error: {error}
        </p>
      )}
    </div>
  );
}
