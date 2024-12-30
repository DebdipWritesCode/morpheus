import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import React, { useState } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const signupSchema = z.object({
  email: z.string().email("Invalid email address"),
  username: z.string().min(3, "Username is too short"),
  password: z
    .string()
    .min(6, "Password must be at least 6 characters")
    .regex(
      /^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])/,
      "Password must include uppercase, lowercase, number, and special character"
    ),
});

interface SignupError {
  response?: {
    data?: {
      error: string;
    };
  };
  message: string;
}

interface SignupResponse {
  data: {
    message: string;
  };
}

const Signup = () => {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    role: "admin",
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const result = signupSchema.safeParse(formData);

    if (!result.success) {
      const validationErrors: Record<string, string> = {};
      result.error.errors.forEach((error) => {
        if (error.path[0]) {
          validationErrors[error.path[0] as string] = error.message;
        }
      });
      setErrors(validationErrors);
      return;
    }

    setErrors({});

    try {
      setIsSubmitting(true);
      const response = await axios.post<SignupResponse>(
        `${import.meta.env.VITE_BACKEND_URL}/api/auth/signup`,
        {
          email: formData.email,
          username: formData.username,
          password: formData.password,
          role: formData.role,
        }
      );

      console.log("Signup successful", response.data);
      toast.success("Signup successful! Redirecting to login...", {
        onClose: () => navigate("/login"),
      });
    } catch (err) {
      const error = err as SignupError;
      let errorMessage = error.response?.data?.error || "Something went wrong";

      if (
        errorMessage.includes("duplicate key value violates unique constraint")
      ) {
        errorMessage = "Username already exists";
      }
      toast.error(errorMessage);
      setErrors({
        server: errorMessage,
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <div className=" p-6 shadow-xl bg-slate-50 max-w-[500px] rounded-md flex flex-col gap-6">
        <h1 className="font-bold text-4xl text-blue-600 text-center">
          Create your admin account
        </h1>
        <form onSubmit={handleSubmit}>
          <div className="flex flex-col gap-2 text-md font-semibold">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder="potato@tomato.com"
              className=" outline-none rounded-md px-2 py-1"
              onChange={handleChange}
              value={formData.email}
            />
            {errors.email && <p className="text-red-500">{errors.email}</p>}
            <label className="mt-4" htmlFor="username">
              Username
            </label>
            <input
              type="text"
              name="username"
              id="username"
              placeholder="Potato"
              className=" outline-none rounded-md px-2 py-1 "
              onChange={handleChange}
              value={formData.username}
            />
            {errors.username && (
              <p className="text-red-500">{errors.username}</p>
            )}
            <label className="mt-4" htmlFor="password">
              Password
            </label>
            <input
              type="password"
              name="password"
              id="password"
              placeholder="Potato123$"
              className=" outline-none rounded-md px-2 py-1 "
              onChange={handleChange}
              value={formData.password}
            />
            {errors.password && (
              <p className="text-red-500">{errors.password}</p>
            )}
            <div className=" flex justify-between items-center gap-4 mt-5">
              <button
                type="submit"
                className="bg-blue-600 text-white rounded-xl px-3 py-2 hover:bg-blue-900">
                Signup
              </button>
              <Link to={"/login"}>
                <button className="text-blue-950">
                  Already have an admin account?
                </button>
              </Link>
            </div>
          </div>
        </form>
      </div>
      {isSubmitting && (
        <div className=" w-screen h-screen overflow-hidden absolute z-20 bg-slate-500 opacity-65"></div>
      )}
      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
};

export default Signup;
