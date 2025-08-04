import Image from "next/image";
import React from "react";

const page = () => {
  return (
    <div className="w-full h-[100vh] m-0 p-0">
      <nav className="h-[7vh] flex justify-cente items-center ml-2">
        <div className="flex flex-row gap-2">
          <Image src='/svgviewer-output.svg' alt="logo" width={15} height={15} />
          <h1 className="text-1xl font-bold">DyslexiaLens</h1>
        </div>
      </nav>
      <hr className="text-gray-300" />

    </div>
  );
};

export default page;
