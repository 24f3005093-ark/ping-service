import requests

base = "http://127.0.0.1:8080/ping"

print(requests.get(base, headers={"X-Request-ID": "abc123"}).json())
print(requests.get(base).json())

codes = [requests.get(base, headers={"X-Client-Id": "charli"}).status_code for _ in range(13)]
print(codes)

print(requests.get(base, headers={"X-Client-Id": "alice"}).status_code)
