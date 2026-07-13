# Uncomment the imports below before you add the function code
import requests
import os
import json
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()


def _env_or_default(key, default):
    value = os.getenv(key, "").strip()
    if not value or value.lower().startswith("your "):
        return default
    return value


backend_url = _env_or_default("backend_url", "http://localhost:3030")
sentiment_analyzer_url = _env_or_default(
    "sentiment_analyzer_url", "http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"

    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except requests.RequestException:
        # If any error occurs
        print("Network exception occurred")
        return {}


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except requests.RequestException:
        print("Network exception occurred")
        return {}


def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Method not allowed"})

    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except (json.JSONDecodeError, requests.RequestException):
            return JsonResponse(
                {"status": 500, "message": "Error in posting review"}
            )

    return JsonResponse({"status": 403, "message": "Unauthorized"})
