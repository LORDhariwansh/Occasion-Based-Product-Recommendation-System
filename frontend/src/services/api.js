const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function getRecommendations(occasion, topK = 6) {
  const response = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ occasion, top_k: topK }),
  });
  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(
      detail.detail || "We could not find recommendations right now.",
    );
  }
  return response.json();
}
