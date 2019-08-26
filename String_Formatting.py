def format_number_string(start, number, precision, length):
    number = round_to_precision(number, precision)
    s = '| ' + start
    for i in range(length - 2 - (len(s) + len(number))):
        s += ' '
    s += number
    s += ' |'
    return s


def format_coordinate(description, n1, n2, length):
    c = " (" + str(n1) + ", " + str(n2) + ")"
    s = '| ' + description
    for i in range(length - 2 - (len(s) + len(c))):
        s += ' '
    s += c
    s += ' |'
    return s


def format_string(description, n1, length):
    s = '| ' + description
    for i in range(length - 2 - (len(s) + len(str(n1)))):
        s += ' '
    s += str(n1)
    s += ' |'
    return s


def round_to_precision(number, precision):
    """
    Rounds a number to two decimal places
    :param precision:
    :param number: The float that is to be rounded
    :return: a rounded float in the form of a string
    """
    str_format = "{0:." + str(precision) + "f}"
    return str_format.format(number)
