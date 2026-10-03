# ~/.config/zsh/kaiju.zsh-theme
# Kaiju prompt: agnoster's segment chain, standalone (no
# oh-my-zsh). The joins are the theme's terrace, not the powerline arrow: the
# chain opens with the two-step cut top-left (▗▟, U+2597 U+259F) and every
# segment ends with the two-step cut bottom-right (▛▘, U+259B U+2598), drawn
# in the segment's colour over the next one. They are quadrant block elements,
# which foot, alacritty and ghostty draw themselves, so the steps are exact.
#   status  Blaze + Charcoal, only on failure / root / background jobs
#   context Raised Slag + Magma, only over SSH or as another user
#   dir     Ember + Ash
#   git     Ash block with Charcoal text when clean, Magma with ± when dirty
#           (accent choice E: Spine blue only colours small text, never a block)
# The right prompt and autosuggestions use Dim (#7A6656): Hairline
# measures 1.5:1 on Charcoal and cannot be read.
# Hex colours need zsh 5.7+ and a true-colour terminal. No Nerd Font glyph is used.

setopt prompt_subst

KAIJU_DEFAULT_USER=${KAIJU_DEFAULT_USER:-$USER}   # hide context on your own box

K_RAISED='#221C18' K_EMBER='#9E3B14' K_MAGMA='#FF8A3D'
K_ASH='#ECE6DA'    K_SPINE='#5FB8FF' K_BLAZE='#FF3B3B'
K_CHARCOAL='#0C0B0A' K_DIM='#7A6656'

KAIJU_HEAD='▗▟'   # terrace, top-left: rises in two steps into the first segment
KAIJU_SEP='▛▘'    # terrace, bottom-right: a segment steps down onto the next one
typeset -g KAIJU_BG=NONE

kaiju_segment() {
  local bg="%K{$1}" fg="%F{$2}"
  if [[ $KAIJU_BG == NONE ]]; then
    print -n "%{%k%F{$1}%}$KAIJU_HEAD%{$bg$fg%} "
  elif [[ $1 != $KAIJU_BG ]]; then
    print -n "%{$bg%F{$KAIJU_BG}%}$KAIJU_SEP%{$fg%} "
  else
    print -n "%{$bg%}%{$fg%} "
  fi
  KAIJU_BG=$1
  [[ -n $3 ]] && print -n -- "$3 "
}

kaiju_end() {
  if [[ $KAIJU_BG != NONE ]]; then
    print -n "%{%k%F{$KAIJU_BG}%}$KAIJU_SEP"
  else
    print -n "%{%k%}"
  fi
  print -n "%{%f%}"
  KAIJU_BG=NONE
}

# ~/dotfiles/hypr -> ~/d/hypr
kaiju_short_pwd() {
  local p=${(%):-%~}
  local -a parts=("${(@s:/:)p}")
  local i
  for (( i = 1; i < ${#parts}; i++ )); do
    [[ -z ${parts[i]} || ${parts[i]} == '~' ]] && continue
    if [[ ${parts[i]} == .* ]]; then
      parts[i]=${parts[i][1,2]}
    else
      parts[i]=${parts[i][1]}
    fi
  done
  print -rn -- "${(j:/:)parts//\%/%%}"
}

kaiju_status() {
  local -a s
  (( KAIJU_RETVAL != 0 )) && s+="✘ $KAIJU_RETVAL"
  (( UID == 0 )) && s+="⚡"
  [[ -n ${jobstates} ]] && s+="⚙"
  (( ${#s} )) && kaiju_segment $K_BLAZE $K_CHARCOAL "${(j: :)s}"
}

kaiju_context() {
  [[ $USER != $KAIJU_DEFAULT_USER || -n $SSH_CONNECTION ]] &&
    kaiju_segment $K_RAISED $K_MAGMA '%n@%m'
}

kaiju_dir() {
  kaiju_segment $K_EMBER $K_ASH "$(kaiju_short_pwd)"
}

kaiju_git() {
  command git rev-parse --is-inside-work-tree &>/dev/null || return
  local ref
  ref=$(command git symbolic-ref --short HEAD 2>/dev/null) ||
    ref="➦ $(command git rev-parse --short HEAD 2>/dev/null)"
  ref=${ref//\%/%%}
  if [[ -n $(command git status --porcelain --ignore-submodules=dirty 2>/dev/null | head -n1) ]]; then
    kaiju_segment $K_MAGMA $K_CHARCOAL "$ref ±"
  else
    kaiju_segment $K_ASH $K_CHARCOAL "$ref"
  fi
}

kaiju_build_prompt() {
  kaiju_status
  kaiju_context
  kaiju_dir
  kaiju_git
  kaiju_end
}

kaiju_precmd() { KAIJU_RETVAL=$? }
autoload -Uz add-zsh-hook
add-zsh-hook precmd kaiju_precmd

PROMPT='%{%f%b%k%}$(kaiju_build_prompt) '
RPROMPT="%F{$K_DIM}%*%f"

# ---- completion ------------------------------------------------------
autoload -Uz compinit && compinit
zstyle ':completion:*' menu select
zstyle ':completion:*' list-colors 'ma=48;2;23;18;37;38;2;237;232;223'

# ---- plugins ---------------------------------------------------------
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=$K_DIM"
[[ -r /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh ]] &&
  source /usr/share/zsh/plugins/zsh-autosuggestions/zsh-autosuggestions.zsh

# zsh-syntax-highlighting must be sourced last, then styled.
if [[ -r /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]]; then
  source /usr/share/zsh/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  ZSH_HIGHLIGHT_STYLES[command]='fg=#ECE6DA'
  ZSH_HIGHLIGHT_STYLES[builtin]='fg=#ECE6DA'
  ZSH_HIGHLIGHT_STYLES[alias]='fg=#ECE6DA'
  ZSH_HIGHLIGHT_STYLES[function]='fg=#ECE6DA'
  ZSH_HIGHLIGHT_STYLES[precommand]='fg=#ECE6DA,underline'
  ZSH_HIGHLIGHT_STYLES[path]='fg=#ECE6DA'
  ZSH_HIGHLIGHT_STYLES[single-hyphen-option]='fg=#5FB8FF'
  ZSH_HIGHLIGHT_STYLES[double-hyphen-option]='fg=#5FB8FF'
  ZSH_HIGHLIGHT_STYLES[single-quoted-argument]='fg=#FF8A3D'
  ZSH_HIGHLIGHT_STYLES[double-quoted-argument]='fg=#FF8A3D'
  ZSH_HIGHLIGHT_STYLES[unknown-token]='fg=#FF3B3B,underline'
fi

export FZF_DEFAULT_OPTS="--color=bg+:#221C18,fg:#A89070,fg+:#ECE6DA,hl:#9E3B14,hl+:#FF8A3D,pointer:#FF8A3D,prompt:#FF8A3D,info:#A89070,border:#9E3B14 --pointer='›' --border=sharp"
