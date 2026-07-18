
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
