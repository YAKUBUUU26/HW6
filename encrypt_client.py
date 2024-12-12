from cryptography.fernet import Fernet

# Replace this key with the key received from the /get_key endpoint
key = 'IJ-lCg5DE59yIRX4rfvuaXb6HGwOWGtGlxeWFMYyroQ='
cipher_suite = Fernet(key)

# Encrypt the message
message = ("English texts for beginners to practice reading and comprehension ")
encrypted_message = cipher_suite.encrypt(message.encode())

# Print the encrypted message in bytes
print(encrypted_message)
