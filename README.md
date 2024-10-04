# spotify-current-art-wallpaper

Set current album art from spotify as wallpaper (linux and windows). If you like this crap that I call software please leave it a star :).

## Dependencies

- Linux
  - `feh` (in `main.py` change `set_linux_wallpaper` to a custom command if you dont have `feh`/dont want to use it),
  - `python`/`pip` (🤓well akshually `python3` but `python` should most of the times alias to `python3` in any recent distros).
- Windows
  - `python`/`pip`.

## Warning

Scuffed script meant for my personal use!!! It may brick your toaster, or expose your anime wallpaper directory! Use at your own risk!

## Limitation

Image max dimensions(from spotify api): 640x300 and it scales to fit so the quality is not the best...

## Usage

- See [Getting client credentials from spotify](#getting-client-credentials-from-spotify),
- `pip install -r requirements.txt`,
- `python main.py`,
- A browser window should open prompting you to login, if you havent already:
  - Like the cli stdout says, copy the localhost link (its ok that is says connection refused),
  - and paste it in stdin (the terminal basically).
- Profit. Every REFRESH_TIME ms you should see the wallpaper update depending on your currently playing song.

## Getting client credentials from spotify

- Go to [spotify developer dashboard](https://developer.spotify.com/dashboard) (by logging in, if you havent already),
- Click purple `create app` button,
- Give it a simple name, a description and add a redirect uri of `http://localhost:8888/callback/` (even slash is important for the uri!),
- Agree to their terms and click `Save`,
- Navigate to the settings page (top right - `Settings button`) of the project and in the `Basic information` tab copy `client id` and `client secret` (in order for the secret to appear click the purple `view secret` link),
- Create a `.env` file in the root of the cloned spotify-current-art-wallpaper repo and write in this format:
```bash
SPOTIFY_CLIENT_ID=PASTE_YOUR_SPOTIFY_CLIENT_ID_HERE
SPOTIFY_CLIENT_SECRET=PASTE_YOUR_SPOTIFY_CLIENT_SECRET_HERE
```

## Shameless Promotion xD

While you re at it, might as well check [my 80s/90s disco dance playlist](https://open.spotify.com/playlist/3KUhPod9UN9BU47X1wiIR1?si=7bbda8f326ec4332), while debugging this crap that I wrote :D. Cheers!
