import React from "react";
import { Link } from "react-router-dom";

interface FallBackProps {
  linkTo: string;
  linkText: string;
  headingText: string;
}

const FallBack: React.FC<FallBackProps> = ({
  linkTo,
  linkText,
  headingText,
}) => {
  return (
    <div className="flex flex-col gap-10 items-center justify-center h-screen">
      <h1 className="text-5xl font-bold text-red-600">{headingText}</h1>
      <Link to={`/${linkTo}`}>
        <button className="px-3 py-2 bg-slate-100 font-semibold text-red-600 border border-red-600 rounded-3xl hover:bg-slate-200">
          {linkText}
        </button>
      </Link>
    </div>
  );
};

export default FallBack;
