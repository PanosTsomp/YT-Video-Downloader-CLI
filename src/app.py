from __future__ import annotations

from src.config import AppConfig, load_config
from src.downloader import (
    build_ydl_opts,
    perform_batch_download,
    perform_download,
    update_yt_dlp,
)
from src.menus import (
    get_batch_file_input,
    get_url_input,
    show_audio_format_menu,
    show_audio_quality_menu,
    show_embed_options_menu,
    show_main_menu,
    show_source_menu,
    show_sponsorblock_menu,
    show_startup_menu,
    show_subtitle_lang_menu,
    show_video_format_menu,
    show_video_quality_menu,
)

AUDIO_ONLY_CHOICES = {"Download Audio", "Download Playlist only Audio"}
VIDEO_ONLY_CHOICES = {"Download Video", "Download Playlist only Video"}
VIDEO_WITH_AUDIO_CHOICES = {
    "Download Audio and Video",
    "Download Playlist Video and Audio",
}
VIDEO_MENU_CHOICES = VIDEO_ONLY_CHOICES | VIDEO_WITH_AUDIO_CHOICES | {"Download Chapters"}
EMBED_MENU_CHOICES = (
    AUDIO_ONLY_CHOICES
    | VIDEO_ONLY_CHOICES
    | VIDEO_WITH_AUDIO_CHOICES
    | {"Download Subtitles", "Download Chapters"}
)
SPONSORBLOCK_MENU_CHOICES = AUDIO_ONLY_CHOICES | VIDEO_ONLY_CHOICES | VIDEO_WITH_AUDIO_CHOICES


def _show_about() -> None:
    print("Personal downloader powered by yt-dlp (YouTube + YouTube Music).")
    print("Made by Panagiotis Ilias Tsompanoglou :: https://github.com/PanosTsomp")
    input("Press Enter to return to the startup menu...")


def _handle_options(_config: AppConfig) -> None:
    print("\nOptions are not implemented yet.")
    input("Press Enter to return to the startup menu...")


def _build_download_inputs(menu_choice: str, config: AppConfig) -> dict[str, object]:
    source = None
    url = None
    batch_file = None

    if menu_choice == "Batch Download from File":
        batch_file = get_batch_file_input().strip()
    else:
        source = show_source_menu()
        url = get_url_input(source).strip()

    audio_format = None
    audio_quality = None
    if menu_choice in AUDIO_ONLY_CHOICES:
        audio_format = show_audio_format_menu() or config.default_audio_format
        audio_quality = show_audio_quality_menu() or config.default_audio_quality

    video_format = None
    video_quality = None
    if menu_choice in VIDEO_MENU_CHOICES:
        video_format = show_video_format_menu() or config.default_video_format
        video_quality = show_video_quality_menu() or config.default_video_quality

    subtitle_lang = None
    if menu_choice == "Download Subtitles":
        subtitle_lang = show_subtitle_lang_menu()

    embed_option = None
    if menu_choice in EMBED_MENU_CHOICES:
        embed_option = show_embed_options_menu()

    sponsorblock = False
    if menu_choice in SPONSORBLOCK_MENU_CHOICES:
        sponsorblock = show_sponsorblock_menu()

    return {
        "source": source,
        "url": url,
        "batch_file": batch_file,
        "audio_format": audio_format,
        "audio_quality": audio_quality,
        "video_format": video_format,
        "video_quality": video_quality,
        "subtitle_lang": subtitle_lang,
        "embed_option": embed_option,
        "sponsorblock": sponsorblock,
    }


def _run_download_menu(config: AppConfig) -> None:
    menu_choice = show_main_menu()
    if menu_choice == "Update yt-dlp":
        update_yt_dlp()
        return

    inputs = _build_download_inputs(menu_choice, config)
    if menu_choice == "Download Subtitles" and inputs["subtitle_lang"] == "none":
        print("Subtitles download cancelled: no language selected.")
        return

    opts = build_ydl_opts(
        menu_choice=menu_choice,
        source=inputs["source"],
        output_dir=config.output_dir,
        audio_format=inputs["audio_format"],
        audio_quality=inputs["audio_quality"],
        video_format=inputs["video_format"],
        video_quality=inputs["video_quality"],
        subtitle_lang=inputs["subtitle_lang"],
        embed_option=inputs["embed_option"],
        sponsorblock=bool(inputs["sponsorblock"]),
    )

    if menu_choice == "Batch Download from File":
        batch_file = str(inputs["batch_file"] or "").strip()
        if not batch_file:
            print("Batch download cancelled: empty file path.")
            return
        perform_batch_download(batch_file, opts)
        return

    url = str(inputs["url"] or "").strip()
    if not url:
        print("Download cancelled: empty URL.")
        return
    perform_download(url, opts)


def run_cli() -> None:
    config = load_config()
    print("\nWelcome to YouTube Video Downloader CLI! (YVD-CLI)\n")

    while True:
        startup_choice = show_startup_menu()

        if startup_choice == "Exit":
            break
        if startup_choice == "Menu":
            _run_download_menu(config)
        elif startup_choice == "Options":
            _handle_options(config)
        elif startup_choice == "About us":
            _show_about()

    print("Goodbye!")
