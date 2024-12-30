import React from "react";

interface LoadingProps {
  message?: string;
}

const Loading: React.FC<LoadingProps> = ({ message }) => {
  return (
    <div className="flex flex-col gap-10 h-screen items-center justify-center">
      <h1 className="text-5xl font-bold text-blue-600">Loading...</h1>
      <p className="text-xl font-semibold text-blue-400">
        {
          message || "Please wait while we load the data"
        }
      </p>
    </div>
  );
};

export default Loading;
