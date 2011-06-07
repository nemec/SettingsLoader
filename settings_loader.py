import platformdata
import os

class Settings(object):

  config_ext = ".conf"

  def __init__(self, app_name, default_settings = {}, config_ext=None):
    # Turn keys in default_settings to uppercase
    default_settings = dict(zip(map(lambda x: x.upper(),
                                    default_settings.keys()),
                                default_settings.values()))
    if config_ext is not None:
      self.config_ext = "." + config_ext.lstrip(".")
    self.__settings = default_settings
    self.__appname = app_name
    self.__initialized = True


  # Allows access to setting through Settings()[key]
  def __getitem__(self, key):
    return self.__settings.get(key.upper(), None)


  # Allows access to setting through Settings().key
  # Only if key isn't already a function/object in the class
  def __getattr__(self, key):
    return self[key]


  def __setattr__(self, item, value):
    print self.__dict__
    if not "_Settings__Initialized" in self.__dict__:
      return object.__setattr__(self, item, value)
    elif item in self.__dict__:
      object.__setattr__(self, item, value)
    else:
      self.__setitem__(item, value)


  def save_settings(self, filename = None):
    if not filename:  
      filename = self.__appname
    filepath = platformdata.getExistingFile(self.__appname, filename + self.config_ext, False)
    with open(filepath, "w") as settingsFile:
      for k in self.__settings:
        settingsFile.write("%s = %s\n" % (k, self.__settings[k]))


  # @TODO create the file if not exists
  def create_settings_file(self, filename):
    pass


  def load_settings(self, filename = None):
    data = None
    if not filename:  
      filename = self.__appname
    filepath = platformdata.getExistingFile(self.__appname, filename + self.config_ext, True)
    if not filepath:
      raise IOError("Cannot find settings file %s.conf" % filename)
    with open(filepath,"r") as settingsFile:
        data = settingsFile.readlines()
    if data != None:
      for line in data:
        line = line.strip()
        if len(line) == 0:
          continue
        # Lines beginning with # are comments
        if line[0]=='#':
          continue
        ix = line.find('=')
        if ix < 0:
          continue
        self.__settings[line[0:ix].strip().upper()]=line[ix+1:].strip()


  def __str__(self):
    return repr(self.__settings)


def test():
  val = "value"
  s = Settings("settings_test", {"test": val})
  if s.test != val:
    raise Exception("Test value is %s" % s.test)
  s.save_settings()
  d = Settings("settings_test")
  d.load_settings()
  if d.test != val:
    raise Exception("Test value is {}, should be '{}'.".format(d.test, val))

if __name__ == "__main__":
  test()

