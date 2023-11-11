import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

#1
response = requests.get(url=url)
print(response.status_code, response.text)
#2
response_2 = requests.head(url=url, data={"method" : "HEAD"})
print(response_2.status_code, response_2.text)
#3
response_3 = requests.get(url=url, params={"method" : "GET"})
print(response_3.status_code, response_3.text)

#4
listOfValues = {
    "GET",
    "POST",
    "PUT",
    "DELETE"
}

for i in listOfValues:
    response_4 = requests.get(url=url, params={"method": i})
    print(f"GET +", i, "value in params is", response_4.status_code, response_4.text)

for i in listOfValues:
    response_4 = requests.post(url=url, data={"method": i})
    print(f"POST +", i, "value in params is", response_4.status_code, response_4.text)

for i in listOfValues:
    response_4 = requests.put(url=url, data={"method": i})
    print(f"PUT +", i, "value in params is", response_4.status_code, response_4.text)

for i in listOfValues:
    response_4 = requests.delete(url=url, data={"method": i})
    print(f"DELETE +", i, "value in params is", response_4.status_code, response_4.text)