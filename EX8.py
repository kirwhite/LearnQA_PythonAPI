import requests
import time

response_1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")

parsed_response_text = response_1.json()
needed_token = parsed_response_text["token"]
print(parsed_response_text["seconds"])
response_2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": needed_token})
print(response_2.text)

time.sleep(parsed_response_text["seconds"] + 1)

response_3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": needed_token})
parsed_response_text_2 = response_3.json
print(response_3.text)