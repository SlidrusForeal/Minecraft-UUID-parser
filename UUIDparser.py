import requests
import time

def get_minecraft_uuid(nickname):
    try:
        # Construct the API URL
        url = f"https://api.mojang.com/users/profiles/minecraft/{nickname}"

        # Send a GET request to the Mojang API
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            # Extract the UUID from the response data
            uuid = data.get('id')
            if uuid:
                return uuid
            else:
                raise ValueError("UUID not found in the response.")
        elif response.status_code == 204:
            raise ValueError("No content found for the given nickname.")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors
        print(f"An error occurred while trying to fetch the UUID: {e}")
    except ValueError as e:
        # Handle cases where the UUID is not found or other value errors
        print(e)
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")


def save_uuids_to_file(nicknames_uuids, filename="uuids.txt"):
    try:
        with open(filename, 'w') as file:
            for nickname, uuid in nicknames_uuids.items():
                content = f'{{ name: "{nickname}", uuid: "{uuid}" }},\n'
                file.write(content)
        print(f"UUIDs saved to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")


def process_blacklist(file_path):
    nicknames_uuids = {}
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            position, nickname = line.strip().split(' ', 1)
            print(f"Processing {nickname}...")
            uuid = get_minecraft_uuid(nickname)
            if uuid:
                nicknames_uuids[nickname] = uuid
                time.sleep(3)

        save_uuids_to_file(nicknames_uuids)
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")


# Path to the blacklist.txt file
blacklist_file_path = ('blacklist.txt')

# Process the blacklist
process_blacklist(blacklist_file_path)
