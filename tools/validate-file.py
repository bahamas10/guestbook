#!/usr/bin/env python3
"""Validate one or more guestbook contributor files (stdlib only)."""

import re
import sys
import unicodedata
from pathlib import Path

EMOJI_FILE = Path(__file__).resolve().parent.parent / "data" / "emoji-test.txt"
GRANDFATHERED = {"arch-err", "adrad1234"}
ACCEPTED = {"fully-qualified", "minimally-qualified", "unqualified"}

# Aproksimacija Unicode svojstva Default_Ignorable_Code_Point
# (stdlib ga nema), raspon po raspon.
IGNORABLE_RANGES = [
    (0x00AD, 0x00AD),
    (0x034F, 0x034F),
    (0x061C, 0x061C),
    (0x115F, 0x1160),
    (0x17B4, 0x17B5),
    (0x180B, 0x180F),
    (0x200B, 0x200F),
    (0x202A, 0x202E),
    (0x2060, 0x206F),
    (0x3164, 0x3164),
    (0xFE00, 0xFE0F),
    (0xFEFF, 0xFEFF),
    (0xFFA0, 0xFFA0),
    (0xFFF0, 0xFFF8),
    (0x1BCA0, 0x1BCA3),
    (0x1D173, 0x1D17A),
    (0xE0000, 0xE0FFF),
]


class Fail(Exception):
    pass


def is_ignorable(ch):
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in IGNORABLE_RANGES)


def is_single_grapheme(s):
    """Pojednostavljena provjera: jedan znak + eventualni combining
    markovi / variation selectori. Emoji sekvence su već pokrivene
    službenom listom, pa ovo služi samo za ne-emoji simbole."""
    if not s:
        return False
    for ch in s[1:]:
        if unicodedata.category(ch)[0] != "M" and not (0xFE00 <= ord(ch) <= 0xFE0F):
            return False
    return unicodedata.category(s[0])[0] != "M"


def load_emojis():
    try:
        text = EMOJI_FILE.read_text(encoding="utf-8")
    except OSError as e:
        sys.exit(f"FATAL cannot open emoji data: {e}")

    emojis = set()
    for line in text.splitlines():
        m = re.match(r"([0-9A-F ]+?)\s*;\s*([\w-]+)", line)
        if m and m.group(2) in ACCEPTED:
            emojis.add("".join(chr(int(p, 16)) for p in m.group(1).split()))

    if not emojis:
        sys.exit("FATAL emoji data contains no accepted sequences")
    return emojis


def validate_file(file, emojis):
    path = Path(file)
    if path.is_symlink():
        raise Fail(f"symbolic links are not allowed: {file}")
    if not path.is_file():
        raise Fail(f"not a regular file: {file}")

    # ime filea -> github login
    if not path.name.endswith(".txt"):
        raise Fail("filename must end in .txt")
    login = path.name[:-4]
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,38}", login):
        raise Fail("filename must contain a lowercase GitHub login")
    if "--" in login:
        raise Fail("GitHub logins cannot contain consecutive hyphens")
    if login.endswith("-"):
        raise Fail("GitHub logins cannot end with a hyphen")

    # provjere nad sirovim bajtovima
    data = path.read_bytes()
    if len(data) > 1024:
        raise Fail("file must not exceed 1024 bytes")
    if not (data.endswith(b"\n") and data.count(b"\n") == 1):
        raise Fail("file must contain exactly one newline-terminated line")
    if b"\r" in data:
        raise Fail("Windows-style CRLF line endings are not allowed")

    try:
        line = data[:-1].decode("utf-8")
    except UnicodeDecodeError:
        raise Fail("file must be valid UTF-8")

    # re.ASCII: bez toga bi re.I npr. 'ſ' prihvatio kao 's'
    m = re.fullmatch(r"([^ ]+) was here (.+)", line, re.I | re.S | re.A)
    if not m:
        raise Fail("expected: <username> was here <char>")
    have_login, symbol = m.groups()

    if not re.fullmatch(r"[A-Za-z0-9-]+", have_login):
        raise Fail("username may contain only ASCII letters, numbers, and hyphens")
    if have_login.lower() != login:
        raise Fail("username must match the lowercase filename (case-insensitive)")

    # emoji iz službene liste su uvijek OK
    if symbol in emojis:
        return

    # inače: točno jedan vidljivi grapheme
    if not is_single_grapheme(symbol):
        raise Fail("the final item must be exactly one visible Unicode character")

    if all(unicodedata.category(c)[0] in "ZC" for c in symbol):
        raise Fail("the final character cannot be whitespace or a control character")

    if login in GRANDFATHERED:
        return

    # ne-emoji simbol mora biti jedan znak iz kategorija L, N, P, S
    is_char = (
        len(symbol) == 1
        and unicodedata.category(symbol)[0] in "LNPS"
        and not is_ignorable(symbol)
    )
    if not is_char:
        raise Fail("final symbol must be a single character or emoji")


def main(argv):
    if not argv:
        print("usage: validate-file <file.txt> [...]", file=sys.stderr)
        return 2

    emojis = load_emojis()
    code = 0
    for arg in argv:
        try:
            validate_file(arg, emojis)
            print(f"OK: {arg}")
        except (Fail, OSError) as e:
            print(f"FAIL: {arg} - {e}", file=sys.stderr)
            code = 1
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
