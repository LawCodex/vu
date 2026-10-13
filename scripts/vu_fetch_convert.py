#!/usr/bin/env python3
"""Fetch the Constitution of the Republic of Vanuatu (Consolidated Edition 2020, English) from the
Parliament of Vanuatu website and convert it to Markdown.

Usage: vu_fetch_convert.py RAW_DIR OUT_DIR      (needs poppler `pdftotext`)
"""
import datetime, os, re, subprocess, sys
import requests

URL = "https://parliament.gov.vu/images/constitution.pdf"
UA = "LawCodex/1.0 (+https://github.com/LawCodex)"
RAW, OUT = sys.argv[1], sys.argv[2]
HDR = {"LAWS OF THE REPUBLIC OF VANUATU", "Consolidated Edition 2020", "CONSTITUTION OF THE REPUBLIC OF VANUATU"}
LABEL = re.compile(r"^(\(\w{1,6}\)|“|\")")


def fetch():
    p = os.path.join(RAW, "constitution.pdf")
    if not os.path.exists(p):
        r = requests.get(URL, headers={"User-Agent": UA}, timeout=300)
        r.raise_for_status()
        assert r.content[:5] == b"%PDF-" and b"%%EOF" in r.content[-1024:], "incomplete PDF"
        open(p, "wb").write(r.content)
    return p


def convert(p):
    txt = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", p, "-"], capture_output=True, check=True).stdout.decode()
    lines = []
    for page in txt.split("\f"):
        for l in page.split("\n"):
            s = l.strip()
            for h in HDR:  # running header glued to the last line of the previous page
                if s.endswith(h) and s != h:
                    s = s[: -len(h)].strip()
            if not s or s in HDR or re.fullmatch(r"\d{1,3}", s):
                continue
            lines.append(s)
    start = next(i for i, l in enumerate(lines) if l.startswith("WE, the people of Vanuatu"))
    lines = lines[start:]
    out, para, last = ["## Preamble"], [], 0

    def flush():
        if para:
            out.append(" ".join(para))
            para.clear()

    for i, s in enumerate(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if re.match(r"^(CHAPTER \d+|SCHEDULE \d+)\b", s):
            flush(); out.append("## " + s); continue
        if re.match(r"^PART [IVX]+\b", s, re.I):
            flush(); out.append("### " + s); continue
        m = re.match(r"^(\d{1,3}[A-Z]?)\.\s+(\S.{0,150})$", s)
        if m and not re.search(r"[.;:,]$", s):
            n = int(re.match(r"\d+", m.group(1)).group())
            if last < n <= last + 10 or (n == last and m.group(1)[-1].isalpha()):
                flush(); out.append(f"#### Article {m.group(1)}. {m.group(2)}"); last = n; continue
        if LABEL.match(s) or (para and re.search(r"[.:;]$", para[-1]) and s[:1].isupper()):
            flush()
        para.append(s)
    flush()
    return "\n\n".join(out)


def main():
    p = fetch()
    body = convert(p)
    fm = ["---", 'title: "Constitution of the Republic of Vanuatu"', 'identifier: "Laws of the Republic of Vanuatu, Consolidated Edition 2020"',
          "type: constitution", "jurisdiction: vu", "language: en", "date: 1980-07-30",
          'consolidation: "Consolidated English Version Order, commenced 29 April 2020 (amendments to Act 27 of 2013)"',
          "status: in_force", f'source: "{URL}"', 'source_page: "https://parliament.gov.vu/index.php/parliamentary-business/constitution"',
          'format_note: "text extracted from the official PDF; layout not preserved"',
          f"retrieved: {datetime.date.today().isoformat()}", "---", ""]
    out = os.path.join(OUT, "constitution", "constitution-of-the-republic-of-vanuatu-en.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(fm) + "# Constitution of the Republic of Vanuatu\n\n" + body + "\n")
    print(out, body.count("#### "))


if __name__ == "__main__":
    main()
