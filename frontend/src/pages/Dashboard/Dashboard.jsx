import React from "react";

export default function Dashboard() {
  const username = localStorage.getItem("username");

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Welcome, {username || "User"} 👋</h2>
      <p>This is your dashboard page connected to FastAPI backend.</p>

      <button
        onClick={() => {
          localStorage.clear();
          window.location.href = "/";
        }}
        style={{
          padding: "10px 20px",
          background: "#e53e3e",
          color: "#fff",
          border: "none",
          borderRadius: "4px",
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </div>
  );
}