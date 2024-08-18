import random

SOURCE_FILE = "charade_words.md"
COMPLETED_WORDS_FILE = "charade_printed.md"


########################################################################
def git_commands(action=None, file=None):
    from git import Repo
    repo = Repo('.')
    if action == 'push':
        repo.git.add(file)
        repo.index.commit('[auto] syncing done words.')
        print(repo.git.push())
    elif action == 'clean':
        print(repo.git.restore(file))
    elif action == 'pull':
        print(repo.git.pull())
    else:
        print(repo.git.status())


try:
    import sys
    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command in ("push"):
            print("pushing to git...")
            git_commands('push', COMPLETED_WORDS_FILE)
            print("pushed")
            sys.exit()
        elif command in ("clean", "restore", "discard"):
            print("cleaning...")
            git_commands('clean', COMPLETED_WORDS_FILE)
            print("cleaned")
            sys.exit()
        elif command in ("pull"):
            print("pulling...")
            git_commands('pull')
            print("pulled")
            sys.exit()
        elif command in ("status"):
            print("status...")
            git_commands()
            sys.exit()

except Exception as catch_all:
    print("!!! sync not possible !!!")
    print(catch_all)
########################################################################

all_words = []
with open(SOURCE_FILE) as f:
    all_words = [line.rstrip() for line in f]

printed_strings = []

# openning with w+ mode allows the file to be auto generated if it doesn't exist
with open(COMPLETED_WORDS_FILE, 'r') as f:
    printed_strings = [line.rstrip() for line in f]


def print_random_strings(strings, used, total=5):
    """ get a list of strings and return 5 random from it.
    """
    random_string_list = []
    while len(random_string_list) < total:
        random_string = random.choice(strings)
        if random_string not in used:
            random_string_list.append(random_string)
            # used.append(random_string)
    used += random_string_list
    return random_string_list


random_strings = print_random_strings(all_words, printed_strings)

for i, w in enumerate(random_strings, start=1):
    print(f'{i}. {w}')

with open(COMPLETED_WORDS_FILE, 'a') as f:
    for w in random_strings:
        f.write(w + "\n")  # Write each list item on a new line
