class Dot:
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates

    def __str__(self) -> str:
        return "[id: {}, coordinates: {}]".format(self.id, self.coordinates)

    def __repr__(self) -> str:
        return self.__str__()


