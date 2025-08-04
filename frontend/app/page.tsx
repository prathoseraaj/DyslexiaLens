import Image from "next/image";
import React from "react";

const page = () => {
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
        <div className="flex items-center m-10 mt-20 flex-col gap-1">
          <h1 className="font-bold text-4xl font-serif">
            DyslexiaLens - Text Simplifier
          </h1>
          <p className="text-[12px] ">
            Paste or types your text below to simplify it for easier reading.
          </p>

          <div className="mt-15">
            <textarea className="border border-gray-300 outline-0 resize-none rounded-[10px] w-[500px] h-[40vh] p-3" placeholder="Enter the text Here" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default page;
