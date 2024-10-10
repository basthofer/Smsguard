# Scambuster by scamjammers

Scambuster is a tool that uses AI to detect and analyze potential SMS scams. It leverages both Node.js and Python to provide a comprehensive solution for SMS analysis. This is the backend server/ API of scambuster tool.

## Prerequisites

- Node.js (version 20 or above)
- Python (version 3.10 or above)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/basthofer/scambuster.git
   cd scambuster
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Install Python dependencies:
   ```
   pip install fastapi google-generativeai requests uvicorn
   ```

## Configuration

Create a `.env` file in the root directory and add your API keys:

```
GEMINI_API_KEY=your_google_api_key
VISION_API_KEY=your_vision_key
```

## Running the Application

You need to run three separate components:

1. Node.js Browser API:
   ```
   node browserapi.js
   ```
   This will run on `http://localhost:3000`

2. Python SMS API:
   ```
   uvicorn smsapi:app
   ```
   This will run on `http://localhost:8000`

3. Main API:
   ```
   uvicorn api:app --port 5000
   ```
   This will run on `http://localhost:5000`
4. Image Detection API:
   ```
   python3 convodetect.py
   ```
   This will run on `http://localhost:3123`
## Usage

To analyze an SMS message, send a POST request to the main API:

```bash
curl -X POST "http://localhost:5000/api" \
     -H "Content-Type: application/json" \
     -d '{"message": "Deal of the Day! Your NIRO loan of Rs. 336000 is ready! Tap into the best EMIs now. Claim your funds here- http://f49.bz/mKfvum - Finbud"}'
```
To analyze an Image , send a POST request to the convodetect/image API:

```bash
curl -X POST "http://localhost:3123/image" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://i.postimg.cc/k506WBfT/amy-is-offering-me-a-job-as-a-music-promotion-optimizer-i-v0-amklp5ya6ntd1.webp"}'
```
## Dependencies

### Node.js Dependencies

```json
{
  "dependencies": {
    "@google/generative-ai": "^0.20.0",
    "axios": "^1.7.7",
    "dotenv": "^16.4.5",
    "express": "^4.21.0",
    "puppeteer": "^23.4.1",
    "puppeteer-extra": "^3.3.6",
    "puppeteer-extra-plugin-stealth": "^2.11.2"
  }
}
```

### Python Dependencies

- FastAPI
- google-generative-ai
- requests
- uvicorn
- flask
- flask_cors


