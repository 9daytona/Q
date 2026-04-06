"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [Patient, setPatients] = useState([]);
  const [name, setName] = useState("");
  const [age, setAge] = useState("");

  // Load residents from backend
  const loadPatients = async () => {
    const res = await fetch("/api/Patient");
    const data = await res.json();
    setPatients(data);
  };

  useEffect(() => {
    loadPatients();
  }, []);

  // Add Patient
  const addPatient = async () => {
    await fetch("/api/Patient", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name,
        age: Number(age),
      }),
    });

    setName("");
    setAge("");
    loadPatients(); // refresh list
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Q Care Platform</h1>

      <h2>Add Patient</h2>
      <input
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        placeholder="Age"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />
      <button onClick={addPatient}>Add Patient</button>

      <h2>Patients</h2>
      <ul>
        {Patient.map((r, i) => (
          <li key={i}>
            {r.name} (Age: {r.age})
          </li>
        ))}
      </ul>
    </div>
  );
}