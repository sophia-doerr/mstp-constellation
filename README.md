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

## Updating the yearbook

Replace `2026/index.html` with the new version, commit, push. Netlify redeploys in about a minute.

## Notes

- The page has no backend and stores nothing about visitors.
- The Retreat Agenda panel includes a staff contact number; remove it before making the site public beyond the program if that matters.
