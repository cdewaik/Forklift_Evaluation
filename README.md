# Forklift Operator Evaluation Form

A no-login replacement for the Google Form at
`docs.google.com/forms/d/e/1FAIpQLScypWQy3DDFyqxKFnYI77q4GTaAYsnKDuUWYwGI6TvRzeDFPg`
(that form requires signing in with a `cscmfg.com` account; this one doesn't
require signing in at all). Styled to match the
[Container Supply Employee Information Hub](https://container-supply-company.github.io/CSC-Employee-Information-HUB/).

Three things do the work:

- **`index.html`** — the form itself (all styling + the 35-item checklist).
- **`Code.gs`** — an Apps Script backend that writes every submission as a
  row in a Google Sheet.
- **`audio/`** — spoken narration clips, English and Spanish, for each
  checklist item, played from a speaker icon next to it. A language toggle
  in the intro card switches which one plays.

You need `Code.gs` deployed as an Apps Script Web App either way — it's what
actually records responses. `index.html` can then be hosted two ways.

## 1. Deploy the Apps Script backend (required either way)

1. Go to [script.google.com](https://script.google.com) → **New project**.
2. Delete the default `Code.gs` contents and paste in this project's
   `Code.gs`.
3. Add a second file: **File → New → HTML file**, name it `index` (exactly —
   no `.html` extension in the name field), and paste in the contents of
   this project's `index.html`.
4. Click **Deploy → New deployment**.
   - Type: **Web app**
   - Execute as: **Me**
   - Who has access: **Anyone** ← this is what removes the login requirement.
     ("Anyone with a Google account" would still force a sign-in.)
5. Click **Deploy**, authorize the script when prompted, and copy the
   **Web app URL** (ends in `/exec`).

That URL, opened directly, is a fully working version of the form — no
login needed — and every submission lands in a Google Sheet named
**"Forklift Operator Evaluations"** that the script creates the first time
it runs (check My Drive, or Script Properties → `SPREADSHEET_ID` inside the
Apps Script editor for the direct link).

If you only want this Apps Script URL and don't need a separate GitHub
Pages site, you're done — share that `/exec` link.

## 2. (Optional) Host `index.html` on GitHub Pages instead

If you'd rather have a friendlier/custom URL via GitHub Pages, the same
`index.html` works standalone — it just needs to know where to send
submissions, since a static GitHub Pages site has no backend of its own.

1. Open `index.html` and find this line near the bottom:

   ```js
   const WEB_APP_URL = "PASTE_YOUR_APPS_SCRIPT_WEB_APP_URL_HERE";
   ```

2. Replace it with the `/exec` URL from step 1 above.
3. Push `index.html` to a GitHub repo and enable **GitHub Pages** for it
   (Settings → Pages → deploy from branch).
4. `Code.gs` doesn't need to go to GitHub — it only lives in the Apps
   Script project, since that's what receives the submissions.

The page detects which context it's running in automatically: inside Apps
Script it submits via `google.script.run`; anywhere else (GitHub Pages) it
posts to `WEB_APP_URL` through a hidden iframe, which avoids CORS issues
since it's a plain form POST rather than a fetch.

## Audio narration

Each item has a speaker icon that plays a short spoken explanation from the
`audio/` folder — `q1_en.<ext>`…`q35_en.<ext>` and `q1_es.<ext>`…`q35_es.<ext>`
(see `audio-script.md` for the narration text in both languages). The
"English audio" / "Audio en Español" toggle in the intro card switches
`AUDIO_LANG` in `index.html`, which all 35 speaker icons read from.

`audio/` is ~68MB across 70 files. Where it needs to live depends on how
you're hosting `index.html`:

- **Hosting on GitHub Pages:** just commit the `audio/` folder alongside
  `index.html` — the default relative path (`AUDIO_BASE_URL = "audio/"` near
  the top of `index.html`'s `<script>`) already points at it.
- **Hosting via Apps Script instead:** Apps Script's HtmlService can't serve
  a plain folder of static files over relative paths the way GitHub Pages
  can. Host `audio/` on GitHub Pages regardless (even if the form itself
  runs from Apps Script) and change `AUDIO_BASE_URL` in `index.html` to that
  folder's full URL, e.g. `"https://yourname.github.io/your-repo/audio/"`.

If a clip fails to load, the speaker icon just does nothing (check the
browser console for a "failed to load" message) rather than blocking the
form — a missing or mis-pointed audio file never prevents someone from
completing and submitting the evaluation.

## Editing the checklist

The 35 evaluation items live in two places that must stay in sync:

- `index.html` → the `SECTIONS` array (drives what's shown and the field
  names `q1`…`q35`).
- `Code.gs` → the `QUESTIONS` array (drives the Sheet's column headers).

If you add, remove, or reorder an item, update both in the same order.

## Viewing responses

Open the Apps Script project → **Project Settings** (gear icon) →
**Script Properties**, or run `getSheet_()` once from the editor and check
**Executions** for the returned Sheet URL — either way it points to the
"Forklift Operator Evaluations" spreadsheet, sheet tab "Responses".
