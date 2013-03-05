Marek
=====

Marek is a tool to create various projects like Django app or Debian package from templates. The templates are
essentially folders with a bunch of files with placeholders. The placeholders are later on filled in with the data that
you enter during package initialization.

Purpose of this README is to provide an overview of the tool and give several usage examples: how to employ existing
templates and how to create your own ones from scratch.

The key points to overview are:

- Marek CLI
- Rules file (file that describes which data is expected to be entered by the user)
- Template inheritance

Marek CLI
---------

NOTE: package depends on python-jinja2 template engine. It has to be installed in order to use the tool. Also further on
it is assumed that you are confident with jinja2 syntax. If this is not true, please read
`jinja's docs <http://jinja.pocoo.org/docs/>`_ first.

After the package is deployed on Linux box as a Debian package, the following CLI features become available.

Lets list these templates in order to make sure that they are available.

::

    marek -l

The command above shows all available templates: the default ones and the ones created by you. We will have a look at
the latest further on.

Lets create a simple Debian package called **something**. Go to the directory where you want the project to be created
and type:

::

    marek simple_deb something

What you will see afterwards is an input dialog. The dialog contains various options. Some of those have default values
(shown in square brackets) - they can be left empty. Some do not have those (like a *Debian description*) - in their
case the dialog will continue requesting the input till you type at least some text. After the project was created a GIT
repository was initialized. This is done by an additional script. The README explains how to add such scripts to your
own templates further on.

That is it. You created a simple Debian package.

Now lets try to create a debianized python package.

::

    marek simple_pydeb something

Ooops. The tool complains that project directory already exists. And asks if you want to override it. By default the
answer is no. However, lets type **y** for now.

Note: if you want to avoid the tool asking about overriding the existing directory you use **-f** option.

::

    marek simple_pydeb something -f

Also note that you could make the tool not asking you to confirm the default values by using **--quiet** or **-q**
option.

::

    marek simple_pydeb something -q

You can combine both options in order to minimize the amount of questions asked by the tool.

::

    marek simple_pydeb something -fq

Rules file
----------

Lets have a look at the *rules.py* file of **simple_deb** project template. It looks the following way:

::

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
       "deb_description": get_input("Debian description"),
       "deb_now": now_t,
       "gitignore": ".gitignore"
    }

The *rules* file is written in plain Python. It is supposed to define a **data** dictionary that shall be used as a
context by *jinja2* for template rendering. Apart from the tool itself Marek's installation has several helper functions
to ease writing project rules. For instance, **get_input** function takes three parameters. First, help message to be
shown in the interactive dialog during project creation. Second, the default value. In case of **simple_deb**
*deb_maintainer* and *deb_email* default values are taken from *DEBFULLNAME* and *DEBEMAIL* environment variables
respectively. The third parameter is a transformer function. The transformer function is supposed to get a string
parameter, process it and return the value to be used in **data** dictionary.

Apart from **data** you may see **postclone_scripts** variable. It is supposed to have a list of scripts. Language of
the scripts does not matter. But your system should be able to execute them with a dot notation (*. init_git.sh*).
Path to the scripts should be defined relatively to the project root directory.

Template inheritance
--------------------

When thinking about **simple_pydeb** template, the first thing that should come in mind is that it is a Debian package
with some python files. Debian related files already exist in **simple_deb** template. Does not make sense to have the
same files in **simple_pydeb** as well. To prevent such code duplication, in **simple_pydeb** exists **parent_tpl**
file. It has the following contents.

::

    simple_deb

It means that **simple_deb** is a parent template of **simple_pydeb**. As a result of such linking, when you create a
project based on **simple_pydeb**, the tool shall first copy all the file from **simple_deb** and then all the files
from **simple_pydeb**. If the files have similar names (and paths), **simple_deb** versions are overwritten.

Although overwriting is OK in 99% of cases sometimes it makes sense to overwrite only a part of the file. This is where
*jinja2* comes into the game.

Lets have a look at *debian/control* file of **simple_deb**. It looks like this:

::

    Source: {{deb_name}}
    Section: misc
    Priority: optional
    Maintainer: {{deb_maintainer}} <{{deb_email}}>
    Build-Depends: debhelper (>= 7.0.50~)
    Standards-Version: 3.8.4


    Package: {{deb_name}}
    Architecture: all
    Depends: ${python:Depends},
             ${misc:Depends}
    Description: {{deb_description}}


    {% block extra %}{% endblock %}

There are placeholders in curly brackets. They get their values from the rules file. And also there is an **extra**
block.

Now lets have a look at the *control* file of **simple_pydeb** template.

::

    {% block extra %}
    Package: {{deb_name}}-doc
    Section: doc
    Architecture: all
    Depends: ${misc:Depends}
    Description: {{deb_name}} documentation
    {% endblock %}

    {[EXTEND]}

What it has is the **{[EXTEND]}** flag that tells Marek tool that the file should not overwrite the parent, but extend
it instead using template inheritance mechanism. In addition to the flag there is an **extra** block that overwrites
the same block in *debian/control* file of **simple_deb** template.

Template inheritance chain can be as long as you need. For instance, you might want to have a **django_deb** template
that would inherit from **simple_pydeb**. If you want to experiment with your own templates you do not need to modify
Marek's sources and rebuild the package. Instead, just store the template in *~/.marek* directory. The tool is able to
find user templates there as well.

One more point to have a look at. Lets open **simple_pydeb** *rules* file.

::

    import os
    from marek.input import get_input
    from marek import project
    from marek.transformers import debianize, pythonize

    data = {
       "python_name": get_input("Python package name", project.name, pythonize),
    }

    extend = True

Since **simple_deb** already has debian related data being requested from the user, there is no point to have the same
code in **simple_pydeb**. To make sure that the tool merges data attribute from parent and child template, you should
define *extend = True* parameter in the child rules file. If some of the keys collide, child values have a priority.
The tool also combines *postclone_scripts* from several rules files and makes sure that there are no duplicated values
in there (every script is mentioned only once).

In case if you inherit from a parent template some file that you do not need, put *{[IGNORE]}* flag inside that file in
the child template and it shall be dropped.
