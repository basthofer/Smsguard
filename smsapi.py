from fastapi import FastAPI, HTTPException, Request
import google.generativeai as genai
import requests
import os

app = FastAPI()

example_chats = '''
User: "Your account has been locked. Click here to verify your details [fake link]."
1.0

User: "Congratulations! You’ve won $1,000,000. Claim your prize now by clicking this link [fake link]."
1.0

User: "Your package is delayed. Update your delivery preferences here [fake link]."
0.9

User: "Your device has been infected with malware. Contact us immediately at [fake number] to resolve the issue."
1.0

User: "You have unpaid taxes. Pay immediately or face legal action. Call [fake number] now."
1.0

User: "You’ve been pre-approved for a $10,000 loan. Apply now with no credit check at [fake link]."
0.9

User: "Your account has been compromised. Verify your password by following this link [fake link]."
1.0

User: "Your subscription is about to expire. Renew now to avoid service interruption [fake link]."
0.9

User: "You are eligible for a COVID-19 grant. Click here to claim [fake link]."
1.0

User: "Hey, I miss you! Let’s catch up [fake link]."
0.9
'''

# Set up Google Gemini API key
#genai.configure(api_key="YOUR_GEMINI_KEY")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a SMS checker AI that reads the message and predicts if it's a scam. Return a number between 0 and 1, where 0 is not a scam and 1 means 100% sure. Consider suspicious links, special characters, etc.",
)


@app.post("/check_sms/")
async def check_sms(request: Request):
    try:
        body = await request.json()
        sms_message = body.get("message", "")
        
        # Start a chat session and send the message for evaluation
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(sms_message)
        
        # Parse and return the scam probability
        scam_probability = response.text.strip()
        return {"scam_probability": scam_probability}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


headers = {
    'accept': 'application/json',
    'accept-ianguage': 'en-US,en;q=0.9,es;q=0.8',
    'accept-language': 'en-US,en;q=0.9,en-IN;q=0.8',
    'content-type': 'application/json',
    'priority': 'u=1, i',
    'referer': 'https://www.virustotal.com/',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'x-app-version': 'v1x301x1',
    'x-tool': 'vt-ui-main',
    'x-vt-anti-abuse-header': 'youarepwned',
}

@app.get("/search")
async def search_virustotal(query: str, limit: int = 20):
    params = {
        'limit': str(limit),
        'relationships[comment]': 'author,item',
        'query': query,
    }

    # Make the request to VirusTotal
    response = requests.get('https://www.virustotal.com/ui/search', params=params, headers=headers)
    
    # Return the JSON response
    return response.json()