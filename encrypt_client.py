import subprocess

# The curl command
curl_command = [
    'curl',
    'http://127.0.0.1:5000/get_message'
]

# Run the command
result = subprocess.run(curl_command, capture_output=True, text=True)

# Print the output of the curl command
print(result.stdout)Aimport subprocess

# The curl command
curl_command = [
    'curl',
    'http://127.0.0.1:5000/get_message'
]

# Run the command
result = subprocess.run(curl_command, capture_output=True, text=True)

# Print the output of the curl command
print(result.stdout)A
