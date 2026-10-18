import requests

base = "http://localhost:8080/ping"

print(requests.get(base, headers={"X-Request-ID": "abc123"}).json())
print(requests.get(base).json())

codes = [requests.get(base, headers={"X-Client-Id": "bob"}).status_code for _ in range(13)]
print(codes)   # expect eight 200s, then five 429s

print(requests.get(base, headers={"X-Client-Id": "alice"}).status_code)  # 200