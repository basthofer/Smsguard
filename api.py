import re
import requests
from fastapi import FastAPI, Request
import chardet
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

def contains_url(text: str) -> bool:
    # Updated URL regex to handle URL detection without capturing extra characters
    url_regex = r"http[s]?://[a-zA-Z0-9./?=_-]+"
    return bool(re.search(url_regex, text))


def check_url_redirect(url: str) -> (str, str):
    try:
        # Send a HEAD request to check the URL
        response = requests.head(url, allow_redirects=True)

        # Check if the response status code indicates redirection
        if response.history:  # If there is any redirection
            # Get the final redirected URL
            redirected_url = response.url
            print(f"URL was redirected to: {redirected_url}")

            # Parse the URL and extract the domain
            parsed_url = urlparse(redirected_url)
            domain = f"{parsed_url.scheme}://{parsed_url.netloc}"  # Construct the domain
            print(f"Extracted domain: {domain}")
            return redirected_url, domain
        else:
            print("URL is not redirected.")
            return url, url  # Return the original URL as both if not redirected

    except requests.RequestException as e:
        print(f"Error checking URL: {e}")
        return url, url


def clean_text(text: str) -> str:
    # Replace non-breaking spaces and any special characters
    return text.replace("\xa0", " ").strip()

def detect_encoding(body: bytes) -> str:
    # Detect the encoding of the incoming byte stream
    result = chardet.detect(body)
    encoding = result['encoding']
    print(f"Detected encoding: {encoding}")
    return encoding

def make_request_sms(message: str):
    response = requests.post("http://localhost:8000/check_sms/", json={"message": message})
    return response.json()

def make_request_search(url: str):
    search_params = {"query": url, "limit": 20}
    response = requests.get("http://localhost:8000/search", params=search_params)
    search_data = response.json()
    last_analysis_stats = search_data["data"][0]["attributes"]["last_analysis_stats"] if "data" in search_data else None
    return last_analysis_stats

def make_request_browser(url: str):
    response = requests.post("http://localhost:3000/check-website", json={"url": url})
    return response.json()

def calculate_final_score(scam_probability: float, search_response: dict, browser_response: dict) -> float:
    # Determine if search_response has malicious content
    malicious = search_response.get("malicious", 0) if search_response else 0
    browser_score = float(browser_response.get("score", 0)) if browser_response else 0

    # Maximize all the risk values (scam_probability, malicious, browser score)
    if malicious > 0:
        final_score = 1.0
    else:
        final_score = max(scam_probability, browser_score)

    return final_score

@app.post("/api")
async def analyze_text(request: Request):
    try:
        # Detect encoding and decode the body accordingly
        body = await request.body()
        encoding = detect_encoding(body)
        message = body.decode(encoding)
    except UnicodeDecodeError:
        # If decoding fails, handle the error and try ignoring invalid bytes
        message = body.decode("utf-8", errors="ignore")
        print("Warning: Some characters could not be decoded.")

    # Clean the message from non-breaking spaces and any special characters
    message = clean_text(message)
    print(f"Cleaned message: {message}")

    if contains_url(message):
        # Extract only the first occurrence of a URL using refined regex
        url_match = re.search(r"http[s]?://[a-zA-Z0-9./?=_-]+", message)
        url = url_match.group(0) if url_match else ""
        print(f"Extracted URL: {url}")
        full_url, domain = check_url_redirect(url)
        print(full_url,domain)
        # Use ThreadPoolExecutor to make requests concurrently
        with ThreadPoolExecutor() as executor:
            future_sms = executor.submit(make_request_sms, message)
            future_search = executor.submit(make_request_search, domain)
            future_browser = executor.submit(make_request_browser, full_url)

            sms_response = future_sms.result()
            search_response = future_search.result()
            browser_response = future_browser.result()

        # Extract the scam_probability from the sms response
        scam_probability = float(sms_response.get("scam_probability", 0))

        # Calculate the final score
        final_score = calculate_final_score(scam_probability, search_response, browser_response)

        return {
            "sms_response": sms_response,
            "search_response": search_response,
            "browser_response": browser_response,
            "final_score": final_score
        }
    else:
        # If no URL, make only the SMS request and return null for the others
        sms_response = make_request_sms(message)
        scam_probability = float(sms_response.get("scam_probability", 0))

        # No URL, so search_response and browser_response are null
        final_score = calculate_final_score(scam_probability, None, None)

        return {
            "sms_response": sms_response,
            "search_response": None,
            "browser_response": None,
            "final_score": final_score
        }
