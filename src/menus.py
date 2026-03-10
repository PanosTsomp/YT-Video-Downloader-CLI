"""
Command-line menu system for the YouTube Video Downloader.

This module contains all user interface prompts and menus,
including the startup menu, download menu, and option
selection prompts. It collects user input and returns
structured choices to the main application.

YouTube Video Downloader CLI
Author: PANAGIOTIS ILIAS TSOMPANOGLOU 
GitHub:  https://github.com/PanosTsomp
License: MIT
"""
from pick import pick

PICK_INDICATOR = "=>"

# When you get the options we call the pick method so the user can choose
def _pick_option(options, title):
    option, _ = pick(options, title, indicator=PICK_INDICATOR)
    return option

# Returns the chosen option from the user 
def show_startup_menu():
    title = "Please Choose An Option:"
    options = [
        "Menu",
        "Options",
        "About us",
        "Exit"
    ]
    return _pick_option(options, title)

# Shows the main menu of the app
def show_main_menu():
    title = "What Do You Want To Do?"
    options = [
        "Download Audio",
        "Download Video",
        "Download Audio and Video",
        "Download Subtitles",
        "Download Thumbnail",
        "Download Playlist only Audio",
        "Download Playlist only Video",
        "Download Playlist Video and Audio",
        "Download Chapters",
        "Download Metadata",
        "Batch Download from File",
        "Update yt-dlp"
    ]
    return _pick_option(options, title)

# Tell me the source of the URL
def show_source_menu():
    title = "Where is this URL from?"
    options = [
        "YouTube",
        "YouTube Music"
    ]
    return _pick_option(options, title)

# Tell me the audio format you want
def show_audio_format_menu():
    title = "What type of file format do you want the Audio to be?"
    options = ["mp3", "opus", "m4a", "wav", "best"]
    return _pick_option(options, title)

# Tell me the Audio Quality you want
def show_audio_quality_menu():
    title = "What audio quality (bitrate) do you want? (Higher is better, but larger file)"
    options = ["best", "256k", "192k", "128k", "64k"]
    return _pick_option(options, title)

# Tell me the Video Quality you want
def show_video_quality_menu():
    title = "What video quality do you want?"
    options = ["best", "1080p", "720p", "480p", "360p", "240p", "worst"]
    return _pick_option(options, title)

# Tell me the video Format you want
def show_video_format_menu():
    title = "What video format do you want?"
    options = ["mp4", "webm", "mkv", "best"]
    return _pick_option(options, title)

# Tell me if you want to install subs
def show_subtitle_lang_menu():
    title = "What subtitle language do you want? (or 'all' for all available)"
    options = ["en", "es", "fr", "de", "all", "none"]
    return _pick_option(options, title)

# Tell me what you want to Embed
def show_embed_options_menu():
    title = "Embed options: Choose what to embed (pick one or none)"
    options = ["None", "Embed everything", "Embed subtitles", "Embed thumbnail", "Embed metadata"]
    return _pick_option(options, title)

# Tell me if you want to remove the Sponsored parts 
def show_sponsorblock_menu():
    title = "Remove sponsors/ads using SponsorBlock?"
    options = ["Yes (remove all)", "No"]
    option = _pick_option(options, title)
    return option == "Yes (remove all)"

# Enter the url OR the name
def get_url_input(source=None):
    def _normalize_url_or_search(value):
        query = value.strip()
        if not query:
            return query

        lowered = query.lower()
        if lowered.startswith("ytsearch:") or lowered.startswith("ytmusicsearch:"):
            return query

        if (
            "://" in query
            or lowered.startswith("www.")
            or lowered.startswith("youtube.com/")
            or lowered.startswith("m.youtube.com/")
            or lowered.startswith("music.youtube.com/")
            or lowered.startswith("youtu.be/")
        ):
            return query

        if source == "YouTube Music":
            return f"ytmusicsearch:{query}"
        return f"ytsearch:{query}"

    if source == "YouTube":
        return _normalize_url_or_search(input("Enter YouTube URL or video name: "))
    if source == "YouTube Music":
        return _normalize_url_or_search(input("Enter YouTube Music URL or song name: "))
    return _normalize_url_or_search(input("Enter URL or name: "))

# Choose the output destination
def get_output_path_input(default_path="downloads"):
    path = input(f"Enter download path (default: {default_path}): ").strip()
    return path if path else default_path

# Tell me if you want a batch file download
def get_batch_file_input():
    return input("Enter path to batch file (list of URLs): ")
