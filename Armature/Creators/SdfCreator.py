from Interfaces import IArmsCreator
import re

class SdfCreator(IArmsCreator.IArmsCreator):
    @property
    def file_extension(self):
        return ".sdf"

    def CanCreate(self, fileType):
        return re.search('--sdf', fileType, re.I) != None

    def CreateFile(self, armsDict):
        raise NotImplementedError()