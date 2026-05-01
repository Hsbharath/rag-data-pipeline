import { useState } from "react";
import "./App.css";

const API_BASE_URL = "http://127.0.0.1:8000";

function App() {
  const [query, setQuery] = useState("");
  const [topK, setTopK] = useState(5);
  const [results, setResults] = useState([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (event) => {
    event.preventDefault();

    setError("");
    setMessage("");
    setResults([]);

    if (!query.trim()) {
      setMessage("Please enter a search query.");
      return;
    }

    try {
      setLoading(true);

      const response = await fetch(
        `${API_BASE_URL}/search?q=${encodeURIComponent(query)}&top_k=${topK}`
      );

      if (!response.ok) {
        throw new Error("Backend error. Please check if FastAPI is running.");
      }

      const data = await response.json();

      setResults(data.results || []);
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
            {loading ? "Searching..." : "Search"}
          </button>
        </form>

        {message && <p className="message">{message}</p>}
        {error && <p className="error">{error}</p>}

        <section className="results">
          {results.map((item, index) => (
            <article key={item.id} className="result-card">
              <div className="result-header">
                <h2>Result {index + 1}</h2>
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