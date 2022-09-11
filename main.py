import requests

nfl_request = requests.get("https://www.nfl.com/schedules/2022/reg1/")

print(nfl_request.content)