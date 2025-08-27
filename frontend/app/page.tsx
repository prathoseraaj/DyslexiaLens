"use client";
import axios from "axios";
import Image from "next/image";
import React, { useState } from "react";

const page = () => {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState("");
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);

  console.log(text);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    const file = files[0];
    if (!file) return;

    setUploadedFile(file);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setText(response.data.text);
    } catch (error) {
      console.error(error);
      setText("Error extracting text from file");
    } finally {
      setLoading(false);
    }
  };

  const handleSimply = async () => {
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/simplif", {
        text,
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      setResult("Error simplifying text");
    } finally {
      setLoading(false);
    }
  };

const LoadingSpinner = () => (
    <div className="flex items-center justify-center min-h-[50vh]">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-gray-300 border-t-green-600 rounded-full animate-spin mx-auto mb-4"></div>
        
        <p className="text-lg text-gray-700">
          Wait a minute, it is undergoing the simplification process...
        </p>
      </div>
    </div>
  );


  return (
    <div className="w-full h-[100vh] m-0 p-0">
      <nav className="h-[7vh] flex  items-center ml-2">
        <div className="flex flex-row gap-2">
          <Image
            src="/svgviewer-output.svg"
            alt="logo"
            width={15}
            height={15}
          />
          <h1 className="text-1xl font-bold">DyslexiaLens</h1>
        </div>
      </nav>
      <hr className="text-gray-300" />

      <div className="h-[93h]">
        {loading ? (
          <LoadingSpinner />
        ) : !result ? (
          <div className="flex items-center m-10 mt-20 flex-col gap-1">
            <h1 className="font-bold text-4xl font-serif">
              DyslexiaLens - Text Simplifier
            </h1>
            <p className="text-[12px] ">
              Paste or types your text below to simplify it for easier reading.
            </p>

            <div className="mt-15">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Upload PDF or Image (PNG, JPG, JPEG)
                </label>
                <input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg"
                  onChange={handleFileUpload}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-green-50 file:text-green-700 hover:file:bg-green-100"
                />
              </div>
              
              <textarea
                className="border border-gray-300 outline-0 resize-none rounded-[10px] w-[500px] h-[40vh] p-3"
                placeholder="Enter the text Here or upload a PDF/Image file"
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            </div>

            <button
              className="bg-green-600 mt-4 px-3 py-1 rounded text-white cursor-pointer hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              onClick={handleSimply}
              disabled={loading || !text.trim()}
            >
              {loading ? "Simplifying..." : "Simplify Text"}
            </button>
          </div>
        ) : (
          <div className="flex flex-col items-center m-10 mt-10 mb-10 max-w-4xl mx-auto">
            <div className="w-full max-w-3xl bg-yellow-50 border-2 border-yellow-200 rounded-xl p-8 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-6 text-center">
                Simplified Text
              </h3>
              <div
                className="text-gray-800 leading-loose text-lg font-medium tracking-wide"
                style={{
                  fontFamily: "Arial, sans-serif",
                  lineHeight: "2.2",
                  letterSpacing: "0.05em",
                  wordSpacing: "0.3em",
                }}
              >
                {result.split("\n").map((paragraph, index) => (
                  <p key={index} className="mb-6 text-left">
                    {paragraph}
                  </p>
                ))}
              </div>
            </div>

            <div className="mt-8">
              <button
                className="bg-green-600 mt-4 px-3 py-1 rounded text-white cursor-pointer hover:bg-green-700 transition-colors"
                onClick={() => {
                  setText("");
                  setResult("");
                  setUploadedFile(null);
                }}
              >
                Simplify Another Text
              </button>
            </div>

            <div className="w-full max-w-3xl mt-8  mb-10 bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-bold text-blue-800 mb-3">
                Reading Tips
              </h3>
              <ul className="text-blue-700 text-base leading-relaxed space-y-2">
                <li>Take breaks between paragraphs if needed</li>
                <li>Read at your own comfortable pace</li>
                <li>Use a pointer to follow along if helpful</li>
                <li>Focus on understanding rather than speed</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default page;