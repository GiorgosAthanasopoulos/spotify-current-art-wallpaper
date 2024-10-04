# spotify-current-album-art-set-wallpaper

Set current album art from spotify as wallpaper (linux and windows). If you like this crap that I call software please leave it a star :).

## Dependencies

- Linux
  - `feh` (in `main.py` change `set_linux_wallpaper` to a custom command if you dont have `feh`/dont want to use it)

## Warning

Scuffed script meant for my personal use!!! It may brick your toaster, or expose your anime wallpaper directory! Use at your own risk!

## Limitation

Image max dimensions(from spotify api): 640x300 and it scales to fit so the quality is not the best...

## Usage

- `pip install -r requirements.txt`
- `python main.py`
- A browser window should open prompting you to login, if you havent already:
  - Like the cli stdout says, copy the localhost link (its ok that is says connection refused),
  - and paste it in stdin (the terminal basically).
- Profit. Every REFRESH_TIME ms you should see the wallpaper update depending on your currently playing song.

## Shameless Promotion xD

While you re at it, might as well check [my 80s/90s disco dance playlist](https://open.spotify.com/playlist/3KUhPod9UN9BU47X1wiIR1?si=7bbda8f326ec4332), while debugging this crap that I wrote :D. Cheers!
