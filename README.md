# MSTP Constellation

The UW–Madison MSTP retreat yearbook, as a night sky. Live at https://mstp-constellation.com

## Layout

- `2026/index.html` — the 2026 yearbook. One self-contained file: all photos, data, and code are inside it.
- `index.html` + `netlify.toml` — the root redirects to the current year.
- Future years get their own folder (`2027/`) and a one-line change to the redirect in `netlify.toml`.

## Deploying (first time)

1. Push this repo to GitHub.
2. In Netlify: **Add new site → Import an existing project → GitHub → mstp-constellation**.
   Build command: *(leave empty)*. Publish directory: `.`
3. **Domain management → Add a domain → mstp-constellation.com**, then follow Netlify's DNS instructions
   at your registrar (either point nameservers at Netlify, or add the A/CNAME records it shows).
   HTTPS is automatic once DNS resolves.

## Passcode

`2026/index.html` is a tiny gate page. The real yearbook lives beside it as `2026/sky-<hash>.bin`, AES-256 encrypted with the
program passcode, so the content is unreadable without it (not just hidden). The gate starts downloading the payload immediately
with a progress indicator, then decrypts it when the passcode is entered. Visitors enter it once per browser tab session.

To change the passcode or re-lock a new version: `python3 tools/lock.py "<passcode>" unlocked.html 2026/index.html` (writes the gate and a new `sky-<hash>.bin`, removing the old one)
(needs `pip install cryptography`). Keep the unlocked source out of the repo.

## Updating the yearbook

Replace `2026/index.html` with the new version, commit, push. Netlify redeploys in about a minute.

## Notes

- The page has no backend and stores nothing about visitors.
- The Retreat Agenda panel includes a staff contact number; remove it before making the site public beyond the program if that matters.
