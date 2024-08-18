import random

SOURCE_FILE = "charade_words.md"
COMPLETED_WORDS_FILE = "charade_printed.md"


########################################################################
def sync_with_git(action, file=None):
    from git import Repo
    repo = Repo('.')
    if action == 'push':
        repo.git.add(file)
        repo.index.commit('[auto] syncing done words.')
        origin = repo.remote(name='origin')
        origin.push()
    elif action == 'clean':
        repo.git.restore(file)
    elif action == 'pull':
        repo.git.pull()
    else:
        print("unknown command")


try:
    import sys
    if len(sys.argv) == 2:
        command = sys.argv[1]
        if command in ("push"):
            print("pushing to git...")
            sync_with_git('push', COMPLETED_WORDS_FILE)
            print("pushed")
            sys.exit()
        elif command in ("clean", "restore", "discard"):
            print("cleaning...")
            sync_with_git('clean', COMPLETED_WORDS_FILE)
            print("cleaned")
            sys.exit()
        elif command in ("pull"):
            print("pulling...")
            sync_with_git('pull')
            print("pulled")
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
