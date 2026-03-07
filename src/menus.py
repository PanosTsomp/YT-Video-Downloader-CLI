from pick import pick

def show_startup_menu():
    title = "Please Choose An Option:"
    options = [
        "Menu",
        "Options",
        "About us",
        "Exit"
    ]
    option, _ = pick(options, title)
    return option

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
    option, _ = pick(options, title)
    return option

def show_audio_format_menu():
    title = "What type of file format do you want the Audio to be?"
    options = ["mp3", "opus", "m4a", "wav", "best"]
    option, _ = pick(options, title)
    return option

def show_audio_quality_menu():
    title = "What audio quality (bitrate) do you want? (Higher is better, but larger file)"
    options = ["best", "256k", "192k", "128k", "64k"]
    option, _ = pick(options, title)
    return option

def show_video_quality_menu():
    title = "What video quality do you want?"
    options = ["best", "1080p", "720p", "480p", "360p", "240p", "worst"]
    option, _ = pick(options, title)
    return option

def show_video_format_menu():
    title = "What video format do you want?"
    options = ["mp4", "webm", "mkv", "best"]
    option, _ = pick(options, title)
    return option

def show_subtitle_lang_menu():
    title = "What subtitle language do you want? (or 'all' for all available)"
    options = ["en", "es", "fr", "de", "all", "none"]
    option, _ = pick(options, title)
    return option

def show_embed_options_menu():
    title = "Embed options: Choose what to embed (multi-select if needed, but for simplicity, pick one or none)"
    options = ["Embed subtitles", "Embed thumbnail", "Embed metadata", "None"]
    option, _ = pick(options, title)
    return option

def show_sponsorblock_menu():
    title = "Remove sponsors/ads using SponsorBlock?"
    options = ["Yes (remove all)", "No"]
    option, _ = pick(options, title)
    return option == "Yes (remove all)"

def get_url_input():
    return input("Enter URL (or 'ytsearch:query' for search): ")

def get_output_path_input(default_path="downloads"):
    path = input(f"Enter download path (default: {default_path}): ").strip()
    return path if path else default_path

def get_batch_file_input():
    return input("Enter path to batch file (list of URLs): ")