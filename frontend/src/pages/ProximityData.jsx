import React, { useState } from "react";

export default function ProximityData() {
  const [form, setForm] = useState({
    start_date: "",
    end_date: "",
    interval: "1H",
  });
  const [plot, setPlot] = useState(null);
  const [message, setMessage] = useState("");

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
  e.preventDefault();
  setMessage("Loading...");

  try {
    const params = new URLSearchParams(form).toString();
    const res = await fetch(`http://127.0.0.1:8010/proximity-data/?${params}`, {
      method: "GET",
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    setPlot(data.plot_image);
    setMessage(data.message);
  } catch (err) {
    console.error("Fetch error:", err);
    setMessage("Error fetching data");
  }
};
  return (
    <div style={{ textAlign: "center", marginTop: "30px" }}>
      <h2>Proximity Data Plot</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input type="date" name="start_date" onChange={handleChange} required />{" "}
        <input type="date" name="end_date" onChange={handleChange} required />{" "}
        <select name="interval" onChange={handleChange} value={form.interval}>
          <option value="30T">30 min</option>
          <option value="1H">1 hour</option>
          <option value="6H">6 hours</option>
          <option value="1D">1 day</option>
        </select>{" "}
        <button type="submit">Generate</button>
      </form>

      {message && <p>{message}</p>}
      {plot && (
        <img
          src={`data:image/png;base64,${plot}`}
          alt="Proximity Plot"
          style={{ width: "80%" }}
        />
      )}
    </div>
  );
}
