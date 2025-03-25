import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import StudyPlan from "./pages/StudyPlan";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/study-plan" element={<StudyPlan />} />
      </Routes>
    </Router>
  );
}
export default App;
