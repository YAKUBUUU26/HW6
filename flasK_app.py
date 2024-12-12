import subprocess

# The curl command
curl_command = [
    'curl',
    '-X', 'DELETE',
    '-H', 'API-Key: 114eb4ec8b02db3469ba560ca1528f0e',
    'http://127.0.0.1:3000/users/Efremenkods@mail.ru'
]

# Run the command
result = subprocess.run(curl_command, capture_output=True, text=True)

# Print the output of the curl command
print(result.stdout)
