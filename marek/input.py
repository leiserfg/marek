from marek import project


def get_input(help_message, default=None, transformer=[]):
    """ Gets input from keyboard and processes it """
    if not isinstance(transformer, list):
        transformer = [transformer]
    if default is not None:
        for call in transformer:
            default = call(default)
        if project.quiet:
            return default
        help_message = "%s [%s]: " % (help_message, str(default))
    else:
        help_message = "%s: " % help_message
    data = raw_input(help_message)
    while not data and default is None:
        print "There is not default for this placeholder. Please enter some value or cancel the creation process."
        data = raw_input("[mandatory] %s" % help_message)
    if data:
        trans_data = data
        for call in transformer:
            trans_data = call(data)
        if data != trans_data:
            print "Your input was transformed from '%s' to '%s'" % (data, trans_data)
        data = trans_data
    return data or default
