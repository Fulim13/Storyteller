import "./App.css";
import { useState, useEffect } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/test/")
      .then((res) => res.json())
      .then((data) => setData(data.data));
  });

  return (
    <div className="App">
      <header className="App-header">
        <h1>An Awesome Blog </h1>
        <h3>On Django, React, Postgres, and Docker </h3>

        <p>{data}</p>
      </header>
    </div>
  );
}

export default App;
