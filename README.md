# YouTube Video Downloader CLI

A terminal-based YouTube and YouTube Music downloader built on top of `yt-dlp`.

The app gives you an interactive menu for:
- downloading audio or video
- downloading playlists
- downloading subtitles, thumbnails, chapters, and metadata
- embedding subtitles/thumbnail/metadata into media files
- removing sponsored segments with SponsorBlock
- updating `yt-dlp` from inside the app

It also accepts plain search text, so you can type a song/video name instead of only full URLs.

## Run With Scripts (No UV Needed)

These scripts are for users who only have Python and want the easiest setup.

### Requirements
- Python `3.13` (project target)
- Internet access for dependency installation
- `ffmpeg` installed on your system (needed for conversions/embedding/merging)

### First-time setup
```bash
./setup.sh
```

### Run the app
```bash
./run.sh
```

`run.sh` will auto-run setup if `.venv` does not exist yet.

## Run With UV

If you use `uv`, you can run the project directly without the helper scripts.

### Requirements
- `uv`
- Python `3.13`
- `ffmpeg`

### Install dependencies
```bash
uv sync
```

### Run
```bash
uv run python main.py
```

## Features

- Source selection:
  - YouTube
  - YouTube Music

- Core download modes:
  - Download Audio
  - Download Video
  - Download Audio and Video
  - Download Playlist only Audio
  - Download Playlist only Video
  - Download Playlist Video and Audio

- Extra content modes:
  - Download Subtitles (language-specific or `all`)
  - Download Thumbnail
  - Download Chapters (split chapters)
  - Download Metadata (`.info.json` + description)

- Embed options:
  - None
  - Embed subtitles
  - Embed thumbnail
  - Embed metadata
  - Embed everything

- Quality and format controls:
  - Audio formats: `mp3`, `opus`, `m4a`, `wav`, `auto`
  - Audio bitrate: `auto`, `256k`, `192k`, `128k`, `64k`
  - Video formats: `mp4`, `webm`, `mkv`, `auto`
  - Video quality: `auto`, `1080p`, `720p`, `480p`, `360p`, `240p`, `worst`

- Search input:
  - Plain text is automatically converted to `ytsearch:` / `ytmusicsearch:`

- SponsorBlock:
  - Optional automatic removal of sponsor/ads segments

- Batch mode:
  - Download from a text file (one URL/query per line)
  - Comment lines starting with `#` are ignored

- In-app updater:
  - `Update yt-dlp` tries multiple methods for compatibility:
    - `uv pip install --upgrade yt-dlp`
    - `python -m pip install --upgrade yt-dlp`
    - `yt-dlp -U`

## Scripts

### `setup.sh`
Bootstraps a local virtual environment and installs required packages:
- creates `.venv` (if missing)
- upgrades `pip`
- installs/updates `pick` and `yt-dlp`

Usage:
```bash
./setup.sh
```

### `run.sh`
Runs the app from the local virtual environment:
- checks `.venv`
- runs `setup.sh` automatically if needed
- launches `main.py`

Usage:
```bash
./run.sh
```

Pass-through args are supported:
```bash
./run.sh --help
```

## Project Structure

```text
main.py                # CLI entrypoint
src/app.py             # Main program flow
src/menus.py           # Interactive terminal menus
src/downloader.py      # yt-dlp option builder + download execution
src/config.py          # Loads/saves .yvd-config.json
setup.sh               # Non-UV setup helper
run.sh                 # Non-UV run helper
```

## Notes

- The app stores config in `.yvd-config.json` (when used).
- Some YouTube extractions may require a JavaScript runtime depending on `yt-dlp` changes.
- If subtitle downloads hit rate limits (`HTTP 429`), retry later or avoid `all` subtitle languages.



YouTube Video Downloader CLI
Author: PANAGIOTIS ILIAS TSOMPANOGLOU 
GitHub:  https://github.com/PanosTsomp
License: MIT
