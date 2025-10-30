import React from "react";
import ProximityData from "./pages/ProximityData";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Signup from "./pages/signup/Signup";



export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/proximity-data" element={<ProximityData />} />
        
      </Routes>
    </Router>
  );
}




