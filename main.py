#He wrote the script: @trmob on the test server
import os
import random
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid, FloodWait, PhoneNumberInvalid, AuthKeyUnregistered

api_id = 2040
api_hash = "b18441a1ff607e10a989891a5462e627" #A universal pair of APIs, you don't have to change it, because it's not necessary

def generate_numbers():
    prefixes = ['+99966', '+99922']
    numbers = []

    for _ in range(80000):
        prefix = random.choice(prefixes)
        middle_digit = str(random.randint(1, 4))
        number = f'{prefix}{middle_digit}{random.randint(1000, 9999)}'
        numbers.append(number)

    return numbers

phone_numbers = generate_numbers()

for phone_number in phone_numbers:
    session_name = f"session_{phone_number}.session"

    client = None
    try:
        print(f'\033[94m[HTB] Generated number: {phone_number}\033[0m')
        client = Client(session_name, api_id, api_hash, test_mode=True)
        client.connect()
        sent_code_info = client.send_code(phone_number)

        middle_digit = phone_number[6]
        phone_code = middle_digit * 5

        print(f'\033[94m[HTB] Attempting login with code: {phone_code}\033[0m')
        client.sign_in(phone_number, sent_code_info.phone_code_hash, phone_code)

        user = client.get_me()
        print(f'\033[94m[HTB] Successfully logged in as {user.first_name} {user.last_name or ""} ID: {user.id}\033[0m')

        # Example 1: Sending a message to a user by ID
        # client.send_message("user_id", "Hello!")

        # Example 2: Joining a channel by username or invite link
        # client.join_chat("channel_username_or_invite_link")

        # Example 3: Viewing a specific post in a channel
        # message = client.get_messages("channel_username_or_id", message_id)
        # print(message.text)

        # Example 4: Reacting to a message in a chat or channel
        # client.send_reaction("channel_username_or_id", message_id, "👍")

    except Exception as e:
        print(f'\033[91m[HTB] Error for number {phone_number}: {e}, skipping...\033[0m')

    finally:
        if client is not None:
            client.disconnect()
        
        session_files = [f for f in os.listdir() if f.endswith('.session')]
        for session_file in session_files:
            os.remove(session_file)
            print(f'\033[94m[HTB] Session file {session_file} deleted.\033[0m')

print('\033[94mScript completed.\033[0m')
