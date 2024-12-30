import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div className="flex flex-col gap-10 items-center justify-center h-screen">
      <h1 className="text-5xl font-bold text-red-600">404 Page Not Found</h1>
      <Link to={"/"}>
        <button className="px-3 py-2 bg-slate-100 font-semibold text-red-600 border border-red-600 rounded-3xl hover:bg-slate-200">
          Go back to home
        </button>
      </Link>
    </div>
  );
};

export default NotFound;
