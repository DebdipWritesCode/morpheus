import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="flex justify-center items-center h-screen ">
      <div className="flex flex-col items-center justify-center gap-10">
        <h1 className="text-7xl font-bold text-blue-600">
          Welcome to Form Builder
        </h1>
        <Link to="/login">
          <button className="bg-slate-100 border border-blue-600 text-blue-600 rounded-xl px-4 py-2 font-semibold text-xl hover:bg-slate-200">
            Create your form
          </button>
        </Link>
      </div>
    </div>
  );
};

export default Home;
