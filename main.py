#!/usr/bin/env python3
import requests  # to make requests to spotify api
import os  # for os.getenv
import webbrowser  # to open authorization page
import shutil  # to save image stream to file
import ctypes  # to apply wallpaper on windows
import time  # for sleep
import subprocess  # to set wallpaper on linux
import sys  # to check current operating system
import dotenv # to load spotify client id and secret
from PIL import Image # to resize image


dotenv.load_dotenv()


SPOTIFY_GET_CURRENT_TRACK_URL: str = 'https://api.spotify.com/v1/me/player/currently-playing'
SPOTIFY_GET_AUTHORIZATION_CODE_URL: str = 'https://accounts.spotify.com/authorize'
SPOTIFY_GET_ACCESS_TOKEN_URL: str = 'https://accounts.spotify.com/api/token'
SPOTIFY_CLIENT_ID: str = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET: str = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI: str = 'http://localhost:8888/callback/'
OUTPUT_FILE: str = 'wallpaper.jpg'
CACHE_ACCESS_TOKEN: bool = False # if you get an error: access token is expired you need to delete CACHE_ACCESS_TOKEN_FILE_PATH and rerun to retrieve a new valid access token
CACHE_ACCESS_TOKEN_FILE_PATH: str = '.access_token'
REFRESH_TIME: int = 0.1  # in seconds
SCREEN_SIZE: tuple = (1920, 1080)
LINUX_SET_WALLPAPER_CMD: list = ['feh', '--bg-scale'] # we assume that the image path is the last thing we need to pass the cmd


# author: imdadahad@github.com
def get_current_track(access_token: str) -> dict:
    response: requests.Response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    json_resp: any = response.json()

    track_id: str = json_resp['item']['id']
    track_name: str = json_resp['item']['name']
    artists: [str] = [artist for artist in json_resp['item']['artists']]
    link: str = json_resp['item']['external_urls']['spotify']
    artist_names: str = ', '.join([artist['name'] for artist in artists])
    image: str = json_resp['item']['album']['images'][0]['url']

    current_track_info: dict = {
        'id': track_id,
        'track_name': track_name,
        'artists': artist_names,
        'link': link,
        'image': image
    }

    return current_track_info


def get_authorization_code() -> str:
    response: requests.Response = requests.get(f'{SPOTIFY_GET_AUTHORIZATION_CODE_URL}?client_id={SPOTIFY_CLIENT_ID}&response_type=code&scope=user-read-currently-playing&redirect_uri={SPOTIFY_REDIRECT_URI}')
    print('get_authorization_code response:', response.text)

    auth_url: str = response.url
    webbrowser.open(auth_url)

    redirected_url: str = input('Enter the redirected url (its fine if it says localhost failed to connect): ')
    authorization_code: str = redirected_url.split('=')[1]

    return authorization_code


def get_access_token(authorization_code: str) -> str:
    response: requests.Response = requests.post(
        SPOTIFY_GET_ACCESS_TOKEN_URL,
        {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        })
    print('get_access_token response:', response.text)

    return response.json()['access_token']


def download_image(url: str, output_file: str) -> None:
    response: requests.Response = requests.get(url, stream=True)

    with open(output_file, 'wb') as f:
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, f)


def set_windows_wallpaper(image_absolute_path: str) -> None:
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_absolute_path, 3)


def set_linux_wallpaper(image_absolute_path: str) -> None:
    subprocess.run(LINUX_SET_WALLPAPER_CMD.append(image_absolute_path))


def get_absolute_path_of_script_directory_file(cwd_file_path: str) -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), cwd_file_path)


def set_wallpaper(absolute_file_path: str) -> None:
    if sys.platform == "linux" or sys.platform == "linux2":
        set_linux_wallpaper(absolute_file_path)
    elif sys.platform == "win32":
        set_windows_wallpaper(absolute_file_path)
    elif sys.platform == "darwin":
        # too broke to have a mac :'(
        pass


def get_cache_or_fetch_and_cache_access_token(cache_file_path: str) -> str:
    token: str = ''

    if os.path.isfile(cache_file_path) and CACHE_ACCESS_TOKEN:
        with open(cache_file_path, 'r') as f:
            token = f.read()
    else:
        token = get_access_token(get_authorization_code())
        with open(cache_file_path, 'w') as f:
            f.write(token)

    return token


def resize_image(size: tuple, image_path: str) -> None:
    img = Image.open(image_path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    img.save(image_path)


def download_resize_and_set_wallpaper(image_url: str, size: tuple, output_file: str) -> None:
    download_image(image_url, output_file)
    resize_image(size, output_file)
    set_wallpaper(output_file)


def main() -> None:
    token: str = get_cache_or_fetch_and_cache_access_token(CACHE_ACCESS_TOKEN_FILE_PATH)
    output_file: str = get_absolute_path_of_script_directory_file(OUTPUT_FILE)

    track: dict = get_current_track(token)
    print(f"current song: {track['track_name']}")
    download_resize_and_set_wallpaper(track['image'], SCREEN_SIZE, output_file)

    while True:
        new_track: dict = get_current_track(token)

        if track['id'] != new_track['id']:
            track = new_track
            print(f"current song: {track['track_name']}")
            download_resize_and_set_wallpaper(track['image'], SCREEN_SIZE, output_file)

        time.sleep(REFRESH_TIME)


if __name__ == '__main__':
    main()
