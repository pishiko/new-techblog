#!/usr/bin/env python3
# repo_card.py
import sys
import re
import requests

THEMES = {
    "dark-theme": {
        "background": "transparent",
        "borderColor": "rgb(48, 54, 61)",
        "color": "rgb(139, 148, 158)",
        "linkColor": "rgb(88, 166, 255)",
    },
}

def fetch_json(url, timeout=15):
    headers = {"Accept": "application/vnd.github+json"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def replace_emojis(text, emoji_map):
    if not text:
        return ""
    pattern = re.compile(r":\w+:")
    def _repl(m):
        name = m.group(0)[1:-1]
        url = emoji_map.get(name)
        if url:
            return (
                f'<span><img src="{url}" '
                f'style="width: 1rem; height: 1rem; vertical-align: -0.2rem;" '
                f'alt="{name}"></span>'
            )
        return m.group(0)
    return pattern.sub(_repl, text)

def render_repo_card(user, repo):
    theme = THEMES["dark-theme"]

    # 外部データの取得（JS と同じエンドポイント）
    emojis = fetch_json("https://api.github.com/emojis")
    colors = fetch_json("https://raw.githubusercontent.com/ozh/github-colors/master/colors.json")
    data = fetch_json(f"https://api.github.com/repos/{user}/{repo}")

    # 説明文の :emoji: を <img> に置換
    description_html = replace_emojis(data.get("description") or "", emojis)

    # 各種表示用値
    is_fork = bool(data.get("fork"))
    source = data.get("source") or {}
    source_html_url = source.get("html_url", "")
    source_full_name = source.get("full_name", "")

    language = data.get("language")
    language_color = colors.get(language, {}).get("color", "") if language else ""

    stars = int(data.get("stargazers_count", 0))
    forks = int(data.get("forks", data.get("forks_count", 0) or 0))

    html = f"""
    <div style="font-family: -apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji; border: 1px solid {theme['borderColor']}; border-radius: 6px; background: {theme['background']}; padding: 16px; font-size: 14px; line-height: 1.5; color: #24292e;">
      <div style="display: flex; align-items: center;">
        <svg style="fill: {theme['color']}; margin-right: 8px;" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5v-9zm10.5-1V9h-8c-.356 0-.694.074-1 .208V2.5a1 1 0 011-1h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"></path></svg>
        <span style="font-weight: 600; color: {theme['linkColor']};">
          <a style="text-decoration: none; color: inherit;" href="{data.get('html_url', '')}">{data.get('full_name', '')}</a>
        </span>
      </div>
      <div style="display: {'block' if is_fork else 'none'}; font-size: 12px; color: {theme['color']};">Forked from <a style="color: inherit; text-decoration: none;" href="{source_html_url}">{source_full_name}</a></div>
      <div style="font-size: 12px; margin-bottom: 16px; margin-top: 8px; color: {theme['color']};">{description_html}</div>
      <div style="font-size: 12px; color: {theme['color']}; display: flex;">
        <div style="{'' if language else 'display: none;'} margin-right: 16px;">
          <span style="width: 12px; height: 12px; border-radius: 100%; background-color: {language_color}; display: inline-block; top: 1px; position: relative;"></span>
          <span>{language or ''}</span>
        </div>
        <div style="display: {'flex' if stars != 0 else 'none'}; align-items: center; margin-right: 16px;">
          <svg style="fill: {theme['color']};" aria-label="stars" viewBox="0 0 16 16" version="1.1" width="16" height="16" role="img"><path fill-rule="evenodd" d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z"></path></svg>
          &nbsp; <span>{stars}</span>
        </div>
        <div style="display: {'flex' if forks != 0 else 'none'}; align-items: center;">
          <svg style="fill: {theme['color']};" aria-label="fork" viewBox="0 0 16 16" version="1.1" width="16" height="16" role="img"><path fill-rule="evenodd" d="M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 100-1.5.75.75 0 000 1.5z"></path></svg>
          &nbsp; <span>{forks}</span>
        </div>
      </div>
    </div>
    """.strip("\n")

    return html

if __name__ == "__main__":
    print(render_repo_card('pishiko', 'tenmusu'))