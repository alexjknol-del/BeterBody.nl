# -*- coding: utf-8 -*-
"""Bouwt site/ uit site.zip.

Vanaf 02-10-2026 is site.zip de bron: een volledige kopie van de live site.
De eerdere generator staat in de git-geschiedenis.
Bijwerken: nieuwe site.zip uploaden en committen; Cloudflare draait
`python3 build.py` en publiceert site/.
"""
import shutil
import zipfile

shutil.rmtree("site", ignore_errors=True)
zipfile.ZipFile("site.zip").extractall("site")
print("site opgebouwd uit site.zip")
