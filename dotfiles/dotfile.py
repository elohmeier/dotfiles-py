import errno


class Dotfile:
    """
    This class implements the 'dotfile' abstraction.

    A dotfile has two primary attributes:

    name -- name of dotfile in the home directory (~/.vimrc)
    target -- target the dotfile should point to (~/Dotfiles/vimrc)

    The above attributes are both py.path.local objects.

    The goal is for there to be no special logic or stored global state.  Only
    the implementation of three operations made available to the caller:

    add -- moves a dotfile into the repository and replaces it with a symlink
    remove -- the opposite of add
    sync -- ensure that each repository file has a corresponding symlink

    This is where most filesystem operaitons (link, delete, etc) should be
    called, and not in the layers above.
    """

    def __init__(self, name, target):
        self.name = name
        self.target = target

    def add(self):
        if self.target.check(exists=1):
            raise OSError(errno.EEXIST, self.target)
        self.name.move(self.target)
        self.sync()

    def remove(self):
        if self.target.check(exists=0):
            raise OSError(errno.ENOENT, self.target)
        self.name.remove()
        self.target.move(self.name)

    def sync(self):
        self.name.mksymlinkto(self.target)
