import argparse
import asyncio
import subprocess
import sys
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

DEFAULT_COOKIES_PATH = Path.home() / "Downloads" / "cookies.txt"


def chunked(items: list, size: int):
    for index in range(0, len(items), size):
        yield items[index : index + size]


def split_into_windows(items: list, window_count: int) -> list[list]:
    if window_count <= 1 or len(items) <= 1:
        return [items]

    window_count = min(window_count, len(items))
    base_size = len(items) // window_count
    remainder = len(items) % window_count
    chunks: list[list] = []
    start = 0

    for index in range(window_count):
        extra = 1 if index < remainder else 0
        end = start + base_size + extra
        chunks.append(items[start:end])
        start = end

    return [chunk for chunk in chunks if chunk]


def split_track_ranges(total_items: int, window_count: int) -> list[tuple[int, int]]:
    if window_count <= 1 or total_items <= 1:
        return [(0, total_items)]

    window_count = min(window_count, total_items)
    base_size = total_items // window_count
    remainder = total_items % window_count
    ranges: list[tuple[int, int]] = []
    start = 0

    for index in range(window_count):
        extra = 1 if index < remainder else 0
        end = start + base_size + extra
        if start < end:
            ranges.append((start, end))
        start = end

    return ranges


def launch_worker_window(script_path: str, cookies_path: str, urls: list[str], concurrency: int, batch_size: int) -> None:
    command = [
        sys.executable,
        script_path,
        "--window-worker",
        "--cookies-path",
        cookies_path,
        "--concurrency",
        str(concurrency),
    ]

    if batch_size > 0:
        command.extend(["--batch-size", str(batch_size)])

    command.extend(urls)

    subprocess.Popen(
        command,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


def launch_playlist_worker_window(
    script_path: str,
    cookies_path: str,
    playlist_url: str,
    track_start: int,
    track_end: int,
    concurrency: int,
    batch_size: int,
) -> None:
    command = [
        sys.executable,
        script_path,
        "--window-worker",
        "--cookies-path",
        cookies_path,
        "--playlist-url",
        playlist_url,
        "--playlist-track-start",
        str(track_start),
        "--playlist-track-end",
        str(track_end),
        "--concurrency",
        str(concurrency),
    ]

    if batch_size > 0:
        command.extend(["--batch-size", str(batch_size)])

    subprocess.Popen(
        command,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


async def download_item(downloader: AppleMusicDownloader, item) -> None:
    try:
        await downloader.download(item)
    except Exception as e:
        print(f"Error downloading: {e}")


async def download_items(
    downloader: AppleMusicDownloader,
    items: list,
    concurrency: int,
) -> None:
    if concurrency <= 1:
        for item in items:
            await download_item(downloader, item)
        return

    semaphore = asyncio.Semaphore(concurrency)

    async def run_item(item) -> None:
        async with semaphore:
            await download_item(downloader, item)

    await asyncio.gather(*(run_item(item) for item in items))


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
    parser.add_argument(
        "--batch-size",
        type=int,
        default=0,
        help="Download items in batches of this size. Use 0 to download everything at once.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of items to download at the same time inside each batch.",
    )
    parser.add_argument(
        "--windows",
        type=int,
        default=1,
        help="Open separate command prompt windows and split URLs across them.",
    )
    parser.add_argument(
        "--window-worker",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--playlist-url",
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--playlist-track-start",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--playlist-track-end",
        type=int,
        default=None,
        help=argparse.SUPPRESS,
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    script_path = str(Path(__file__).resolve())

    cookies_path = args.cookies_path or prompt_for_value(
        "Enter cookies.txt path",
        str(DEFAULT_COOKIES_PATH),
    )

    urls = args.urls
    if not urls and args.window_worker and args.playlist_url:
        urls = [args.playlist_url]
    elif not urls:
        urls = [
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

    if args.windows > 1 and not args.window_worker:
        if len(urls) == 1:
            source_url = urls[0]

            try:
                url_info = AppleMusicInterface.get_url_info(source_url)
            except Exception:
                url_info = None

            if url_info and (url_info.type == "playlist" or url_info.library_type == "playlist"):
                apple_music_api = await AppleMusicApi.create_from_netscape_cookies(
                    cookies_path=cookies_path,
                )

                if not apple_music_api.active_subscription:
                    print("No active Apple Music subscription")
                    return

                base_interface = await AppleMusicBaseInterface.create(
                    apple_music_api=apple_music_api,
                )
                probe_interface = AppleMusicInterface(
                    song=AppleMusicSongInterface(base=base_interface),
                    music_video=AppleMusicMusicVideoInterface(base=base_interface),
                    uploaded_video=AppleMusicUploadedVideoInterface(base=base_interface),
                )
                probe_downloader = AppleMusicDownloader(
                    song=AppleMusicSongDownloader(
                        base=AppleMusicBaseDownloader(interface=probe_interface)
                    ),
                    music_video=AppleMusicMusicVideoDownloader(
                        base=AppleMusicBaseDownloader(interface=probe_interface)
                    ),
                    uploaded_video=AppleMusicUploadedVideoDownloader(
                        base=AppleMusicBaseDownloader(interface=probe_interface)
                    ),
                )

                tracks = []
                async for media in probe_downloader.base.interface.get_media_from_url(source_url):
                    if media.playlist_metadata is not None:
                        tracks.append(media)

                if len(tracks) <= 1:
                    print("Not enough playlist tracks to split into multiple windows. Running in one window.")
                else:
                    ranges = split_track_ranges(len(tracks), args.windows)
                    print(f"Launching {len(ranges)} command prompt windows for {len(tracks)} playlist tracks...")
                    for index, (track_start, track_end) in enumerate(ranges, start=1):
                        print(
                            f"Starting window {index}/{len(ranges)} with tracks {track_start + 1}-{track_end}"
                        )
                        launch_playlist_worker_window(
                            script_path=script_path,
                            cookies_path=cookies_path,
                            playlist_url=source_url,
                            track_start=track_start,
                            track_end=track_end,
                            concurrency=args.concurrency,
                            batch_size=args.batch_size,
                        )
                    return

        url_groups = split_into_windows(urls, args.windows)

        if len(url_groups) <= 1:
            print("Not enough URLs to split into multiple windows. Running in one window.")
        else:
            print(f"Launching {len(url_groups)} command prompt windows...")
            for index, group in enumerate(url_groups, start=1):
                print(f"Starting window {index}/{len(url_groups)} with {len(group)} URL(s)")
                launch_worker_window(
                    script_path=script_path,
                    cookies_path=cookies_path,
                    urls=group,
                    concurrency=args.concurrency,
                    batch_size=args.batch_size,
                )
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
            if (
                args.window_worker
                and args.playlist_url
                and args.playlist_track_start is not None
                and args.playlist_track_end is not None
            ):
                if media.media.playlist_metadata is None:
                    continue

                if not (
                    args.playlist_track_start
                    <= media.media.index
                    < args.playlist_track_end
                ):
                    continue

            download_queue.append(media)

    if args.batch_size and args.batch_size > 0:
        batches = list(chunked(download_queue, args.batch_size))
        print(
            f"Found {len(download_queue)} items. Downloading in {len(batches)} batches "
            f"with concurrency={args.concurrency}..."
        )

        for batch_index, batch in enumerate(batches, start=1):
            print(f"Starting batch {batch_index}/{len(batches)} ({len(batch)} items)")
            await download_items(downloader, batch, args.concurrency)
    else:
        print(f"Found {len(download_queue)} items. Starting downloads with concurrency={args.concurrency}...")

        await download_items(downloader, download_queue, args.concurrency)


if __name__ == "__main__":
    asyncio.run(main())
