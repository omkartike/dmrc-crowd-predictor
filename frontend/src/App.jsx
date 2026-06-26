import { useState, useEffect } from "react"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

const CROWD_CONFIG = {
  High:   { color: "#dc2626", bg: "#fef2f2", emoji: "🔴", advice: "Very crowded. Try boarding 30 min later or use a different coach." },
  Medium: { color: "#d97706", bg: "#fffbeb", emoji: "🟡", advice: "Moderately crowded. First and last coaches are typically less full." },
  Low:    { color: "#16a34a", bg: "#f0fdf4", emoji: "🟢", advice: "Good time to travel. Comfortable ride expected." },
}

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

export default function App() {
  const [stations, setStations] = useState([])
  const [lines, setLines]       = useState([])
  const [station, setStation]   = useState("")
  const [line, setLine]         = useState("")
  const [hour, setHour]         = useState(9)
  const [dayOfWeek, setDay]     = useState(0)
  const [result, setResult]     = useState(null)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState("")

  useEffect(() => {
    Promise.all([
      fetch(`${API}/stations`).then(r => r.json()),
      fetch(`${API}/lines`).then(r => r.json())
    ]).then(([s, l]) => { setStations(s.stations); setLines(l.lines) })
  }, [])

  const predict = async () => {
    if (!station || !line) { setError("Please select a station and line."); return }
    setLoading(true); setError("")
    try {
      const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ station, line, hour, day_of_week: dayOfWeek })
      })
      if (!res.ok) throw new Error(await res.text())
      setResult(await res.json())
    } catch (e) { setError("Prediction failed. Is the backend running?") }
    finally { setLoading(false) }
  }

  const cfg = result ? CROWD_CONFIG[result.crowd_level] : null

  return (
    <div style={{minHeight:"100vh", background:"#f8f7f3", padding:"40px 20px"}}>
      <div style={{maxWidth:520, margin:"0 auto"}}>

        <h1 style={{fontSize:24, fontWeight:700, marginBottom:4}}>
          🚇 Delhi Metro Crowd Predictor
        </h1>
        <p style={{color:"#6b6860", marginBottom:28, fontSize:14}}>
          Check predicted crowd levels before you board
        </p>

        <div style={{background:"white", borderRadius:12, padding:24, border:"1px solid #e2dfd8"}}>
          <label style={{display:"block", fontSize:13, fontWeight:600, marginBottom:6}}>Station</label>
          <select value={station} onChange={e => setStation(e.target.value)}
            style={{width:"100%", padding:"9px 12px", borderRadius:8, border:"1px solid #e2dfd8", marginBottom:16, fontSize:14}}>
            <option value="">Select a station</option>
            {stations.map(s => <option key={s}>{s}</option>)}
          </select>

          <label style={{display:"block", fontSize:13, fontWeight:600, marginBottom:6}}>Line</label>
          <select value={line} onChange={e => setLine(e.target.value)}
            style={{width:"100%", padding:"9px 12px", borderRadius:8, border:"1px solid #e2dfd8", marginBottom:16, fontSize:14}}>
            <option value="">Select a line</option>
            {lines.map(l => <option key={l}>{l}</option>)}
          </select>

          <label style={{display:"block", fontSize:13, fontWeight:600, marginBottom:6}}>
            Hour — {hour}:00 {hour < 12 ? "AM" : "PM"}
          </label>
          <input type="range" min={5} max={23} value={hour} onChange={e => setHour(+e.target.value)}
            style={{width:"100%", marginBottom:16}}/>

          <label style={{display:"block", fontSize:13, fontWeight:600, marginBottom:6}}>Day</label>
          <div style={{display:"flex", gap:6, flexWrap:"wrap", marginBottom:20}}>
            {DAYS.map((d, i) => (
              <button key={i} onClick={() => setDay(i)}
                style={{padding:"5px 10px", borderRadius:20, border:"1px solid #e2dfd8", fontSize:12,
                  background: dayOfWeek === i ? "#1a6b3c" : "white",
                  color: dayOfWeek === i ? "white" : "#6b6860", cursor:"pointer"}}>
                {d.slice(0, 3)}
              </button>
            ))}
          </div>

          {error && <p style={{color:"#dc2626", fontSize:13, marginBottom:12}}>{error}</p>}

          <button onClick={predict} disabled={loading}
            style={{width:"100%", padding:"12px", borderRadius:8, border:"none",
              background:"#1a6b3c", color:"white", fontSize:15, fontWeight:600, cursor:"pointer"}}>
            {loading ? "Predicting…" : "Check crowd level"}
          </button>
        </div>

        {cfg && (
          <div style={{marginTop:20, background:cfg.bg, border:`1px solid ${cfg.color}`,
            borderRadius:12, padding:20}}>
            <div style={{fontSize:32, fontWeight:800, color:cfg.color, marginBottom:4}}>
              {cfg.emoji} {result.crowd_level}
            </div>
            <div style={{fontSize:13, color:"#374151", marginBottom:8}}>{cfg.advice}</div>
            <div style={{fontSize:12, color:"#6b6860"}}>
              Model confidence: <strong>{result.confidence}%</strong>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}