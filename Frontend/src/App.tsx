import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import SeeForms from "./pages/SeeForms";
import CreateForm from "./pages/CreateForm";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/create-form" element={<CreateForm />} />
        <Route path="/see-forms" element={<SeeForms />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App