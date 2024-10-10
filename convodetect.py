import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure Google Generative AI API key
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)

# Define the model configuration
generation_config = {
    "temperature": 0.7,
    #"top_p": 0.96,
    "top_k": 40,
    "max_output_tokens": 100,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
    system_instruction="you are a scam conversation detector you analyse text and detect if its a scam ..only return your output as numbers 1 is max , 0 is min , u can also give like 0.8 , 0.9 based on ur predictions. but only give single digit output.",

)

@app.route('/image', methods=['POST'])
def detect_text_from_image():
    image_url = request.json.get('image_url')
    api_key_vision = os.getenv('VISION_API_KEY')  # Add your Vision API key here

    # URL for the Vision API
    url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key_vision}'

    # Create the request payload for text detection
    payload = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": image_url
                    }
                },
                "features": [
                    {
                        "type": "TEXT_DETECTION"
                    }
                ]
            }
        ]
    }

    # Send the request to Vision API
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        texts = response.json()['responses'][0]['textAnnotations']
       # print(texts)
        if texts:
            full_text = texts[0]['description']
            print(full_text)
            # Send detected text to Gemini AI for analysis
            chat_session = model.start_chat(history=[
                
               {
      "role": "user",
      "parts": [
        "\n\nI’m from PayPal. We’ve detected suspicious activity on your account. Please provide your login details so we can secure it.\n\nI didn’t notice anything! My email is user@example.com, and my password is password123.\n\nThank you, we’ll secure your account immediately.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1",
      ],
    },
    {
      "role": "user",
      "parts": [
        "This is your cable provider. We’ve detected illegal streaming activity from your account. To avoid legal action, you need to pay a $200 fine immediately.\n\nI didn’t stream anything illegally! How do I pay?\n\nI’ll send you the payment link. Once it’s paid, we’ll clear your account.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "1",
      ],
    },
    
     # Placeholder for model response
            ])
            gemini_response = chat_session.send_message(full_text)
            return jsonify({"detected_text": full_text, "scam_score": gemini_response.text})
        else:
            return jsonify({"error": "No text detected."}), 400
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == "__main__":
    app.run(debug=True,port=3123)
