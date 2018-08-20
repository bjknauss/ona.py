from .load import load_config


class BaseConfigLoader():
    def __init__(self, filename=None):
        self._filename = filename
        self.reload()

    def load(self, filename):
        return load_config(filename)

    @property
    def filename(self):
        return self._filename

    def reload(self):
        self.raw_cfg = self.load(self.filename)
