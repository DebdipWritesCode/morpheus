import { jwtDecode } from "jwt-decode";
import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import FallBack from "../components/FallBack";
import Loading from "../components/Loading";

interface DecodedToken {
  id: string;
  email: string;
  role: string;
  username: string;
}

interface Form {
  id: number;
  title: string;
  description: string;
  created_by: number;
  created_at: string;
}

interface ResponseData {
  message: string;
  forms: Form[];
}

const SeeForms = () => {
  const [decodedToken, setDecodedToken] = useState<DecodedToken | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [forms, setForms] = useState<Form[]>([]);

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const userDetails = jwtDecode<DecodedToken>(token);
        const tc = {
          id: userDetails.id,
          email: userDetails.email,
          role: userDetails.role,
          username: userDetails.username,
        };
        setDecodedToken(tc);
      } catch (err) {
        console.error("Invalid token", err);
      } finally {
        setIsLoading(false);
      }
    }
  }, []);

  useEffect(() => {
    if (decodedToken && decodedToken.role === "admin") {
      const fetchForms = async () => {
        setIsLoading(true);
        try {
          const response = await axios.get<ResponseData>(
            `${import.meta.env.VITE_BACKEND_URL}/api/get-forms?user_id=${
              decodedToken.id
            }`
          );
          setForms(response.data.forms);
        } catch (error) {
          console.error("Error fetching forms:", error);
        } finally {
          setIsLoading(false);
        }
      };

      fetchForms();
    }
  }, [decodedToken]);

  if (!decodedToken) {
    return (
      <FallBack
        linkTo="login"
        linkText="Login"
        headingText="You must login first"
      />
    );
  }

  if (decodedToken.role !== "admin") {
    return (
      <FallBack
        linkTo="login"
        linkText="Login as admin"
        headingText="You must be an admin to see this page"
      />
    );
  }

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="flex h-screen justify-center mt-20">
      <div className="min-w-[600px]">
        <h1 className="text-5xl font-bold text-blue-600 mb-2">
          Hello {decodedToken.username}
        </h1>
        <h3 className=" text-xl font-semibold text-blue-700 mb-10">
          {decodedToken.email}
        </h3>
        <div className="">
          <Link to="/create-form">
            <button className=" bg-blue-600 text-white rounded-md px-3 py-2 text-lg hover:bg-blue-800">
              Create new
            </button>
          </Link>
        </div>
        <div className="flex flex-col gap-5 mt-8">
          {forms.length !== 0 ? (
            <div className="flex flex-col gap-4">
              {forms.map((form) => (
                <Link to={`/form/${form.id}`} key={form.id}>
                  <div className="border border-gray-300 py-2 px-3 rounded-md flex justify-between items-center">
                    <h2 className="text-lg font-semibold text-blue-500">
                      {form.title.length > 15
                        ? `${form.title.slice(0, 15)}...`
                        : form.title}
                    </h2>
                    <p className="text-sm text-gray-700">
                      {form.description.length > 25
                        ? `${form.description.slice(0, 25)}...`
                        : form.description}
                    </p>
                    <p className="text-md text-blue-900">{form.created_at}</p>
                  </div>
                </Link>
              ))}
            </div>
          ) : (
            <div>
              <h3 className="text-xl font-semibold text-blue-500">
                You haven't created any forms yet!
              </h3>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SeeForms;
