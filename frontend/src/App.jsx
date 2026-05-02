import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [mode, setMode] = useState("semantic");
  const [detail, setDetail] = useState("high");
  const [results, setResults] = useState([]);
  const [ragAnswer, setRagAnswer] = useState("");
  const [responseMode, setResponseMode] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setResults([]);
    setRagAnswer("");
    setResponseMode("");

    if (!query.trim()) {
      setMessage("Please enter a search query.");
      return;
    }

    try {
      setLoading(true);

      const detailParam = mode === "rag" ? `&detail=${detail}` : "";
      const response = await fetch(
        `${API_BASE_URL}/search?q=${encodeURIComponent(query)}&top_k=${topK}&mode=${mode}${detailParam}`
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Backend error. Please check if FastAPI is running.");
      }

      const data = await response.json();

      setResponseMode(data.mode);

      if (data.mode === "rag") {
        setRagAnswer(data.answer || "");
        setResults(data.source_chunks || []);
      } else {
        setResults(data.results || []);
      }

      setMessage(data.message || "");
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="page">
      <section className="card">
        <h1>WikiVector Search</h1>
        <p className="subtitle">
          Search your local vector database using natural language.
        </p>

        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Example: How is AI related to cloud computing?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />

          <select value={topK} onChange={(e) => setTopK(Number(e.target.value))}>
            <option value={3}>Top 3</option>
            <option value={5}>Top 5</option>
            <option value={10}>Top 10</option>
          </select>

          <button type="submit" disabled={loading}>
            {loading ? (mode === "rag" ? "Generating..." : "Searching...") : "Search"}
          </button>
        </form>

        <fieldset className="mode-selector">
          <legend>Search Mode</legend>

          <label className={`mode-option ${mode === "semantic" ? "mode-option--active" : ""}`}>
            <input
              type="radio"
              name="mode"
              value="semantic"
              checked={mode === "semantic"}
              onChange={() => setMode("semantic")}
            />
            <span className="mode-label">
              <span className="mode-name">Semantic Retrieval</span>
              <span className="mode-desc">Returns the top matching chunks from the vector database</span>
            </span>
          </label>

          <label className={`mode-option ${mode === "rag" ? "mode-option--active" : ""}`}>
            <input
              type="radio"
              name="mode"
              value="rag"
              checked={mode === "rag"}
              onChange={() => setMode("rag")}
            />
            <span className="mode-label">
              <span className="mode-name">RAG Answer</span>
              <span className="mode-desc">Generates a natural language answer using retrieved chunks as context</span>
            </span>
          </label>
        </fieldset>

        {mode === "rag" && (
          <fieldset className="mode-selector">
            <legend>Answer Detail</legend>

            <label className={`mode-option ${detail === "low" ? "mode-option--active" : ""}`}>
              <input
                type="radio"
                name="detail"
                value="low"
                checked={detail === "low"}
                onChange={() => setDetail("low")}
              />
              <span className="mode-label">
                <span className="mode-name">Concise</span>
                <span className="mode-desc">Short, direct answer (~100 tokens)</span>
              </span>
            </label>

            <label className={`mode-option ${detail === "high" ? "mode-option--active" : ""}`}>
              <input
                type="radio"
                name="detail"
                value="high"
                checked={detail === "high"}
                onChange={() => setDetail("high")}
              />
              <span className="mode-label">
                <span className="mode-name">Detailed</span>
                <span className="mode-desc">Longer, elaborated answer (~500 tokens)</span>
              </span>
            </label>
          </fieldset>
        )}

        {message && <p className="message">{message}</p>}
        {error && <p className="error">{error}</p>}

        {responseMode === "rag" && ragAnswer && (
          <section className="rag-answer">
            <h2 className="rag-answer__heading">Generated Answer</h2>
            <p className="rag-answer__text">{ragAnswer}</p>
            {results.length > 0 && (
              <p className="rag-answer__source-label">
                Based on {results.length} source chunk{results.length !== 1 ? "s" : ""}
              </p>
            )}
          </section>
        )}

        <section className="results">
          {responseMode === "rag" && results.length > 0 && (
            <h3 className="source-heading">Source Chunks</h3>
          )}
          {results.map((item, index) => (
            <article key={item.id} className="result-card">
              <div className="result-header">
                <h2>{responseMode === "rag" ? `Source ${index + 1}` : `Result ${index + 1}`}</h2>
                <span>Distance: {item.distance.toFixed(4)}</span>
              </div>

              <p className="article">
                Article: {item.metadata?.article || "Unknown"}
              </p>

              <p className="text">{item.text}</p>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}

export default App;
