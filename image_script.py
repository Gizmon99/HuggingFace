import requests
from datetime import datetime
from time import sleep

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer here_your_authorisation_token_for_HuggingFace"}

with open("trends.txt", "r") as file:
    lines = [line.strip() + ", cat" for line in file.readlines()]


def make_request(payload, max_retries=5, base_delay=10):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                return response

            if response.status_code in [503, 429]:
                wait_time = base_delay * attempt
                print(f"Retry {attempt}/{max_retries} - Waiting {wait_time}s... (Error {response.status_code})")
                sleep(wait_time)
            elif response.status_code in [500]:
                wait_time = 60
                print(f"Retry {attempt}/{max_retries} - Waiting {wait_time}s... (Error {response.status_code})")
                sleep(wait_time)
            else:
                print(f"Error {response.status_code}: {response.text}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e} - Retrying {attempt}/{max_retries}")
            sleep(base_delay * attempt)

    return None


for idx, line in enumerate(lines):
    for i in range(5):
        payload = {
            "inputs": line,
            "parameters": {
                "max_sequence_length": 256,
                "num_inference_steps": 4,
                "guidance_scale": 0.0,
                "seed": int(datetime.now().timestamp())
            },
            "options": {
                "wait_for_model": True
            }
        }

        response = make_request(payload)

        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                with open(f"{idx}_{line[:len(line)-5]}_{i}.png", "wb") as f:
                    f.write(response.content)
                print(f"Image saved as '{idx}_{line[:len(line)-5]}_{i}.png'")
            else:
                print("Response is not an image:", response.text)
        else:
            print(f"Error {response.status_code}: {response.text}")

        sleep(21)
