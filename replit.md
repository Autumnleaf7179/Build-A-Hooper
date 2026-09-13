# Offline project setup

This project is a static capture of the Build a Hooper landing/play page. It
does not include the original site's server, database, or source code.

## Run locally on Replit

The `Start application` workflow runs:

```sh
python3 offline_server.py
```

The server listens on port 5000 and serves the downloaded files only. It never
proxies requests to the original website. Captured client routes fall back to
the downloaded `index.html` so they remain local instead of producing a
missing-page request.

Do not open `index.html` by double-clicking it. That uses a `file://` URL, and
the captured Next.js assets use root-relative paths that browsers cannot
resolve correctly from the filesystem. Open the Replit Preview while the
`Start application` workflow is running instead. On another computer, run
`python3 offline_server.py` from this folder and open
`http://localhost:5000/`.

## Current offline boundary

The root page and its downloaded JavaScript, CSS, fonts, and icons work
offline. The original login, account creation, achievements, leaderboard, and
server-backed game persistence were not present in the downloaded files, so
those features cannot be restored without implementing local replacements.