import platform as pl
import os

# This module deals with platform-specific paths

# Set the platform we are currently running on
if pl.system().lower().startswith('windows'):
  platform =  'windows'
elif pl.system().lower().startswith('darwin'):
  platform = 'mac'
else:
  platform = 'linux'

def getDirHierarchy(scriptname):
  return (personaldir(scriptname),
          systemdir(scriptname),
          localdir())

# The personal directory for settings storage.
# The settings location in the "home" directory for a user.
def personaldir(app_name):
  if platform == 'windows':
    return os.path.join(os.environ['APPDATA'], app_name)
  else:
    return os.path.expanduser('~/.{}/'.format(app_name))

# The system directory for settings storage.
# Usually the default "/etc" directory.
def systemdir(app_name):
  if platform == 'windows':
    return os.path.join(os.environ['ProgramFiles'], app_name)
  else:
    return "/etc/{}/".format(app_name)

# The local directory for settings storage.
# Located in the same place as the rest of the modules
# @TODO This should work, but could do with some testing
def localdir(subdir="settings"):
  # Method for getting dir taken from wxPython project
  root = __file__
  if os.path.islink (root):
    root = os.path.realpath (root)
  directory = os.path.dirname (os.path.abspath (root))
  return os.path.join(directory, subdir)

# Searches through the directory hierarchy for a file/path named "filename"
# If 'strict' is false, it returns a path where the file can be placed if there
# is no existing file.
# If 'strict' is true, returns None there is no existing file.
def getExistingFile(appname, filename, strict = False):
  path = None
  # First check to see if the queue file exists anywhere
  for d in getDirHierarchy(appname):
    if os.path.exists(d):
      filepath = os.path.join(d, filename)
      if os.access(filepath, os.W_OK):
        path = filepath
        break
  # Now try to create a queue file in one of the dirs
  if path is None and not strict:
    for d in getDirHierarchy(appname):
      if not os.path.exists(d):
        try:
          os.mkdir(d)
        except:
          pass
      filepath = os.path.join(d, filename)
      if os.access(d, os.R_OK):
        path = filepath
        break
  return path
