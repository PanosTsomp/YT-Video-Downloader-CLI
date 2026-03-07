from pick import pick

PICK_INDICATOR = "=>"


def _pick_option(options, title):
    option, _ = pick(options, title, indicator=PICK_INDICATOR)
    return option


def show_startup_menu():
    title = "Please Choose An Option:"
    options = [
        "Menu",
        "Options",
        "About us",
        "Exit"
    ]
    return _pick_option(options, title)

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

def show_source_menu():
    title = "Where is this URL from?"
    options = [
        "YouTube",
        "YouTube Music"
    ]
    return _pick_option(options, title)

def show_audio_format_menu():
    title = "What type of file format do you want the Audio to be?"
    options = ["mp3", "opus", "m4a", "wav", "best"]
    return _pick_option(options, title)

def show_audio_quality_menu():
    title = "What audio quality (bitrate) do you want? (Higher is better, but larger file)"
    options = ["best", "256k", "192k", "128k", "64k"]
    return _pick_option(options, title)

def show_video_quality_menu():
    title = "What video quality do you want?"
    options = ["best", "1080p", "720p", "480p", "360p", "240p", "worst"]
    return _pick_option(options, title)

def show_video_format_menu():
    title = "What video format do you want?"
    options = ["mp4", "webm", "mkv", "best"]
    return _pick_option(options, title)

def show_subtitle_lang_menu():
    title = "What subtitle language do you want? (or 'all' for all available)"
    options = ["en", "es", "fr", "de", "all", "none"]
    return _pick_option(options, title)

def show_embed_options_menu():
    title = "Embed options: Choose what to embed (pick one or none)"
    options = ["Embed subtitles", "Embed thumbnail", "Embed metadata", "None"]
    return _pick_option(options, title)

def show_sponsorblock_menu():
    title = "Remove sponsors/ads using SponsorBlock?"
    options = ["Yes (remove all)", "No"]
    option = _pick_option(options, title)
    return option == "Yes (remove all)"

def get_url_input(source=None):
    if source == "YouTube":
        return input("Enter YouTube URL (or 'ytsearch:query' for search): ")
    if source == "YouTube Music":
        return input("Enter YouTube Music URL (or 'ytsearch:query' for search): ")
    return input("Enter URL (or 'ytsearch:query' for search): ")

def get_output_path_input(default_path="downloads"):
    path = input(f"Enter download path (default: {default_path}): ").strip()
    return path if path else default_path

def get_batch_file_input():
    return input("Enter path to batch file (list of URLs): ")
