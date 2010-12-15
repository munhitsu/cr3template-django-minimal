from fabric.api import *
from fabric.decorators import runs_once
from fabric.context_managers import cd

import os

HOME = os.environ['HOME']
USER = os.environ["USER"]

env.user = "update me !!!"


remote_repo_sub_dir = "repos/git/django_site.git"
remote_site_dir = "django_site"

#usefull shortcut
def prod():
    env.hosts = ["ichi.cr3studio.com",]

def cert():
    env.hosts = ["alf.cr3studio.com",]

def dev():
    env.hosts = ["alf.cr3studio.com",]



#helper functions
class memoized(object):
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

@memoized
def get_remote_home_dir():
    return run("echo $HOME")

@memoized
def get_remote_repo_dir():
    return  os.path.join(get_remote_home_dir(),remote_repo_sub_dir)

@memoized
def get_remote_site_dir():
    return  os.path.join(get_remote_home_dir(),remote_site_dir)



#operations
def init_master_repo():
    """
    Initializes master repository
    """
    run("mkdir -p %s" % get_remote_repo_dir())
    with cd(get_remote_repo_dir()):
        run("git config --global user.name '%s'" % env.user)
        run("git config --global user.email %s@%s" % (env.user,env.host))
        run("git --bare init")
        with cd("hooks"):
            put("hooks/post-update",os.path.join(get_remote_repo_dir(),"hooks"), mode=0755)

def init_master_site():
    """
    Initializes django_site on master server (connected to master repository)
    """
    run("git clone %s" % get_remote_repo_dir())
#    with cd(get_remote_site_dir()):
#        run("git --bare init")
#        with cd("hooks"):
#            put("hooks/post-update",os.path.join(get_remote_repo_dir(),"hooks"), mode=0755)
    

def connect_local():
    """
    Connects local repository with remote
    """
    #TODO: pobierac dane przez webapi z admin?
    #TODO: extend admin with web api based on django-piston
    remote_user = env.user
    remote_repo_server = "ichi.cr3studio.com"
    local("git remote add origin ssh://%s@%s%s" % 
        (remote_user,remote_repo_server,get_remote_repo_dir()))
    local("git config branch.master.remote origin")
    local("git config branch.master.merge refs/heads/master")


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
    
