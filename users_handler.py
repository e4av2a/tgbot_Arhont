def load_users(filename="users.txt"):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        return set()


def add_user_in_file(user, filename="users.txt"):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(str(user) + '\n')