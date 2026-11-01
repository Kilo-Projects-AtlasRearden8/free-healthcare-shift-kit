#!/usr/bin/env python3
"""Validation for the Free Healthcare Shift Kit (Asdale Dynamics, LLC)."""
import html.parser
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(ROOT)
failures = []


def fail(msg):
    failures.append(msg)
    print("FAIL: " + msg)


class TagChecker(html.parser.HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stack = []
        self.void = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in self.void:
            return
        if not self.stack:
            fail(f"{self.name}: closing </{tag}> with no open tag")
            return
        if self.stack[-1] != tag:
            fail(f"{self.name}: expected </{self.stack.pop()}> before </{tag}>")
        else:
            self.stack.pop()

    def finish(self):
        for tag in self.stack:
            fail(f"{self.name}: unclosed <{tag}>")


def check_html(path):
    print("checking " + os.path.relpath(path, PROJECT))
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if "<!DOCTYPE html>" not in content[:200]:
        fail(path + ": missing doctype")
    parser = TagChecker(os.path.basename(path))
    parser.feed(content)
    parser.finish()
    for marker in ["Asdale Dynamics, LLC", "Education only", "@media print"]:
        if marker not in content:
            fail(path + ": missing marker '" + marker + "'")
    if os.path.basename(path) != "index.html" and "no-print" not in content:
        fail(path + ": missing marker 'no-print'")


EXPECTED_HTML = {
    "index.html",
    "brain-sheet.html",
    "handover-template.html",
    "ce-tracker.html",
    "medication-log.html",
}
EXPECTED_MD = {
    "brain-sheet.md",
    "handover-template.md",
    "ce-tracker.md",
    "medication-log.md",
}


def main():
    files = []
    for dirpath, _dirnames, filenames in os.walk(PROJECT):
        if ".git" in dirpath:
            continue
        for fn in filenames:
            files.append(os.path.join(dirpath, fn))

    html_files = [p for p in files if p.endswith(".html")]
    md_files = [p for p in files if p.endswith(".md")]
    rel_html = {os.path.relpath(p, PROJECT) for p in html_files}
    rel_md = {os.path.relpath(p, PROJECT) for p in md_files}

    missing_html = EXPECTED_HTML - rel_html
    missing_md = EXPECTED_MD - rel_md
    if missing_html:
        fail("missing HTML: " + ", ".join(sorted(missing_html)))
    if missing_md:
        fail("missing Markdown: " + ", ".join(sorted(missing_md)))

    for p in sorted(html_files):
        check_html(p)

    # Secrets scan
    secret_re = re.compile(r"(?i)(api[_-]?key|secret[_-]?key|password|access[_-]?token|private[_-]?key|sk_live|sk_test)")
    for p in files:
        rel = os.path.relpath(p, PROJECT)
        if rel.startswith(".git/") or rel == "LICENSE" or rel == "tests/validate.py":
            continue
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except OSError:
            continue
        for m in secret_re.finditer(content):
            fail(rel + ": possible secret '" + m.group(0) + "'")

    # Copyright line exact
    lic = os.path.join(PROJECT, "LICENSE")
    with open(lic, encoding="utf-8") as f:
        lic_lines = f.read().splitlines()
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in lic_lines:
        fail("LICENSE: copyright line not exact")
    if lic_lines[2] != "Copyright (c) 2026 Asdale Dynamics, LLC":
        fail("LICENSE: copyright line not on line 3 exactly")

    # README credit
    readme = os.path.join(PROJECT, "README.md")
    with open(readme, encoding="utf-8") as f:
        readme_content = f.read()
    if "Asdale Dynamics, LLC" not in readme_content:
        fail("README.md: missing Asdale Dynamics, LLC credit")
    if "Copyright (c) 2026 Asdale Dynamics, LLC" not in readme_content:
        fail("README.md: missing copyright line")

    # No .github/workflows
    wf = os.path.join(PROJECT, ".github", "workflows")
    if os.path.isdir(wf):
        fail(".github/workflows present (should not be created)")

    print()
    if failures:
        print(f"{len(failures)} failure(s)")
        sys.exit(1)
    print("All checks passed.")
    print(f"HTML files: {len(html_files)}  Markdown files: {len(md_files)}")


if __name__ == "__main__":
    main()
