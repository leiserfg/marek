import os
from datetime import datetime

from marek.input import get_input
from marek import project
from marek.transformers import debianize

now = datetime.now()
now_t = now.strftime("%a, %d %b %Y %H:%M:%S +0200")

postclone_scripts = [
    "init_git.sh"
]

data = {
   "deb_name": get_input("Debian package name", project.name, debianize),
   "deb_maintainer": get_input("Debian maintainer", os.environ.get("DEBFULLNAME", None)),
   "deb_email": get_input("Debian email", os.environ.get("DEBEMAIL", None)),
   "deb_description": get_input("Debian description", "Debian package for %s" % project.name),
   "deb_now": now_t,
   "gitignore": ".gitignore"
}
