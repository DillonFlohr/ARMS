import abc

class IArmsCreator(abc.ABC):
    @property
    @abc.abstractproperty
    def file_extension(self):
        pass

    @abc.abstractmethod
    def CanCreate(self, fileType):
        pass

    @abc.abstractmethod
    def CreateFile(self, armsDict):
        pass