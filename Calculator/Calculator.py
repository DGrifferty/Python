def check_input(user_input, variables):
    '''Checks input by converting every element in the equation to a
    character and then looking at the sequence of characters
    returns True and none if input is good, or false and E if it is bad,
    E will be a string and state the issue'''

    equ = user_input.split()
    conv_equ = []
    symbols = '^*+-/'
    # negative_check_indices = []
    # av = assigned variable
    # bv = bad variable - letters and numbers
    # uav = unassigned variable (just letters)
    # n = number
    # s = symbol (not brackets or =)

    for p, element in enumerate(equ):
        contains_number = False
        contains_letter = False

        if element in variables.keys():
            conv_equ.append('av')
        elif element == '(':
            conv_equ.append('(')
        elif element == ')':
            conv_equ.append(')')
        elif element == '=':
            conv_equ.append('=')
        elif element in symbols:
            conv_equ.append('s')
        else:
            for index, char in enumerate(element):
                if char in numbers:
                    contains_number = True
                    if contains_letter:
                        conv_equ.append('bv')
                        break
                elif char in alphabet:
                    contains_letter = True
                    if contains_number:
                        conv_equ.append('bv')
                        break
                elif char in ['+', '-']:
                    if index == 0:
                        continue
                    elif element[index - 1] in ['-', '+']:
                        long_symbol = True
                        continue
                    else:
                        E = 'bad element - +- in middle of element'
                        return False, E
                else:
                    E = 'bad element - not allowed element/ character'
                    return False, E

            if contains_number:
                conv_equ.append('n')
            elif contains_letter:
                conv_equ.append('uav')
            elif long_symbol:
                conv_equ.append('s')

    if 'bv' in conv_equ:
        E = 'Bv used'
        return False, E

    if '=' in conv_equ:

        # Errors - bad variable name left
        # Bad equation right -  bad assignment
        # More than one =
        allowed_combs = [['uav', '=', 'n'], ['uav', '=', 'av']]
        if conv_equ not in allowed_combs:
            if 'bv' == equ[0]:
                E = 'Invalid identifier'
            elif 'bv' == equ[2]:
                E = 'Invalid assignment'
            else:
                E = 'Invalid assignment'
            return False, E

        return True, 'Assignment'

    if 'uav' in conv_equ:
        E = 'Unassigned variable used'
        return False, E

    if conv_equ.count('(') != conv_equ.count(')'):
        if conv_equ.count('(') >= conv_equ.count(')'):
            E = 'More opening brackets than closing brackets'
        else:
            E = 'More closing brackets than opening brackets'
        return False, E

    open_count = 0

    for index, element in enumerate(conv_equ):
        # Here element can equal (, ), s, n, av
        if element == 'n':
            if index != len(conv_equ) - 1:
                if conv_equ[index + 1] not in 's)':  # right
                    E = 'Bad symbol to right of number'
                    return False, E
            if index != 0:
                if conv_equ[index - 1] not in '(s':  # left
                    E = 'Bad symbol to left of number'
                    return False, E
        elif element == 's':
            if index == 0:
                E = 'Symbol at start of equation'
                return False, E
            if index == len(conv_equ) - 1:
                E = 'Symbol at end of equation'
                return False, E
            if conv_equ[index + 1] not in '(nav':  # right
                E = 'Bad symbol to right of symbol'
                return False, E
            if conv_equ[index - 1] not in ')nav':  # left
                E = 'Bad symbol to left of symbol'
                return False, E

        elif element == 'av':
            if index != len(conv_equ) - 1:
                if conv_equ[index + 1] not in 's)':  # right
                    E = 'Bad symbol to right of number'
                    return False, E
            if index != 0:
                if conv_equ[index - 1] not in 's(':  # left
                    E = 'Bad symbol to left of number'
                    return False, E

        elif element == '(':
            open_count += 1
            # count brackets opening and closed with integers if closed, minus from open, if it goes negative close before open
            # if they are not zero at the end, bad count!
            if index == len(conv_equ) - 1:
                E = 'Opening bracket at end of equation'
                return False, E
            if conv_equ[index + 1] not in '(nav':  # right
                E = ' Bad right of opening bracket'
                return False, E
            if index != 0:
                if conv_equ[index - 1] not in '(s':
                    E = 'Bad left of opening bracket'
                    return False, E

        elif element == ')':
            open_count -= 1
            if open_count < 0:
                E = 'Closed bracket before open bracket'
                return False, E
            if index != len(conv_equ) - 1:
                if conv_equ[index + 1] not in 's)':  # right
                    E = ' Bad right of closing bracket'
                    return False, E
            if index != 0:
                if conv_equ[index - 1] not in ')nav':
                    E = 'Bad left of closing bracket'
                    return False, E

    return True, 'Calculation'

    # TODO: if [n (] insert * or if )(
    # TODO: Make check input tell whether av's have been used, so they can be replaced


