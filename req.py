import requests

# GET request to retrieve all users
response = requests.get('http://127.0.0.1:5000/users')

# Print the response data
print(response.json())