"use client";
import {useState, useEffect} from "react";

export default function Dashboard() {
  const [activePanel, setActivePanel]=useState("Home");

  // DATA STATES
  const [patient, setPatient] = useState([]);
  const [observations, setObservation] = useState([]);
  const [envr, setEnvr] = useState([]);
  const [assistanceCalls, setAssistanceCalls] = useState([]);
  const [appointments, setAppointments] = useState([]);

  // LOAD BACKEND FOR SELECTED PANEL
  useEffect(() => {
    if (activePanel === "Patient") fetch("/api/Patient").then(r=> r.json()).then(setPatient);
    if (activePanel === "Vitals") fetch("/api/Observation").then(r=>r.json()).then(setObservation);
    if (activePanel === "Environment") fetch("/api/envr").then(r=> r.json()).then(setEnvr);
    if (activePanel === "Assistance") fetch("/api/AssistanceCall").then(r => r.json()).then(setAssistanceCalls);

  }, [activePanel]);

  // LAYOUT
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Left navigation pane */}
      <nav style={{ width: 200, backgroundColor: "#1E293B", color: "#fff", padding: 20 }}>
        <h2>Q Care Platform</h2>
        {["Home","Patients","Vitals","Clinical","Environment","Assistance","Telehealth","Family"].map(panel => (
          <div
            key={panel}
            style={{
              padding: 10,
              marginTop: 10,
              cursor: "pointer",
              backgroundColor: activePanel === panel ? "#334155" : "transparent"
            }}
            onClick={() => setActivePanel(panel)}
          >
            {panel}
          </div>
        ))}
      </nav>

      {/* Central dashboard area */}
      <main style={{ flex: 1, padding: 20, overflowY: "auto" }}>
        {activePanel === "Home" && <h1>Welcome to Q Care Platform</h1>}

        {activePanel === "Residents" && (
          <div>
            <h2>Residents</h2>
            <ul>
              {patient.map((r:any, i:number) => <li key={i}>{r.name} (Age: {r.age})</li>)}
            </ul>
          </div>
        )}

        {activePanel === "Vitals" && (
          <div>
            <h2>Vitals / Observations</h2>
            {observations.map((v:any,i:number) => (
              <div key={i}>
                {v.residentName} - HR: {v.heartRate} bpm, BP: {v.bp}
              </div>
            ))}
          </div>
        )}

        {activePanel === "Environment" && (
          <div>
            <h2>Environmental Monitoring</h2>
            {envr.map((e:any,i:number) => (
              <div key={i}>
                HVAC: {e.hvac} | Lighting: {e.lighting} | Water: {e.water}
              </div>
            ))}
          </div>
        )}

        {activePanel === "Assistance" && (
          <div>
            <h2>Assistance / Staff Calls</h2>
            {assistanceCalls.map((c:any,i:number) => (
              <div key={i}>
                {c.residentName} called from {c.wing}, bed #{c.bed}
              </div>
            ))}
          </div>
        )}

        {activePanel === "Telehealth" && (
          <div>
            <h2>Telehealth Appointments</h2>
            {appointments.map((t:any,i:number) => (
              <div key={i}>
                {t.residentName} with {t.specialist} at {t.time}
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );

}