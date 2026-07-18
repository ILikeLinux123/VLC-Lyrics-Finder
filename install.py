import os
import sys


EXTENSION_NAME = "lyricsfinder.lua"


# Put your entire VLC Lua extension code between these quotes
LUA_CODE = r"""
-- Lyrics Finder Auto Version
-- VLC 3.0.x
-- ILikeLinux rewrite


auto_change = true
last_song = ""
running = false



function descriptor()

    return {
        title = "Lyrics Finder Auto",
        version = "1.0",
        author = "ILikeLinux",
        shortdesc = "Automatic lyrics finder",
        description = "Automatically opens lyrics when the song changes.",
        capabilities = {
            "input-listener";
            "playing-listener";
            "meta-listener";
        }
    }

end



function activate()

    vlc.msg.info("[Lyrics Finder] Started")

    running = true
    check_song()
    return true

end



function deactivate()

    running = false

    vlc.msg.info("[Lyrics Finder] Stopped")

    return true

end



function close()

    deactivate()

end
------------------------------------------------
-- Get current song
------------------------------------------------

function get_current_song()

    local item = vlc.input.item()

    if not item then
        return ""
    end


    local meta = item:metas()

    local artist = meta["artist"] or ""
    local title = meta["title"] or ""


    -- fallback to filename if metadata is missing
    if title == "" then

        local name = item:name() or ""

        name = string.gsub(
            name,
            "%.%w+$",
            ""
        )

        title = name

    end


    local song =
        artist .. " - " .. title


    return song

end



------------------------------------------------
-- Check if song changed
------------------------------------------------

function check_song()

    if not running then
        return
    end


    local song = get_current_song()


    if song == "" then
        return
    end



    if song ~= last_song then


        vlc.msg.info(
            "[Lyrics Finder] New song: "
            .. song
        )


        last_song = song


        if auto_change then

            find_lyrics()

        end

    end

end



------------------------------------------------
-- VLC calls these when media changes
------------------------------------------------

function input_changed()

    check_song()

end



function playing_changed()

    check_song()

end



function meta_changed()

    check_song()

end
------------------------------------------------
-- URL encode
------------------------------------------------

function url_encode(text)

    if not text then
        return ""
    end


    text = string.gsub(
        text,
        "([^%w %-%_%.%~])",
        function(c)

            return string.format(
                "%%%02X",
                string.byte(c)
            )

        end
    )


    text = string.gsub(
        text,
        " ",
        "+"
    )


    return text

end



------------------------------------------------
-- Build Genius search URL
------------------------------------------------
function remove_artist_from_title(title, artist)

    if title == "" or artist == "" then
        return title
    end

    -- removes:
    -- " - band"
    -- " band"
    title = string.gsub(
        title,
        "%s*%-%s*" .. artist .. "$",
        ""
    )

    title = string.gsub(
        title,
        "%s*" .. artist .. "$",
        ""
    )

    return title

end
------------------------------------------------
-- Convert text into Genius URL format
------------------------------------------------

function slugify(text)

    text = string.lower(text)

    text = string.gsub(text, "&", "and")
    text = string.gsub(text, "[^%w%s%-]", "")
    text = string.gsub(text, "%s+", "-")
    text = string.gsub(text, "%-+", "-")

    return text

end


function build_lyrics_url()

    local item = vlc.input.item()

    if not item then
        return nil
    end


    local meta = item:metas()

    local artist = meta["artist"] or ""
    local title = meta["title"] or ""


    if artist == "" then
        artist = "unknown"
    end


    if title == "" then
        title = item:name()
        title = string.gsub(title, "%.%w+$", "")
    end


title = remove_artist_from_title(title, artist)

local url =
    "https://genius.com/"
    .. slugify(artist)
    .. "-"
    .. slugify(title)
    .. "-lyrics"

    return url

end

------------------------------------------------
-- Open Firefox
------------------------------------------------

function open_firefox(url)

    if not url then
        return
    end


    vlc.msg.info(
        "[Lyrics Finder] Opening: "
        .. url
    )


    os.execute(
        'start "" firefox "' 
        .. url 
        .. '"'
    )

end



------------------------------------------------
-- Find lyrics
------------------------------------------------

function find_lyrics()

    local url = build_lyrics_url()


    if url then

        open_firefox(url)

    else

        vlc.msg.warn(
            "[Lyrics Finder] No song detected"
        )

    end

end
"""


def find_vlc_extensions():
    locations = []

    # Windows
    if sys.platform.startswith("win"):
        locations.append(
            os.path.join(
                os.environ.get("APPDATA", ""),
                "vlc",
                "lua",
                "extensions"
            )
        )

        locations.append(
            r"C:\Program Files\VideoLAN\VLC\lua\extensions"
        )

        locations.append(
            r"C:\Program Files (x86)\VideoLAN\VLC\lua\extensions"
        )

    # Linux
    elif sys.platform.startswith("linux"):
        locations.append(
            os.path.expanduser(
                "~/.local/share/vlc/lua/extensions"
            )
        )

        locations.append(
            "/usr/lib/vlc/lua/extensions"
        )

    # macOS
    elif sys.platform == "darwin":
        locations.append(
            os.path.expanduser(
                "~/Library/Application Support/org.videolan.vlc/lua/extensions"
            )
        )

    return locations


def install_extension():

    folders = find_vlc_extensions()

    installed = False

    for folder in folders:

        if os.path.exists(folder):

            path = os.path.join(folder, EXTENSION_NAME)

            with open(path, "w", encoding="utf-8") as f:
                f.write(LUA_CODE)

            print("Installed:")
            print(path)

            installed = True


    if not installed:

        # Use user VLC folder if none exists
        folder = folders[0]

        os.makedirs(folder, exist_ok=True)

        path = os.path.join(folder, EXTENSION_NAME)

        with open(path, "w", encoding="utf-8") as f:
            f.write(LUA_CODE)

        print("Created and installed:")
        print(path)



if __name__ == "__main__":

    print("VLC Lyrics Finder Installer")
    print("---------------------------")

    install_extension()

    print("\nDone! Restart VLC to load the extension.")