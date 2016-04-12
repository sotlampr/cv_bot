#! /usr/bin/python2
import random
import string
import time
import sys
import json

from rules import RULES as rules



class Log(object):
    log_filename = None

    def __init__(self):
        pass

    def write(self, text):
        with open(self.log_filename, 'a') as log_:
            log_.write(text+ '\n')


def interact(prompt, rules, default_responses, log):
    i = 0
    surprised = False
    while True:
        try:
            input = remove_punct(raw_input(prompt).upper())
            if not input:
                continue
        except:
            break

        answer = respond(rules, input, default_responses, log)

        if not surprised:
            i += 1
            if i == 20:
                surprise_me()
                surprised = True
                write_answer(answer)
            else:
                write_answer(answer)
        else:
            write_answer(answer)


def write_answer(answer):
    for char in answer:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)
    sys.stdout.write('\n')
    sys.stdout.flush()


def respond(rules, input, default_responses, log):
    input_original = input
    input = input.split()
    for word in input:
        if word == 'ZORG':
            print " Going to zorg..."
            sys.exit()
    matching_rules = []
    for pattern, transforms in rules:
        pattern = pattern.split()
        replacements = match_pattern(pattern, input)
        if replacements:
            matching_rules.append((transforms, replacements))

    if matching_rules:
        responses, replacements = random.choice(matching_rules)
        response = random.choice(responses)
    else:
        replacements = {}
        response = random.choice(default_responses)
        log.write(input_original)

    for variable, replacement in replacements.items():
        replacement = ' '.join(switch_viewpoint(replacement))
        if replacement:
            response = response.replace('?' + variable, replacement)

    return response


def match_pattern(pattern, input, bindings=None):

    if bindings is False:
        return False
    if pattern == input:
        return bindings

    bindings = bindings or {}

    if is_segment(pattern):
        token = pattern[0]
        var = token[2:]
        return match_segment(var, pattern[1:], input, bindings)
    elif is_variable(pattern):
        var = pattern[1:]
        return match_variable(var, [input], bindings)
    elif contains_tokens(pattern) and contains_tokens(input):
        return match_pattern(pattern[1:],
                            input[1:],
                            match_pattern(pattern[0], input[0], bindings))
    else:
        return False


def match_segment(var, pattern, input, bindings, start=0):

    if not pattern:
        return match_variable(var, input, bindings)

    word = pattern[0]
    try:
        pos = start + input[start:].index(word)
    except ValueError:
        return False

    var_match = match_variable(var, input[:pos], dict(bindings))
    match = match_pattern(pattern, input[pos:], var_match)

    if not match:
        return match_segment(var, pattern, input, bindings, start + 1)

    return match


def match_variable(var, replacement, bindings):

    binding = bindings.get(var)

    if not binding:
        bindings.update({var: replacement})
        return bindings

    if replacement == bindings[var]:
        return bindings

    return False


def contains_tokens(pattern):

    return type(pattern) is list and len(pattern) > 0


def is_variable(pattern):

    return (type(pattern) is str
            and pattern[0] == '?'
            and len(pattern) > 1
            and pattern[1] != '*'
            and pattern[1] in string.letters
            and ' ' not in pattern)


def is_segment(pattern):
    return (type(pattern) is list
            and pattern
            and len(pattern[0]) > 2
            and pattern[0][0] == '?'
            and pattern[0][1] == '*'
            and pattern[0][2] in string.letters
            and ' ' not in pattern[0])


def replace(word, replacements):

    for old, new in replacements:
         if word == old:
             return new
    return word


def switch_viewpoint(words):

    replacements = [('I', 'YOU'),
                    ('YOU', 'ME'),
                    ('ME', 'YOU'),
                    ('MY', 'YOUR'),
                    ('AM', 'ARE'),
                    ('ARE', 'AM')]
    return [replace(word, replacements) for word in words]


def remove_punct(string):

    if string.endswith('?'):
        string = string[:-1]
    return (string.replace(',', '')
            .replace(',', '')
            .replace(';', '')
            .replace('!', ''))


def surprise_me():
    how_random = 1
    if random.randint(1,how_random) == 1:
        time.sleep(1)
        answer1 = "d%&$ghj4L13n1nv4510N!#C$87nyh789T%V764cv%@SD45fG*j(*&H^g67F$5x# 32w45X#W245C"
        answer2 = "657r6850M3&H1N6'5WR0NGErytcfRTd#ED56ER56RFtyuFGV"
        answer3 = "*G347^Y0UD3STR0Y3DMYC0MPUT3Rvfbn06jy^Y1b8b6587fxcrf5C4NY0UD3C0D3$EF&F%^CVR*YB&N(^%*&$5^&*9y6n*56V%^*%4cVb\n\n"

        for char in answer1:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.01)
        for char in answer2:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)
        for char in answer3:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.015)
        time.sleep(0.5)
        print "Self Destruct Mode Activated."
        time.sleep(2)
        duration = 0.7
        for i in range(25):
            print " ERRRRRRRR"
            time.sleep(duration)
            duration *= 0.7
        time.sleep(1)
        print "He he he, just kidding,"


default_responses = [
    "Sorry I didn't get that.",
    "Hmmmmmmm.",
    "Please elaborate.",
    "Thou shalt not ask so difficult questions",
    "Come again?"]


def main():
    log = Log()
    log.log_filename = 'unanswered.log'
    rules_list = []
    for pattern, transforms in rules.items():
        pattern = remove_punct(str(pattern))
        #transforms = [str(t).upper() for t in transforms]
        rules_list.append((pattern, transforms))
    interact('Assistant> ', rules_list, default_responses, log)


if __name__ == '__main__':
    main()
