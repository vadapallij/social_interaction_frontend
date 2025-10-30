import React, { useState } from "react";
import axios from "axios";

export default function Signup() {
  const [form, setForm] = useState({
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:8010/register", form);
      setMessage(res.data.message);
    } catch (err) {
      if (err.response?.status === 400)
        setError("Username already exists.");
      else setError("Registration failed. Please try again.");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h2>Create an Account</h2>
      <form
        onSubmit={handleSubmit}
        style={{ display: "inline-block", width: "320px", textAlign: "left" }}
      >
        <label>Username</label>
        <input
          name="username"
          type="text"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "8px", padding: "8px" }}
        />
        <label>First Name</label>
        <input
          name="first_name"
          type="text"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "8px", padding: "8px" }}
        />
        <label>Last Name</label>
        <input
          name="last_name"
          type="text"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "8px", padding: "8px" }}
        />
        <label>Email</label>
        <input
          name="email"
          type="email"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "8px", padding: "8px" }}
        />
        <label>Password</label>
        <input
          name="password"
          type="password"
          onChange={handleChange}
          required
          style={{ width: "100%", marginBottom: "12px", padding: "8px" }}
        />
        <button
          type="submit"
          style={{
            width: "100%",
            padding: "10px",
            background: "#2b6cb0",
            color: "#fff",
            border: "none",
            cursor: "pointer",
          }}
        >
          Register
        </button>
      </form>
      {message && <p style={{ color: "green" }}>{message}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}