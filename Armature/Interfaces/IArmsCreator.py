import abc

class IArmsCreator(abc.ABC):
    @property
    @abc.abstractproperty
    def file_extension(self):
        pass

    @abc.abstractmethod
    def can_create(self, fileType):
        pass

    @abc.abstractmethod
    def create_file(self, armsDict):
        pass