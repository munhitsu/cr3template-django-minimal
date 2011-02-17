from fabric.api import *
from fabric.decorators import runs_once
from fabric.context_managers import cd
from fabric.operations import require


import os

HOME = os.environ['HOME']
USER = os.environ["USER"]

PROJECT = os.path.split(os.path.dirname(__file__))[-1]
#EDIT: in case one needs to store project in different directory - change following line
env.user = PROJECT


remote_repo_sub_dir = "repos/git/django_site.git"
remote_site_dir = "django_site"

#EDIT: may depend on specific customer
env.roledefs = {
    'prod': ["ichi.cr3studio.com",],
    'cert': ["alf.cr3studio.com",],
    'dev' : ["alf.cr3studio.com",],
}


#helper functions
class _memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)

@_memoized
def _get_remote_home_dir():
    return run("echo $HOME")

@_memoized
def _get_remote_repo_dir():
    return  os.path.join(_get_remote_home_dir(),remote_repo_sub_dir)

@_memoized
def _get_remote_site_dir():
    return  os.path.join(_get_remote_home_dir(),remote_site_dir)



#operations
def init_remote_repo():
    """
    Initializes remote git repository and configures post-hook
    """
    run("mkdir -p %s" % _get_remote_repo_dir())
    with cd(_get_remote_repo_dir()):
        run("git config --global user.name '%s'" % env.user)
        run("git config --global user.email %s@%s" % (env.user,env.host))
        run("git --bare init")
        with cd("hooks"):
            put("hooks/post-update",os.path.join(_get_remote_repo_dir(),"hooks"), mode=0755)

def init_remote_site():
    """
    Initializes django_site on master server (connected to master repository)
    """
    run("git clone %s" % _get_remote_repo_dir())
#    with cd(_get_remote_site_dir()):
#        run("git --bare init")
#        with cd("hooks"):
#            put("hooks/post-update",os.path.join(get_remote_repo_dir(),"hooks"), mode=0755)
    

def configure_remote_branch(remote=None,branch=None):
    """
    Connects local repository with remote
    """
    if branch is None:
        branch = env.roles[0]
    if remote is None:
        remote = env.roles[0]
    #TODO: pobierac dane przez webapi z admin?
    #TODO: extend admin with web api based on django-piston
    remote_user = env.user
    remote_repo_server = env.host
    with settings(warn_only=True):
        local("git remote rm %s" % remote, capture=False)
    local("git remote add %s ssh://%s@%s%s" % 
        (remote,remote_user,remote_repo_server,_get_remote_repo_dir()))
    local("git config branch.%s.remote %s" % (branch,remote))
    local("git config branch.%s.merge refs/heads/%s" % (branch,branch))


def ssh_keygen():
    """
    SSH key generation
    """
    dsa_filename = os.path.join(HOME, '.ssh', 'id_dsa')
    local("ssh-keygen -t dsa -P '' -f %s" % dsa_filename)


def ssh_register():
    """
    Upload public SSH key for login automation.
    """
    f = open(os.path.join(HOME, '.ssh', 'id_dsa.pub'), 'r')
    pubkey = f.read()
    run("mkdir -p ~/.ssh 2>/dev/null; chmod 700 ~/.ssh; echo '%s' >> ~/.ssh/authorized_keys; chmod 644 ~/.ssh/authorized_keys" % pubkey)
    
def ssh_remote_pubkey():
    """
    Returns remote pubkey
    """
    run("cat ~/.ssh/id_dsa.pub")

def ssh_remote_keygen():
    """
    SSH key generation - remote
    """
    dsa_filename = os.path.join(_get_remote_home_dir(), '.ssh', 'id_dsa')
    run("ssh-keygen -t dsa -P '' -f %s" % dsa_filename)
    ssh_remote_pubkey()
