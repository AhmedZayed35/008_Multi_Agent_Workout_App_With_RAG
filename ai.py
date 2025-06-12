import requests
import json

# API endpoint URLs for different flows
ask_ai_url = "http://127.0.0.1:7860/api/v1/run/171f7d3e-ab0a-40e3-bcd0-af03ff762073"  # Endpoint for AskAI flow
calculate_macros_url = "http://127.0.0.1:7860/api/v1/run/107904f5-1cb2-493e-a133-42b1947a8634"  # Endpoint for CalculateMacros flow

def ask_ai(question, user_profile):
    """
    Sends a question and user profile to the AskAI API endpoint.

    Args:
        question (str): The user's question.
        user_profile (dict): The user's profile information.

    Returns:
        str: The AI's response as a string.
    """
    payload = {
        "tweaks": {
            "TextInput-nu5nz": {  # Field for user question
                "input_value": question
            },
            "TextInput-F3NqN": {  # Field for user profile (as JSON string)
                "input_value": json.dumps(user_profile)
            }
        }
    }
    return send_request(payload, ask_ai_url)

def calculate_macros(goals, user_profile):
    """
    Sends user goals and profile to the CalculateMacros API endpoint.

    Args:
        goals (list of str): List of user goals.
        user_profile (dict): The user's profile information.

    Returns:
        str: The calculated macros as a string.
    """
    payload = {
        "tweaks": {
            "TextInput-bmWAZ": {  # Field for user goals (comma-separated)
                "input_value": ', '.join(goals)
            },
            "TextInput-SttRa": {  # Field for user profile (as JSON string)
                "input_value": json.dumps(user_profile)
            }
        }
    }
    return send_request(payload, calculate_macros_url)

def send_request(payload, url):
    """
    Sends a POST request to the specified API endpoint with the given payload.

    Args:
        payload (dict): The request payload to send.
        url (str): The API endpoint URL.

    Returns:
        str: The extracted text result from the API response.

    """
    response = requests.post(url, json=payload)
    # Parse the response and extract the result text
    result = response.json()["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
    return result