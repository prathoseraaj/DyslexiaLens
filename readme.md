# DyslexiaLens

DyslexiaLens is an AI-powered web application designed to make text more accessible for individuals with dyslexia. Utilizing advanced Natural Language Processing (NLP) techniques and computer vision, DyslexiaLens transforms and adapts text to improve readability and comprehension.

## Features

- **Text Simplification**: Converts complex text to dyslexia-friendly formats using advanced NLP
- **Multi-format Support**: Processes text from various sources including PDFs and images
- **OCR Integration**: Extracts text from images using Tesseract OCR and OpenCV
- **Readability Analysis**: Provides comprehensive readability scoring and assessment
- **AI Enhancement**: Uses Google's Gemini AI for intelligent text refinement
- **User-friendly Interface**: Clean, accessible web interface built with Next.js
- **File Upload Support**: Upload PDFs and images for text extraction and simplification

## Technology Stack

### Frontend
- **Next.js** - React framework for the user interface
- **React** - Component-based UI library
- **Tailwind CSS** - Utility-first CSS framework

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python** - Core backend language
- **Natural Language Processing**:
  - **NLTK** - Natural language toolkit for text processing
  - **spaCy** - Advanced NLP library for linguistic analysis
  - **TextStat** - Library for readability statistics
- **Computer Vision & OCR**:
  - **OpenCV** - Computer vision library for image processing
  - **Tesseract OCR** - Optical character recognition engine
  - **Pillow (PIL)** - Python imaging library
- **AI Integration**:
  - **Google Generative AI (Gemini)** - Advanced language model for text enhancement
- **File Processing**:
  - **PDFPlumber** - PDF text extraction
  - **python-multipart** - File upload handling
- **Text Processing**:
  - **ftfy** - Text encoding and cleanup
  - **regex (re)** - Pattern matching and text manipulation

## Project Structure

```
DyslexiaLens/
├── frontend/          # Next.js application
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
├── backend/           # Python FastAPI application
│   ├── main.py       # Main application file
│   ├── requirements.txt
│   └── ...
└── README.md
```

## Getting Started

### Prerequisites

#### Frontend
- Node.js (version 14 or higher recommended)
- npm, yarn, pnpm, or bun

#### Backend
- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR installed on your system

### Installation

#### 1. Clone the repository
```bash
git clone https://github.com/prathoseraaj/DyslexiaLens.git
cd DyslexiaLens
```

#### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

**Required Python packages:**
- fastapi
- uvicorn
- python-multipart
- pydantic
- ftfy
- nltk
- spacy
- textstat
- google-generativeai
- python-dotenv
- pytesseract
- pillow
- pdfplumber
- opencv-python

**Additional Setup:**
1. Install Tesseract OCR on your system
2. Download spaCy English model: `python -m spacy download en_core_web_sm`
3. Create a `.env` file with your Gemini API key: `gemini_api_key=your_api_key_here`

#### 3. Frontend Setup
```bash
cd frontend
npm install
# or yarn install / pnpm install / bun install
```

### Running the Application

#### Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at [http://localhost:8000](http://localhost:8000).

#### Start the Frontend Development Server
```bash
cd frontend
npm run dev
# or yarn dev / pnpm dev / bun dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## API Endpoints

- **POST /simplif** - Simplify text input
- **POST /upload** - Upload and process PDF/image files
- **GET /** - Health check endpoint

## Usage

1. **Text Input**: Paste or type text directly into the application
2. **File Upload**: Upload PDF files or images containing text
3. **Processing**: The application will:
   - Extract text (if from file)
   - Analyze readability and complexity
   - Apply lexical simplification
   - Break down long sentences
   - Enhance with AI-powered refinement
4. **Results**: View the dyslexia-friendly adapted text with readability improvements

## Key Features Explained

### Text Processing Pipeline
1. **Text Cleaning**: Fixes encoding issues and normalizes formatting
2. **Segmentation**: Breaks text into paragraphs, sentences, and tokens
3. **Readability Analysis**: Calculates various readability scores (Flesch-Kincaid, SMOG, etc.)
4. **Issue Detection**: Identifies long sentences, passive voice, and ambiguous structures
5. **Lexical Simplification**: Replaces complex words with simpler alternatives
6. **Sentence Splitting**: Breaks long sentences into shorter, clearer ones
7. **AI Enhancement**: Uses Gemini AI for final refinement while preserving meaning

### Supported File Formats
- **PDF**: Extracts text using PDFPlumber
- **Images** (PNG, JPEG, JPG): Uses Tesseract OCR with OpenCV preprocessing

## License

This project is licensed under the [Apache License 2.0](./LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or suggestions, please open an [issue](https://github.com/prathoseraaj/DyslexiaLens/issues) or contact the maintainer.

---

**DyslexiaLens** – Smart AI that reshapes text for dyslexic readers using advanced NLP and computer vision.