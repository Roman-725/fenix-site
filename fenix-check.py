"""Small dependency-free check: python fenix-check.py."""
from html.parser import HTMLParser
from pathlib import Path


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.assets = []
        self.headings = 0
        self.notes = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "h1":
            self.headings += 1
        if "note" in attrs.get("class", "").split():
            self.notes += 1
        if tag == "a":
            self.links.append(attrs.get("href", ""))
            if attrs.get("target") == "_blank":
                assert "noopener" in attrs.get("rel", ""), "Unsafe external link"
        if tag == "img":
            assert attrs.get("alt"), "Missing image description"
        if tag in ("script", "img"):
            self.assets.append(attrs.get("src", ""))
        if tag == "link":
            self.assets.append(attrs.get("href", ""))


root = Path(__file__).resolve().parent
page = Page()
page.feed((root / "fenix.html").read_text(encoding="utf-8"))
assert page.headings == 1, "Expected one h1"
assert len(page.ids) == len(set(page.ids)), "Duplicate IDs"
assert page.notes == 9, "Expected nine review notes"
for link in page.links:
    assert link and link != "#", "Empty link"
    if link.startswith("#"):
        assert link[1:] in page.ids, f"Broken anchor: {link}"
for asset in page.assets:
    assert (root / asset).is_file(), f"Missing asset: {asset}"
assert "noindex" in (root / "fenix.html").read_text(encoding="utf-8")
print("OK: anchors, assets, review notes, image descriptions and external link safety")