def is_negative(i):

    negative_count = 0
    symbol = True
    assert '-' in i
    if len(i) == 1:
        return '-'
    for index, part in enumerate(i):
        if part == '-':
            negative_count += 1
        elif part == '+':
            pass
        elif part in numbers or part in alphabet:
            p = index
            symbol = False
            break
    if not symbol:
        if negative_count % p == 0:
            return [i[:p + 1]]
        else:
            return ['-' + i[:p + 1]]
    if symbol:
        if negative_count % 2 == 0:
            return '+'
        else:
            return '-'


def define_variable(user_input, variables):
    equ = user_input.split()
    equ = ''.join(equ)
    equ = equ.split('=')

    if equ[-1] in variables.keys():
        variables[equ[0]] = variables[equ[-1]]
    else:
        variables[equ[0]] = equ[-1]

    return variables


def conv_to_float(equ, variables):
    symbols = '^*+/()'
    numbers = '1234567890'
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    requ = []

    for index, element in enumerate(equ):
        if '-' in element:
            if len(element) == 1:
                requ.append('-')
                continue
            i = is_negative(element)
            if any(part in numbers for part in i):
                equ.append(float(i))
                continue
            elif any(part in alphabet for part in i):
                if '-' in i:
                    requ.append(-float(variables(i[1:])))
                    continue
                else:
                    requ.append(float(variables[i]))
                    continue
            else:
                requ.append(i)
        elif element in symbols:
            requ.append(element)
            continue
        elif any(part in alphabet for part in element):
            requ.append(float(variables[element]))
        elif all(part in ['-', '+'] for part in element):
            requ.append(is_negative(element))
        else:
            requ.append(float(element))
    return requ


def bracket_scan(equ):
    count = 0

    for open_index, ch in enumerate(equ):
        if ch == '(':
            for closed_index, ch2 in enumerate(equ):
                if ch2 == '(':
                    if closed_index == open_index:
                        continue
                    else:
                        count += 1
                if ch2 == ')':
                    if count == 0:
                        equ[open_index:closed_index + 1] = [solve(equ[open_index + 1:closed_index])]
                        return equ
                    else:
                        count -= 1
    return equ


def solve(equ):

    while True:

        if '(' in equ:
            equ = bracket_scan(equ)
            continue
        elif '^' in equ and '(' not in equ:
            i = equ.index('^')
            q = equ[i - 1]
            for p in range(int(equ[i + 1]) - 1):
                equ[i - 1] *= q
            equ[i - 1:i + 2] = [equ[i - 1]]
            continue

        elif '/' in equ and '(' not in equ:
            i = equ.index('/')
            equ[i - 1:i + 2] = [equ[i - 1] / equ[i + 1]]
            continue
        elif '*' in equ and '(' not in equ:
            i = equ.index('*')
            equ[i - 1:i + 2] = [equ[i - 1] * equ[i + 1]]
            continue
        elif '+' in equ and '(' not in equ:
            i = equ.index('+')
            if equ[i - 2] == '-':
                equ[i - 1:i + 2] = [equ[i - 1] - equ[i + 1]]
            else:
                equ[i - 1:i + 2] = [equ[i - 1] + equ[i + 1]]
                continue
        elif '-' in equ and '(' not in equ:
            i = equ.index('-')
            equ[i - 1:i + 2] = [equ[i - 1] - equ[i + 1]]
            continue
        elif len(equ) == 1:
            return round(equ[0], 10)
        else:
            continue


if __name__ == '__main__':

    variables = dict()
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    numbers = '1234567890'

    while True:

        user_input = input()

        if user_input == '':
            continue

        elif user_input[0] == '/':
            if user_input == "/exit":
                print('Bye!')
                exit()
            elif user_input == '/help':
                print('This program will calculate the sum of a user'
                      'enter list of numbers separated by spaces.\n'
                      'It can calculate equations containing +, -, *, / (), ^ only. \n'
                      'You can assign variables using = to use in a later equation.')
                continue
            else:
                print('Unknown command')
                continue

        check, type = check_input(user_input, variables)

        if not check:
            print(type)
        else:
            if type == 'Assignment':
                define_variable(user_input, variables)
            elif type == 'Calculation':
                equ = user_input.split()
                equ = conv_to_float(equ, variables)
                print(f'{user_input} = {solve(equ)}')
