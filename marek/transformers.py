import re


def pythonize(string):
    string = string.lower().replace(" ", "_").replace("-", "_")
    string = re.sub(r'[^\w]', '', string) # leave alphanumerics and underscores only
    return string


def debianize(string):
    string = pythonize(string)
    return string.replace("_", "-")
