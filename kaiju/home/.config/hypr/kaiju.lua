-- Kaiju look and feel.
-- Charged, not loud, "magma under rock": edges
-- are cold and quiet (a 1px border that runs from ash to stone and fades) and
-- the light behind the one thing that matters is the magma (the focused
-- window's shadow). Spine blue is left to small data text. Nothing pulses. Loaded after
-- futuwwa.lua so these values win; behaviour and binds stay there.
--
-- Hyprland has no per-window corner shader, so windows are sharp here and the
-- theme's 12/6 terrace lives where we draw (bar plates, banner, lock field,
-- menus, notifications, icons, cursor, prompt, tmux). On tiled windows the
-- kaiju-corners helper below paints it over the corners (chosen
-- over a 45-degree chamfer).

local C = {
    ground = "0C0B0A",
    edge   = "CFC6B4",   -- ash edge (head of the border)
    stone  = "5A4E44",   -- stone (its body)
    magma  = "FF8A3D",
}

hl.config({
    general = {
        gaps_in     = 6,
        gaps_out    = 12,
        border_size = 1,
        col = {
            active_border   = {
                colors = { "rgb(" .. C.edge .. ")", "rgb(" .. C.stone .. ")", "rgba(" .. C.stone .. "40)" },
                angle  = 160,
            },
            inactive_border = "rgba(" .. C.edge .. "24)",
        },
    },

    decoration = {
        rounding       = 0,
        rounding_power = 2.0,

        active_opacity   = 0.90,
        inactive_opacity = 0.78,

        blur = {
            enabled           = true,
            size              = 10,
            passes            = 3,
            vibrancy          = 0.12,
            noise             = 0.015,
            new_optimizations = true,
            popups            = true,
        },

        glow = {
            enabled = false,
        },

        -- The magma behind the rock: warm light behind the focused window only.
        shadow = {
            enabled        = true,
            range          = 26,
            render_power   = 3,
            offset         = { 0, 0 },
            color          = "rgba(" .. C.magma .. "42)",
            color_inactive = "rgba(00000088)",
        },
    },

    group = {
        col = {
            border_active   = "rgb(" .. C.edge .. ")",
            border_inactive = "rgba(" .. C.edge .. "24)",
        },
    },

    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        background_color         = "rgb(" .. C.ground .. ")",
    },
})

-- Cursor: KaijuClaw (~/.local/share/icons/KaijuClaw, hyprcursor + XCursor).
-- On a live theme switch restore.sh runs `hyprctl setcursor` from gsettings.txt.
hl.env("HYPRCURSOR_THEME", "KaijuClaw")
hl.env("HYPRCURSOR_SIZE", "24")
hl.env("XCURSOR_THEME", "KaijuClaw")
hl.env("XCURSOR_SIZE", "24")

-- A config reload resets the cursor to the default theme; set it again.
local function kaiju_cursor()
    hl.exec_cmd("hyprctl setcursor KaijuClaw 24")
end
hl.on("hyprland.start", kaiju_cursor)
hl.on("config.reloaded", kaiju_cursor)

-- Window corners: Hyprland cannot clip a window into the theme's two-step
-- terrace, so ~/.local/bin/kaiju-corners fakes it on tiled windows with a
-- click-through overlay (see its header for the limits). It keeps a lock, so
-- starting it again on every reload is harmless, and it exits by itself when
-- hyprland.lua stops requiring "kaiju". `kaiju-corners off` / `on` switches it.
local function kaiju_corners()
    hl.exec_cmd(os.getenv("HOME") .. "/.local/bin/kaiju-corners")
end
hl.on("hyprland.start", kaiju_corners)
hl.on("config.reloaded", kaiju_corners)

-- Launcher bind points at the Kaiju launcher; futuwwa.lua binds the Girih one.
hl.unbind("SUPER + D")
hl.bind("SUPER + D",
    hl.dsp.exec_cmd(os.getenv("HOME") .. "/.local/bin/kaiju-launcher"),
    { description = "Application launcher" })

-- Terminals draw their own charcoal glass (foot/alacritty/ghostty alpha) so text stays opaque.
hl.window_rule({
    name    = "kaiju-terminal-opaque",
    match   = { class = "^(foot|footclient|Alacritty|com.mitchellh.ghostty)$" },
    opacity = "1.0 override 1.0 override",
})

-- Blur behind layer surfaces: the bar, alert banners, launcher, notifications.
-- ignore_alpha keeps fully transparent parts of a layer unblurred.
hl.layer_rule({
    name         = "kaiju-bar-glass",
    match        = { namespace = "^hattin-" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "kaiju-launcher-glass",
    match        = { namespace = "^launcher$" },
    blur         = true,
    ignore_alpha = 0.1,
})

hl.layer_rule({
    name         = "kaiju-notify-glass",
    match        = { namespace = "^swaync" },
    blur         = true,
    ignore_alpha = 0.1,
})

-- Launcher: floating foot + fzf (~/.local/bin/kaiju-launcher).
hl.window_rule({
    name     = "kaiju-launcher",
    match    = { class = "^kaiju-launcher$" },
    float    = true,
    size     = "780 470",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

-- Taskwarrior popups from the waybar "yawm" module (~/.local/bin/kaiju-yawm).
hl.window_rule({
    name     = "kaiju-yawm",
    match    = { class = "^kaiju-yawm$" },
    float    = true,
    size     = "820 600",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

hl.window_rule({
    name     = "kaiju-yawm-add",
    match    = { class = "^kaiju-yawm-add$" },
    float    = true,
    size     = "720 240",
    center   = true,
    pin      = true,
    opacity  = "1.0 override 1.0 override",
})

local kaiju_popups = { "kaiju-launcher", "kaiju-yawm", "kaiju-yawm-add" }

-- Close every popup window except those of class `keep`.
-- hl.get_windows matches `class` exactly (no regex), so pass the plain name.
function kaiju_close_popups(keep)
    for _, class in ipairs(kaiju_popups) do
        if class ~= keep then
            for _, w in ipairs(hl.get_windows({ class = class })) do
                hl.dispatch(hl.dsp.window.close({ window = "address:" .. w.address }))
            end
        end
    end
end

function kaiju_close_launcher()
    kaiju_close_popups()
end

-- Close popups as soon as focus moves elsewhere.
hl.on("window.active", function(win)
    kaiju_close_popups(win and win.class)
end)
