const API_BASE = "http://localhost:5000"; // or "http://172.20.130.147:5000" if you're on a different device

export async function askRhetorica(query) {
  const res = await fetch(`${API_BASE}/ask?q=${encodeURIComponent(query)}`);
  const data = await res.json();
  return data.response;
}
