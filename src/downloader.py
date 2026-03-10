"""
Download engine for the YouTube Video Downloader.

This module builds yt-dlp option dictionaries based on user
choices and executes downloads using the yt-dlp library.
It also supports batch downloads and updating yt-dlp.

YouTube Video Downloader CLI
Author: PANAGIOTIS ILIAS TSOMPANOGLOU 
GitHub:  https://github.com/PanosTsomp
License: MIT
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yt_dlp
from yt_dlp.utils import DownloadError

AUDIO_ONLY_CHOICES = {
    "Download Audio", 
    "Download Playlist only Audio"
}
VIDEO_ONLY_CHOICES = {
    "Download Video", 
    "Download Playlist only Video"
}
VIDEO_WITH_AUDIO_CHOICES = {
    "Download Audio and Video",
    "Download Playlist Video and Audio",
}
PLAYLIST_CHOICES = {
    "Download Playlist only Audio",
    "Download Playlist only Video",
    "Download Playlist Video and Audio",
}
ELEMENT_DOWNLOAD_CHOICES = {"Download Subtitles", 
    "Download Thumbnail", 
    "Download Metadata"
}
EMBED_ELEMENT_CHOICES = {
    "Embed subtitles",
    "Embed thumbnail",
    "Embed metadata",
    "Embed everything",
}


def _quality_kbps(value: str | None) -> str | None:
    if not value or value == "best":
        return None
    if value.endswith("k") and value[:-1].isdigit():
        return value[:-1]
    return None


def _video_format_selector(
    video_format: str | None,
    video_quality: str | None,
    with_audio: bool,
) -> str:
    ext = None if not video_format or video_format == "best" else video_format

    if video_quality == "worst":
        return "worstvideo+worstaudio/worst" if with_audio else "worstvideo/worst"

    height = None
    if video_quality and video_quality.endswith("p") and video_quality[:-1].isdigit():
        height = video_quality[:-1]

    video_filters = ""
    if ext:
        video_filters += f"[ext={ext}]"
    if height:
        video_filters += f"[height<={height}]"

    best_video = f"bestvideo{video_filters}"
    if with_audio:
        fallback_best = f"best[height<={height}]" if height else "best"
        return f"{best_video}+bestaudio/{fallback_best}"

    fallback_video = f"bestvideo[height<={height}]" if height else "bestvideo"
    fallback_best = f"best[height<={height}]" if height else "best"
    return f"{best_video}/{fallback_video}/{fallback_best}"


def _source_prefix(source: str | None) -> str:
    if source == "YouTube":
        return "YouTube/"
    if source == "YouTube Music":
        return "YouTube Music/"
    return ""


def _outtmpl_for_download(source: str | None, put_in_elements_folder: bool) -> str:
    source_prefix = _source_prefix(source)
    base_name = "%(title)s [%(id)s]"
    if put_in_elements_folder:
        return f"{source_prefix}Elements/{base_name}/{base_name}.%(ext)s"
    return f"{source_prefix}{base_name}.%(ext)s"


def _subtitle_langs(subtitle_lang: str | None) -> list[str] | None:
    if not subtitle_lang or subtitle_lang == "none":
        return None
    if subtitle_lang == "all":
        return ["all"]
    return [subtitle_lang]


def _apply_embed_option(
    opts: dict[str, Any],
    embed_option: str | None,
    subtitle_lang: str | None,
) -> None:
    if embed_option == "Embed subtitles":
        langs = _subtitle_langs(subtitle_lang)
        if not langs:
            return
        opts["writesubtitles"] = True
        opts["writeautomaticsub"] = True
        opts["subtitleslangs"] = langs
        opts["embedsubtitles"] = True
    elif embed_option == "Embed thumbnail":
        opts["writethumbnail"] = True
        opts["embedthumbnail"] = True
    elif embed_option == "Embed metadata":
        opts["addmetadata"] = True
    elif embed_option == "Embed everything":
        langs = _subtitle_langs(subtitle_lang)
        if langs:
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            opts["subtitleslangs"] = langs
        opts["writethumbnail"] = True
        if langs:
            opts["embedsubtitles"] = True
        opts["embedthumbnail"] = True
        opts["addmetadata"] = True


def build_ydl_opts(
    menu_choice: str,
    source: str | None = None,
    output_dir: str = "downloads",
    audio_format: str | None = None,
    audio_quality: str | None = None,
    video_format: str | None = None,
    video_quality: str | None = None,
    subtitle_lang: str | None = None,
    embed_option: str | None = None,
    sponsorblock: bool = False,
) -> dict[str, Any]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    put_in_elements_folder = (
        menu_choice in ELEMENT_DOWNLOAD_CHOICES
        or (embed_option in EMBED_ELEMENT_CHOICES)
    )
    opts: dict[str, Any] = {
        "paths": {"home": str(output_path)},
        "outtmpl": _outtmpl_for_download(source, put_in_elements_folder),
        "noplaylist": menu_choice not in PLAYLIST_CHOICES,
    }

    if menu_choice in AUDIO_ONLY_CHOICES:
        opts["format"] = "bestaudio/best"
        if audio_format and audio_format != "best":
            postprocessor: dict[str, Any] = {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
            }
            kbps = _quality_kbps(audio_quality)
            if kbps:
                postprocessor["preferredquality"] = kbps
            opts["postprocessors"] = [postprocessor]

    elif menu_choice in VIDEO_ONLY_CHOICES:
        opts["format"] = _video_format_selector(
            video_format=video_format,
            video_quality=video_quality,
            with_audio=False,
        )

    elif menu_choice in VIDEO_WITH_AUDIO_CHOICES:
        opts["format"] = _video_format_selector(
            video_format=video_format,
            video_quality=video_quality,
            with_audio=True,
        )
        if video_format and video_format != "best":
            opts["merge_output_format"] = video_format

    elif menu_choice == "Download Subtitles":
        opts["skip_download"] = True
        opts["writesubtitles"] = True
        opts["writeautomaticsub"] = True
        if subtitle_lang and subtitle_lang != "none":
            opts["subtitleslangs"] = ["all"] if subtitle_lang == "all" else [subtitle_lang]

    elif menu_choice == "Download Thumbnail":
        opts["skip_download"] = True
        opts["writethumbnail"] = True

    elif menu_choice == "Download Chapters":
        opts["format"] = _video_format_selector(
            video_format=video_format,
            video_quality=video_quality,
            with_audio=True,
        )
        opts["split_chapters"] = True
        if video_format and video_format != "best":
            opts["merge_output_format"] = video_format

    elif menu_choice == "Download Metadata":
        opts["skip_download"] = True
        opts["writeinfojson"] = True
        opts["clean_infojson"] = True
        opts["writedescription"] = True

    elif menu_choice == "Batch Download from File":
        opts["format"] = _video_format_selector(
            video_format=video_format,
            video_quality=video_quality,
            with_audio=True,
        )
        if video_format and video_format != "best":
            opts["merge_output_format"] = video_format

    _apply_embed_option(opts, embed_option, subtitle_lang)

    if sponsorblock:
        opts["sponsorblock_remove"] = ["all"]

    return opts


def perform_download(url: str, ydl_opts: dict[str, Any]) -> None:
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except DownloadError as exc:
        print(f"Download failed: {exc}")


def perform_batch_download(batch_file: str, ydl_opts: dict[str, Any]) -> None:
    batch_path = Path(batch_file)
    if not batch_path.exists():
        print(f"Batch file not found: {batch_file}")
        return

    try:
        lines = batch_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"Failed to read batch file: {exc}")
        return

    urls = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    if not urls:
        print("Batch file has no valid URLs.")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)
    except DownloadError as exc:
        print(f"Batch download failed: {exc}")

# Updates_YT_DLP
#TODO I use UV for this project so the funtion doesn't work. And If someone does not have UV it wont be able to update. May this funtion in not nessesary
def update_yt_dlp() -> None:
    print("Updating yt-dlp...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
        check=False,
    )
    if result.returncode == 0:
        print("yt-dlp updated successfully.")
    else:
        print("yt-dlp update failed.")
