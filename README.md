# VLC-Lyrics-Finder

# 🎵 VLC Lyrics Finder Auto

# ⚠️ THIS MIGHT NOT WORK FOR ALL ARTISTS/BANDS

# ✅ THIS HAS BEEN CONFIRMED USING CDS

A lightweight VLC extension that automatically finds lyrics for the currently playing song.

This extension watches the song currently playing in VLC and can automatically open the matching Genius lyrics page in your browser. It is designed to work without API keys, accounts, or extra services.

## Features

* ✅ Automatic song change detection
* ✅ Opens lyrics automatically when a new song starts
* ✅ Works with VLC 3.x extensions
* ✅ No API keys required
* ✅ Uses Genius lyric pages
* ✅ Supports manual "Find Lyrics" searching
* ✅ Simple installation

## How It Works

The extension checks the currently playing song information from VLC:

```
Artist - Song Name
```

It then creates a Genius URL:

```
https://genius.com/{artist}-{song-name}-lyrics
```

The extension also cleans up song titles by removing duplicate artist names when needed.

Example:

```
AJR - Worlds Smallest Violin - AJR
```

Becomes:

```
https://genius.com/ajr-worlds-smallest-violin-lyrics
```

## Installation

Run the included installer script and it will automatically find your VLC installation folder and place the extension in the correct location.

Or manually copy:

```
lyricsfinder.lua
```

into:

```
VLC/lua/extensions/
```

Restart VLC, then open:

```
View → Lyrics Finder
```

## Compatibility

Tested with:

* VLC 3.0.23
* Music played from CDs

## Limitations

This extension depends on VLC providing correct artist and title metadata.

Some artists, albums, or songs may not work if:

* The metadata is incorrect
* Genius uses a different URL format
* The song does not have a Genius page
* The artist name or title is formatted differently

## License

Open source project. Use, modify, and share freely.
