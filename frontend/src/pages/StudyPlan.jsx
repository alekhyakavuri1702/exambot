import { useState } from "react";

function StudyPlan() {
  const [plan, setPlan] = useState([]);

  const generatePlan = async () => {
    try {
      const response = await fetch("http://localhost:8000/generate-plan", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic: "Mathematics" }), // Example topic
      });
  
      if (!response.ok) {
        throw new Error("Failed to generate study plan");
      }
  
      const data = await response.json();
      setPlan(data.plan); // Assuming the API returns `{ "plan": ["Step 1", "Step 2"] }`
    } catch (error) {
      console.error("Error:", error);
    }
  };  
  return (
    <div>
      <h1>Personalized Study Plan</h1>
      <button onClick={generatePlan}>Generate Plan</button>
      <ul>
        {plan.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default StudyPlan;
