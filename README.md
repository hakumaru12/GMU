# GMU

[English](#english) | [日本語](#日本語)

---

## English

# GMU
The tool that makes [Gamdl](https://github.com/glomatico/gamdl) (Apple Music downloader) more useful.

This repository provides `GMU.py`, a small wrapper around the `gamdl` library to download Apple Music playlists, songs and videos using a Netscape-format `cookies.txt`.
## Installation
You can also use .exe file from [release](https://github.com/hakumaru12/GMU/releases/).
If you use this file, you don't need to install gamdl.

### Requirements
- Python 3.7 or higher
- pip (Python package manager)

### Steps
1. Clone the repository:
```bash
git clone https://github.com/hakumaru12/GMU.git
cd GMU
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Getting cookies.txt
1. Open your browser (Chrome, Firefox, Safari, etc.)
2. Visit https://music.apple.com and log in to your Apple Music account
3. Install a cookie export extension:
   - **Chrome/Edge**: [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/ookdjilphngeeeghgngjabigmpepanpl)
   - **Firefox**: [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
4. Export cookies in **Netscape format** and save as `cookies.txt`

## How to Use

### Prerequisites
- Apple Music subscription (active)
- Netscape-format `cookies.txt` file from your browser

### Basic Usage
Run the script with:
```bash
python GMU.py
```

The script supports the following options (defaults shown):

- `--cookies-path`: Path to Netscape-format `cookies.txt` (default prompts to `Downloads/cookies.txt`).
- `--batch-size` (int, default `0`): Number of items per batch. `0` downloads all at once.
- `--concurrency` (int, default `1`): Number of parallel downloads inside each batch.
- `--windows` (int, default `1`): On Windows, split URLs/playlists into multiple console windows.

Hidden/internal options used by worker subprocesses:

- `--window-worker`, `--playlist-url`, `--playlist-track-start`, `--playlist-track-end` (not for interactive use).

The script will prompt you for:
1. Path to `cookies.txt`
2. Apple Music URL(s) to download

### Arguments
- `urls`: Apple Music URL(s) for playlist, album, song, artist, or video (optional - you'll be prompted if not provided)
- `--cookies-path`: Path to Netscape-format cookies.txt file (optional - you'll be prompted if not provided)

### Examples

**Interactive mode (with prompts):**
```bash
python GMU.py
```

**Command-line arguments:**
```bash
python GMU.py "https://music.apple.com/playlist/..." --cookies-path "/path/to/cookies.txt"
```

**Multiple URLs:**
```bash
python GMU.py "https://music.apple.com/playlist/..." "https://music.apple.com/song/..." --cookies-path "/path/to/cookies.txt"
```

## Features
- Download Apple Music playlists
- Batch download multiple songs
- Organize downloads by artist and album
- Support for various audio formats

## License
See [LICENSE](LICENSE) file for details.

---

## 日本語

# GMU
[Gamdl](https://github.com/glomatico/gamdl)（Apple Musicダウンローダー）をより便利にするツール。

## インストール
.exeファイルから起動できるようになりました！[リリース](https://github.com/hakumaru12/GMU/releases/)よりダウンロードしてください

これを使用した場合、以下のgamdlをインストールする操作は不要になります
### 必要な環境
- Python 3.7以上
- pip（Pythonパッケージマネージャー）

### インストール手順
1. リポジトリをクローンします：
```bash
git clone https://github.com/hakumaru12/GMU.git
cd GMU
```

2. 依存パッケージをインストールします：
```bash
pip install -r requirements.txt
```

### cookies.txt の取得方法
1. ブラウザを開き、https://music.apple.com にアクセスしてApple Musicアカウントでログインします
2. Cookie エクスポート拡張機能をインストール：
   - **Chrome/Edge**: [Cookie Editor](https://chromewebstore.google.com/detail/cookie-editor/ookdjilphngeeeghgngjabigmpepanpl)
   - **Firefox**: [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
3. **Netscape形式** でクッキーをエクスポートして、`cookies.txt` として保存します

## 使い方

### 前提条件
- Apple Music定期契約（有効）
- ブラウザから取得したNetscape形式の `cookies.txt` ファイル

### 基本的な使用方法
以下のコマンドでスクリプトを実行します：
```bash
python GMU.py
```

スクリプトは以下のオプションをサポートしています（既定値を記載）：

- `--cookies-path`: Netscape 形式の `cookies.txt` へのパス（既定：`Downloads/cookies.txt` をプロンプトで提案）。
- `--batch-size`（整数、既定 `0`）: バッチあたりのアイテム数。`0` ですべてを一度にダウンロード。
- `--concurrency`（整数、既定 `1`）: バッチ内で並列にダウンロードするアイテム数。
- `--windows`（整数、既定 `1`）: Windows 上で複数のコマンドプロンプトウィンドウに URL/プレイリストを分割。

内部ワーカーサブプロセスが使用する隠しオプション：

- `--window-worker`, `--playlist-url`, `--playlist-track-start`, `--playlist-track-end`（対話型利用向けではありません）。

スクリプトは以下を入力するよう促します：
1. `cookies.txt` のパス
2. ダウンロードするApple Music の URL（複数の場合はスペース区切り）

### コマンドラインオプション
- `urls`: プレイリスト、アルバム、曲、アーティスト、またはビデオのApple Music URL（オプション - 省略時はプロンプトで入力）
- `--cookies-path`: Netscape形式の cookies.txt ファイルへのパス（オプション - 省略時はプロンプトで入力）

### 実行例

**対話モード（プロンプト入力）:**
```bash
python GMU.py
```

単一 URL 指定:

```bash
python GMU.py "https://music.apple.com/playlist/..." --cookies-path "C:\Users\you\Downloads\cookies.txt"
```

バッチ実行例:

```bash
python GMU.py "https://music.apple.com/playlist/..." --cookies-path "C:\Users\you\Downloads\cookies.txt" --batch-size 10 --concurrency 3
```

複数ウィンドウに分割（Windows 向け）:

```bash
python GMU.py "https://music.apple.com/playlist/..." --cookies-path "C:\Users\you\Downloads\cookies.txt" --windows 3
```

## 機能
- Apple Musicプレイリストのダウンロード
- 複数の楽曲を一括ダウンロード
- アーティストとアルバムごとにダウンロードを整理
- 複数のオーディオ形式に対応

## ライセンス
詳細は[LICENSE](LICENSE)ファイルを参照してください。
