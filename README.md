# Scambuster by Scamjammers🚫

Scambuster is a cutting-edge tool that uses AI to detect and analyze potential SMS scams. This backend server/API leverages both Node.js and Python to provide a comprehensive solution for SMS analysis, including the ability to detect scams through both text messages and message screenshots.

## ✨ Features

- **AI-Powered Detection**: 🤖 Utilize advanced algorithms to identify and flag scam messages effectively.
- **Screenshot Analysis**: 🖼️ Leverage Optical Character Recognition (OCR) to detect scams from SMS screenshots.
- **Real-Time Analysis**: ⏱️ Receive immediate feedback on the legitimacy of messages.

## 📋 Prerequisites

Ensure you have the following before getting started:

- **Node.js**: Version 20 or above
- **Python**: Version 3.10 or above

## 🚀 Installation

Follow these steps to install Scambuster:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/basthofer/scambuster.git
   cd scambuster
   ```

2. **Install Node.js Dependencies**:
   ```bash
   npm install
   ```

3. **Install Python Dependencies**:
   ```bash
   pip install fastapi google-generativeai requests uvicorn flask flask_cors
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory and add your API keys:

```
GEMINI_API_KEY=your_google_api_key
VISION_API_KEY=your_vision_key
```

## 🚦 Running the Application

Run the following components in separate terminal windows:

1. **Node.js Browser API**:
   ```bash
   node browserapi.js
   ```
   - Accessible at `http://localhost:3000`

2. **Python SMS API**:
   ```bash
   uvicorn smsapi:app
   ```
   - Accessible at `http://localhost:8000`

3. **Main API**:
   ```bash
   uvicorn api:app --port 5000
   ```
   - Accessible at `http://localhost:5000`
   
4. **Image Detection API**:
   ```bash
   python3 convodetect.py
   ```
   - Accessible at `http://localhost:3123`

## 📚 Usage

To analyze an SMS message, send a POST request to the main API:

```bash
curl -X POST "http://localhost:5000/api" \
     -H "Content-Type: application/json" \
     -d '{"message": "Deal of the Day! Your NIRO loan of Rs. 336000 is ready! Tap into the best EMIs now. Claim your funds here- http://f49.bz/mKfvum - Finbud"}'
```

To analyze an image, send a POST request to the Image Detection API:

```bash
curl -X POST "http://localhost:3123/image" \
     -H "Content-Type: application/json" \
     -d '{"image_url": "https://i.postimg.cc/k506WBfT/amy-is-offering-me-a-job-as-a-music-promotion-optimizer-i-v0-amklp5ya6ntd1.webp"}'
```

## 📦 Dependencies

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

## 🤝 Contributing

We welcome contributions to enhance Scambuster! Please feel free to open an issue or submit a pull request with your suggestions and improvements.
