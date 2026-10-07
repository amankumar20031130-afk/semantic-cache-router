import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { askQuery, getSummary } from "./api";

function App() {
  const [summary, setSummary] = useState(null);
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchSummary = async () => {
    try {
      const data = await getSummary();
      setSummary(data);
    } catch (err) {
      console.error(err);
      setError("Unable to connect to backend");
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  const handleQuery = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError("");

      const data = await askQuery(query);

      setResult(data);

      // Refresh dashboard metrics
      await fetchSummary();
    } catch (err) {
      console.error(err);
      setError("Failed to process query");
    } finally {
      setLoading(false);
    }
  };

  if (error && !summary) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-500 text-lg">{error}</p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 p-8">

      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">
          Semantic Cache & Cost-Aware Router
        </h1>

        <p className="mt-2 text-slate-500">
          Monitor cache performance, model routing, cost and latency.
        </p>
      </div>

      {/* Query Playground */}
      <div className="bg-white rounded-xl shadow-sm p-6 mb-8">

        <h2 className="text-xl font-semibold text-slate-800">
          Query Playground
        </h2>

        <p className="text-sm text-slate-500 mt-1 mb-4">
          Send a query through the semantic cache and cost-aware router.
        </p>

        <div className="flex gap-3">

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleQuery();
              }
            }}
            placeholder="Ask something..."
            className="flex-1 border border-slate-300 rounded-lg px-4 py-3 outline-none focus:ring-2 focus:ring-slate-400"
          />

          <button
            onClick={handleQuery}
            disabled={loading}
            className="bg-slate-800 text-white px-6 py-3 rounded-lg hover:bg-slate-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Send Query"}
          </button>

        </div>

        {/* Error */}
        {error && (
          <p className="text-red-500 mt-3">
            {error}
          </p>
        )}

        {/* Query Result */}
        {result && (
          <div className="mt-6 border-t pt-6">

            <h3 className="font-semibold text-slate-800 mb-3">
              Response
            </h3>

            <div className="bg-slate-50 rounded-lg p-6 text-slate-700">

              <div className="prose prose-slate max-w-none">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-2xl font-bold text-slate-800 mb-4">
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2 className="text-xl font-bold text-slate-800 mt-6 mb-3">
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3 className="text-lg font-semibold text-slate-800 mt-5 mb-2">
                        {children}
                      </h3>
                    ),

                    p: ({ children }) => (
                      <p className="mb-4 leading-7">
                        {children}
                      </p>
                    ),

                    ul: ({ children }) => (
                      <ul className="list-disc ml-6 mb-4 space-y-2">
                        {children}
                      </ul>
                    ),

                    ol: ({ children }) => (
                      <ol className="list-decimal ml-6 mb-4 space-y-2">
                        {children}
                      </ol>
                    ),

                    li: ({ children }) => (
                      <li className="leading-6">
                        {children}
                      </li>
                    ),

                    strong: ({ children }) => (
                      <strong className="font-semibold text-slate-900">
                        {children}
                      </strong>
                    ),

                    table: ({ children }) => (
                      <div className="overflow-x-auto mb-6">
                        <table className="min-w-full border border-slate-300 rounded-lg overflow-hidden">
                          {children}
                        </table>
                      </div>
                    ),

                    thead: ({ children }) => (
                      <thead className="bg-slate-200">
                        {children}
                      </thead>
                    ),

                    th: ({ children }) => (
                      <th className="border border-slate-300 px-4 py-3 text-left font-semibold">
                        {children}
                      </th>
                    ),

                    td: ({ children }) => (
                      <td className="border border-slate-300 px-4 py-3">
                        {children}
                      </td>
                    ),

                    code: ({ inline, children }) =>
                      inline ? (
                        <code className="bg-slate-200 px-1.5 py-0.5 rounded text-sm">
                          {children}
                        </code>
                      ) : (
                        <pre className="bg-slate-900 text-slate-100 rounded-lg p-4 overflow-x-auto mb-4">
                          <code>{children}</code>
                        </pre>
                      ),
                  }}
                >
                  {result.answer}
                </ReactMarkdown>

              </div>

            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">

              <div className="bg-slate-50 rounded-lg p-4">
                <p className="text-xs text-slate-500">
                  Cache
                </p>
                <p className="font-semibold mt-1">
                  {result.cache_hit ? "HIT" : "MISS"}
                </p>
              </div>

              <div className="bg-slate-50 rounded-lg p-4">
                <p className="text-xs text-slate-500">
                  Similarity
                </p>
                <p className="font-semibold mt-1">
                  {result.similarity !== null
                    ? result.similarity.toFixed(3)
                    : "—"}
                </p>
              </div>

              <div className="bg-slate-50 rounded-lg p-4">
                <p className="text-xs text-slate-500">
                  Model
                </p>
                <p className="font-semibold mt-1">
                  {result.model || "Cached"}
                </p>
              </div>

              <div className="bg-slate-50 rounded-lg p-4">
                <p className="text-xs text-slate-500">
                  Route
                </p>
                <p className="font-semibold mt-1">
                  {result.route || "Cache"}
                </p>
              </div>

            </div>

          </div>
        )}

      </div>

      {/* Dashboard Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">

        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-slate-500">
            Total Requests
          </p>

          <h2 className="text-3xl font-bold text-slate-800 mt-2">
            {summary.total_requests}
          </h2>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-slate-500">
            Cache Hit Rate
          </p>

          <h2 className="text-3xl font-bold text-slate-800 mt-2">
            {summary.cache_hit_rate}%
          </h2>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-slate-500">
            Total Cost
          </p>

          <h2 className="text-3xl font-bold text-slate-800 mt-2">
            ${summary.total_cost}
          </h2>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">
          <p className="text-sm text-slate-500">
            Average Latency
          </p>

          <h2 className="text-3xl font-bold text-slate-800 mt-2">
            {summary.average_latency_ms} ms
          </h2>
        </div>

      </div>

      {/* Model + Cache */}
      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">

        <div className="bg-white rounded-xl shadow-sm p-6">

          <h2 className="text-xl font-semibold text-slate-800">
            Model Usage
          </h2>

          <div className="mt-6 space-y-4">

            <div className="flex justify-between">
              <span className="text-slate-600">
                Small Model
              </span>

              <span className="font-semibold">
                {summary.small_model_requests}
              </span>
            </div>

            <div className="flex justify-between">
              <span className="text-slate-600">
                Large Model
              </span>

              <span className="font-semibold">
                {summary.large_model_requests}
              </span>
            </div>

          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm p-6">

          <h2 className="text-xl font-semibold text-slate-800">
            Cache Performance
          </h2>

          <div className="mt-6">

            <div className="flex justify-between mb-2">

              <span className="text-slate-600">
                Cache Hits
              </span>

              <span className="font-semibold">
                {summary.cache_hits}
              </span>

            </div>

            <div className="w-full bg-slate-200 rounded-full h-3">

              <div
                className="bg-green-500 h-3 rounded-full"
                style={{
                  width: `${summary.cache_hit_rate}%`,
                }}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default App;