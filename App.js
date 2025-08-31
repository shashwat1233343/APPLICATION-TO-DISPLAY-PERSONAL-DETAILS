import React, { useState, useEffect } from "react";

function App() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/profiles/1") // calling FastAPI
      .then((res) => res.json())
      .then((data) => setProfile(data))
      .catch((err) => console.error("Error fetching profile:", err));
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>My API Playground</h1>
      {profile ? (
        <div>
          <h2>{profile.name}</h2>
          <p><b>Email:</b> {profile.email}</p>
          <p><b>Education:</b> {profile.education}</p>

          <h3>Skills</h3>
          <ul>
            {profile.skills.map((s) => (
              <li key={s.id}>{s.name} ({s.level})</li>
            ))}
          </ul>

          <h3>Projects</h3>
          <ul>
            {profile.projects.map((p) => (
              <li key={p.id}>
                <b>{p.title}</b> — {p.description} (<a href={p.link} target="_blank" rel="noreferrer">View</a>)
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading profile...</p>
      )}
    </div>
  );
}

export default App;

