import argparse
import asyncio
from pathlib import Path

from gamdl.api import AppleMusicApi
from gamdl.downloader import (
    AppleMusicBaseDownloader,
    AppleMusicDownloader,
    AppleMusicMusicVideoDownloader,
    AppleMusicSongDownloader,
    AppleMusicUploadedVideoDownloader,
)
from gamdl.interface import (
    AppleMusicBaseInterface,
    AppleMusicInterface,
    AppleMusicMusicVideoInterface,
    AppleMusicSongInterface,
    AppleMusicUploadedVideoInterface,
)

DEFAULT_COOKIES_PATH = Path(r"C:\Users\haku12\Downloads\cookies.txt")


def prompt_for_value(label: str, default: str | None = None) -> str:
    if default:
        prompt = f"{label} [{default}]: "
    else:
        prompt = f"{label}: "
    value = input(prompt).strip()
    return value or (default or "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download an Apple Music playlist or single track with gamdl.",
    )
    parser.add_argument(
        "urls",
        nargs="*",
        help="Apple Music URL(s) for a playlist, album, song, artist, or video.",
    )
    parser.add_argument(
        "--cookies-path",
        default=None,
        help="Path to Netscape-format cookies.txt.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    cookies_path = args.cookies_path or prompt_for_value(
        "Enter cookies.txt path",
        str(DEFAULT_COOKIES_PATH),
    )
    urls = args.urls or [
        url.strip()
        for url in prompt_for_value(
            "Enter Apple Music playlist or song URL(s) separated by spaces",
        ).split()
        if url.strip()
    ]

    if not cookies_path:
        print("No cookies path provided.")
        return

    if not urls:
        print("No Apple Music URL provided.")
        return

    apple_music_api = await AppleMusicApi.create_from_netscape_cookies(
        cookies_path=cookies_path,
    )

    if not apple_music_api.active_subscription:
        print("No active Apple Music subscription")
        return

    base_interface = await AppleMusicBaseInterface.create(
        apple_music_api=apple_music_api,
    )

    song_interface = AppleMusicSongInterface(base=base_interface)
    music_video_interface = AppleMusicMusicVideoInterface(base=base_interface)
    uploaded_video_interface = AppleMusicUploadedVideoInterface(base=base_interface)

    interface = AppleMusicInterface(
        song=song_interface,
        music_video=music_video_interface,
        uploaded_video=uploaded_video_interface,
    )

    base_downloader = AppleMusicBaseDownloader(interface=interface)

    downloader = AppleMusicDownloader(
        song=AppleMusicSongDownloader(base=base_downloader),
        music_video=AppleMusicMusicVideoDownloader(base=base_downloader),
        uploaded_video=AppleMusicUploadedVideoDownloader(base=base_downloader),
    )

    download_queue = []
    for url in urls:
        async for media in downloader.get_download_item_from_url(url):
            download_queue.append(media)

    print(f"Found {len(download_queue)} items. Starting downloads...")

    for item in download_queue:
        try:
            await downloader.download(item)
        except Exception as e:
            print(f"Error downloading: {e}")


if __name__ == "__main__":
    asyncio.run(main())
