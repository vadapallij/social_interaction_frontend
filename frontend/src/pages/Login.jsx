import React, { useState } from "react";
import axios from "axios";

export default function Login() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:8010/login", new URLSearchParams(form), {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      const token = res.data.access_token;
      localStorage.setItem("token", token);
      localStorage.setItem("username", res.data.username);
      window.location.href = "/dashboard"; // Redirect after success
    } catch (err) {
      setError("Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Login to CareWatch</h2>
      <form onSubmit={handleSubmit} style={{ display: "inline-block", width: "300px" }}>
        <input
          name="username"
          type="text"
          placeholder="Username"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
        />
        <input
          name="password"
          type="password"
          placeholder="Password"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "10px", padding: "8px" }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{ width: "100%", padding: "10px", background: "#2b6cb0", color: "#fff" }}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
        <p>
            Don’t have an account? <a href="/signup">Register here</a>
        </p>
      </form>

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
