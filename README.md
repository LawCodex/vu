# LawCodex — Vanuatu (`vu`)

The **Constitution of the Republic of Vanuatu** (English text, *Laws of the Republic of Vanuatu,
Consolidated Edition 2020*) as plain Markdown, from the Parliament of Vanuatu website.

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as Markdown in git.

Retrieved: **2026-10-13**. Status: **minimal** (Constitution only).

## Contents

| File | Notes |
|---|---|
| `constitution/constitution-of-the-republic-of-vanuatu-en.md` | Consolidated English version (Consolidated English Version Order, commenced 29 April 2020; amendments up to Act 27 of 2013); 95 Articles, Schedules |

## What is NOT covered, and why

- **Acts and subsidiary legislation.** The Parliament of Vanuatu site
  (<https://parliament.gov.vu>, *Acts of Parliament*, *Vanuatu Consolidated Legislation*,
  *Vanuatu Subsidiary Legislation*) does not host the texts itself — every Act is a link to
  PacLII (`paclii.org/vu/...`), which is behind a bot challenge (HTTP 403 "Just a moment…") and
  was therefore not used. No other official online source of Vanuatu legislation was reachable
  (`vanuatu.gov.vu` and `legislation.gov.vu` do not respond).
- **Site terms.** parliament.gov.vu's generic *Terms & Conditions* state that its material may be
  accessed for personal use and must not be republished or redistributed. Following the LawCodex
  rule for restrictive terms, no crawl of the site was made: only the Constitution — the supreme
  law of the Republic, an official legislative text — is reproduced here. A bulk
  collection would need the Parliament's (or the State Law Office's) consent.
- The French and Bislama versions of the Constitution (both also official) are not published on the site.

## Sources

- <https://parliament.gov.vu/index.php/parliamentary-business/constitution> →
  <https://parliament.gov.vu/images/constitution.pdf> (single request, identifying User-Agent).
- Text extracted with poppler `pdftotext`; running headers/page numbers and the arrangement of
  articles removed. Headings: `## CHAPTER …`, `### PART …`, `#### Article N. heading`.
  Not an official version.

## Regenerate

```sh
python3 scripts/vu_fetch_convert.py ../_raw/vu .
```
