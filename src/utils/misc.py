import os


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


def get_extensions():
    extensions = []
    for directory in os.listdir("src/cogs"):
        if directory.endswith(".py"):
            extensions.append(f"src.cogs.{directory[:-3]}")

        if os.path.isdir(directory):
            for inner_directory in os.listdir(directory):
                if inner_directory.endswith(".py"):
                    extensions.append(
                        f"src.cogs.{directory}.{inner_directory[:-3]}")

    return extensions
