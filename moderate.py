import requests


def moderate(text):
    """
    Get the text content moderated using ContentGuard.AI
    :param text:
    :return:
    """
    api_url = "http://3.26.146.235:5000/api/v0/moderate"
    # api_url = "http://127.0.0.1:5000/api/v0/moderate"
    payload = {"text": text}
    print(payload)
    print("Executing")
    response = requests.post(api_url, json=payload)
    result = response.json()
    return result


# unit test
if __name__ == "__main__":
    print(moderate("This could be a hate speech, "
                   "but let us see what the ContentGuardAI reports"))
    print(moderate("This vase is fucking beautiful!"))
