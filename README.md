# GMU

[English](#english) | [日本語](#日本語)

---

## English

# GMU
The tool that makes Gamdi (Apple Music downloader) more useful.

## Installation

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
   - **Chrome/Edge**: [Export Cookies](https://chrome.google.com/webstore/detail/export-cookies/) or [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/)
   - **Firefox**: [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies/)
4. Export cookies in **Netscape format** and save as `cookies.txt`

## How to Use

### Prerequisites
- Apple Music subscription (active)
- Netscape-format `cookies.txt` file from your browser

### Basic Usage
Run the script with:
```bash
python download_playlist.py
```

The script will prompt you for:
1. Path to `cookies.txt`
2. Apple Music URL(s) to download

### Arguments
- `urls`: Apple Music URL(s) for playlist, album, song, artist, or video (optional - you'll be prompted if not provided)
- `--cookies-path`: Path to Netscape-format cookies.txt file (optional - you'll be prompted if not provided)

### Examples

**Interactive mode (with prompts):**
```bash
python download_playlist.py
```

**Command-line arguments:**
```bash
python download_playlist.py "https://music.apple.com/playlist/..." --cookies-path "/path/to/cookies.txt"
```

**Multiple URLs:**
```bash
python download_playlist.py "https://music.apple.com/playlist/..." "https://music.apple.com/song/..." --cookies-path "/path/to/cookies.txt"
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
Gamdi（Apple Musicダウンローダー）をより便利にするツール。

## インストール

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
   - **Chrome/Edge**: [Export Cookies](https://chrome.google.com/webstore/detail/export-cookies/) または [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/)
   - **Firefox**: [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies/)
3. **Netscape形式** でクッキーをエクスポートして、`cookies.txt` として保存します

## 使い方

### 前提条件
- Apple Music定期契約（有効）
- ブラウザから取得したNetscape形式の `cookies.txt` ファイル

### 基本的な使用方法
以下のコマンドでスクリプトを実行します：
```bash
python download_playlist.py
```

スクリプトは以下を入力するよう促します：
1. `cookies.txt` のパス
2. ダウンロードするApple MusicのURL

### コマンドラインオプション
- `urls`: プレイリスト、アルバム、曲、アーティスト、またはビデオのApple Music URL（オプション - 省略時はプロンプトで入力）
- `--cookies-path`: Netscape形式の cookies.txt ファイルへのパス（オプション - 省略時はプロンプトで入力）

### 実行例

**対話モード（プロンプト入力）:**
```bash
python download_playlist.py
```

**コマンドライン引数を使用：**
```bash
python download_playlist.py "https://music.apple.com/playlist/..." --cookies-path "/path/to/cookies.txt"
```

**複数のURL:**
```bash
python download_playlist.py "https://music.apple.com/playlist/..." "https://music.apple.com/song/..." --cookies-path "/path/to/cookies.txt"
```

## 機能
- Apple Musicプレイリストのダウンロード
- 複数の楽曲を一括ダウンロード
- アーティストとアルバムごとにダウンロードを整理
- 複数のオーディオ形式に対応

## ライセンス
詳細は[LICENSE](LICENSE)ファイルを参照してください。
