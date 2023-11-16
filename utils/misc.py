def get_cases(string):

    def invert_case(letter):
        if not letter.isalpha():
            return letter
        if letter.isupper():
            return letter.lower()
        return letter.upper()

    string = list(string.upper())

    output = []
    for loop in range(2**len(string)):
        case = ""
        for index in range(len(string)):
            if loop % (2**index) == 0:
                string[index] = invert_case(string[index])
            case += str(string[index])
        output.append(case)
    return list(dict.fromkeys(output))
