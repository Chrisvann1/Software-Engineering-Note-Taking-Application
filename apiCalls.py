import requests

print("\n")

def testCall():
    response = requests.get("https://httpbin.org/get")
    print(response.headers)

testCall()

print("\n")