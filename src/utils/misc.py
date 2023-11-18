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


def parse_time(time):
    days = time // (60 * 60 * 24)
    time %= (60 * 60 * 24)
    hours = time // (60 * 60)
    time %= (60 * 60)
    minutes = time // 60
    time %= 60
    seconds = time

    time_parts = []

    if days:
        time_parts.append(f"{days} {'day' if days == 1 else 'days'}")
    if hours:
        time_parts.append(f"{hours} {'hour' if hours == 1 else 'hours'}")
    if minutes:
        time_parts.append(
            f"{minutes} {'minute' if minutes == 1 else 'minutes'}")
    if seconds:
        time_parts.append(
            f"{seconds} {'second' if seconds == 1 else 'seconds'}")

    if len(time_parts) == 0:
        return "0 seconds"
    if len(time_parts) == 1:
        return time_parts[0]
    if len(time_parts) == 2:
        return f"{time_parts[0]} and {time_parts[1]}"
    return f"{', '.join(time_parts[:-1])}, and {time_parts[-1]}"


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
