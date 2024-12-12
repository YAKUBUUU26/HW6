import subprocess

# The curl command
curl_command = [
    'curl',
    '-X', 'PUT',
    '-H', 'API-Key: ff3e854bf3cf59db197d9aec9dfcd644',
    '-H', 'Content-Type: application/json',
    '-d', '{"age": "25"}',
    'http://127.0.0.1:5000/users/deenyacoubou@gmail.com'
]

# Run the command
result = subprocess.run(curl_command, capture_output=True, text=True)

# Print the output of the curl command
print(result.stdout)

