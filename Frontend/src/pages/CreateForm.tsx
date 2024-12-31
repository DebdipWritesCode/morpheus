import React, { useState } from "react";
import Text from "../components/QuestionTypes/Text";
import Checkbox from "../components/QuestionTypes/Checkbox";
import Dropdown from "../components/QuestionTypes/Dropdown";
import Ranking from "../components/QuestionTypes/Ranking";
import LinearScale from "../components/QuestionTypes/LinearScale";
import DatePicker from "../components/QuestionTypes/DatePicker";
import TimePicker from "../components/QuestionTypes/TimePicker";
import FileUpload from "../components/QuestionTypes/FileUpload";
import Matrix from "../components/QuestionTypes/Matrix";
import Image from "../components/QuestionTypes/Image";
import Slider from "../components/QuestionTypes/Slider";
import Signature from "../components/QuestionTypes/Signature";
import ColorPicker from "../components/QuestionTypes/ColorPicker";
import Location from "../components/QuestionTypes/Location";
import PercentageAllocation from "../components/QuestionTypes/PercentageAllocation";

import { FaRegTrashAlt } from "react-icons/fa";
import { PiDotsSixBold } from "react-icons/pi";

interface QuestionTypes {
  text: string;
  checkbox: string;
  dropdown: string;
  ranking: string;
  linear_scale: string;
  date_picker: string;
  time_picker: string;
  file_upload: string;
  matrix: string;
  image: string;
  slider: string;
  signature: string;
  color_picker: string;
  location: string;
  percentage_allocation: string;
}

interface Question {
  id: number;
  type: keyof QuestionTypes;
  question_text: string;
  options?: {};
}

const questionComponents: { [key in keyof QuestionTypes]: React.FC } = {
  text: Text,
  checkbox: Checkbox,
  dropdown: Dropdown,
  ranking: Ranking,
  linear_scale: LinearScale,
  date_picker: DatePicker,
  time_picker: TimePicker,
  file_upload: FileUpload,
  matrix: Matrix,
  image: Image,
  slider: Slider,
  signature: Signature,
  color_picker: ColorPicker,
  location: Location,
  percentage_allocation: PercentageAllocation,
};

const CreateForm = () => {
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [selectedQuestionType, setSelectedQuestionType] =
    useState<keyof QuestionTypes>("text");
  const [questions, setQuestions] = useState<Question[]>([]);

  const handleFormTitleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormTitle(e.target.value);
  };

  const handleFormDescriptionChange = (
    e: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    setFormDescription(e.target.value);
  };

  const handleQuestionTypeChange = (
    e: React.ChangeEvent<HTMLSelectElement>
  ) => {
    setSelectedQuestionType(e.target.value as keyof QuestionTypes);
  };

  const handleCreateNewQuestion = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault();

    if (questions.length < 100) {
      setQuestions((prevQuestions) => [
        ...prevQuestions,
        {
          id: prevQuestions.length,
          type: selectedQuestionType,
          question_text: "New Question",
        },
      ]);
    } else {
      alert("You can't have more than 100 questions in a form");
    }
  };

  const handleDeleteQuestion = (
    e: React.MouseEvent<HTMLButtonElement>,
    id: number
  ) => {
    e.preventDefault();
    setQuestions((prevQuestions) =>
      prevQuestions.filter((question) => question.id !== id)
    );
  };

  return (
    <div className=" flex justify-center mt-5 py-5 px-4">
      <form className="min-w-[600px] border-t-[12px] border-blue-600 shadow-lg p-6 bg-white rounded-lg">
        <div className=" flex flex-col gap-5 mb-7">
          <input
            type="text"
            name="title"
            id="title"
            placeholder="Enter a title for your form"
            value={formTitle}
            onChange={handleFormTitleChange}
            className="outline-none border-b border-slate-400 text-3xl py-1"
          />
          <textarea
            name="description"
            id="description"
            placeholder="Enter a description"
            value={formDescription}
            onChange={handleFormDescriptionChange}
            className="outline-none border-b border-slate-400 text-lg py-1 h-10"></textarea>
        </div>
        <div className="flex gap-6 items-center mb-5">
          <select
            name="question-type"
            id="question-type"
            value={selectedQuestionType}
            onChange={handleQuestionTypeChange}
            className="outline-none border-2 py-2 text-md font-semibold border-slate-300 rounded-md px-1">
            {Object.keys(questionComponents).map((type) => (
              <option key={type} value={type}>
                {type.replace("_", " ").replace(type[0], type[0].toUpperCase())}
              </option>
            ))}
          </select>
          <button
            className=" p-2 bg-blue-500 hover:bg-blue-700 text-white rounded-xl"
            onClick={handleCreateNewQuestion}>
            Create New Question
          </button>
        </div>
        <div>
          {questions.map((question) => {
            const QuestionComponent = questionComponents[question.type];
            return (
              <div
                key={question.id}
                className="relative px-4 pb-3 pt-5 border mt-8 rounded-lg">
                <QuestionComponent key={question.id} />
                <div className=" absolute -top-5 -left-10 flex gap-4 items-center translate-x-1/2 w-full">
                  <button
                    className="border rounded-full p-2 bg-white hover:bg-red-500 hover:text-white"
                    onClick={(e) => handleDeleteQuestion(e, question.id)}>
                    <FaRegTrashAlt size={22} />
                  </button>
                  <button
                    className="border rounded-full p-2 bg-white hover:bg-slate-200"
                    onClick={(e) => handleDeleteQuestion(e, question.id)}>
                    <PiDotsSixBold size={22} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </form>
    </div>
  );
};

export default CreateForm;
