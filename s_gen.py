"""
s(hape)_gen.py
"""

from collections import namedtuple
from random import randint, uniform
from html_f import HtmlComponent, CircleShape, RectangleShape, EllipseShape, Position, rgb
from typing import List, Tuple, Any, Dict

RandomRange = namedtuple("RangeTuple", ["min", "max", "is_float"])
def _RandomRange_repr(self) -> str:
    """override to make the tuple print nice"""
    return f"{self.min} to {self.max}{' float' if self.is_float else ''}"
RandomRange.__repr__ = _RandomRange_repr

class PyArtConfig:
    """

    
    PyArtConfg
    The config used in generating random shapes.

    The constructor takes normal tuples for maximum ease of use  

    Instance Variables:

    Methods:
        get_config(self) -> Dict[str, RandomRange]: Returns the configuration values as a dictionary
    
    """
    SHA = [0, 1, 3]
    X = RandomRange(0,500, False)
    Y = RandomRange(0,300, False)
    RAD = RandomRange(0,100, False) 
    RX = RandomRange(10,30, False) 
    RY = RandomRange(10,30, False)
    W = RandomRange(10,100, False) 
    H = RandomRange(10,100, False) 
    R = RandomRange(0,255, False) 
    G = RandomRange(0,255, False)
    B = RandomRange(0,255, False)
    OP = RandomRange(0,1, True)

    # copy all config relate attribute setting into _data for ease of programming
    _data = {}
    _init_data = False

    def __init__(self, 
                SHA: List[int] = [0,1,3],
                X: Tuple[int, int] = (0, 500),
                Y: Tuple[int, int] = (0, 300),
                RAD: Tuple[int, int] = (10, 30), 
                RX: Tuple[int, int] = (10,30), 
                RY: Tuple[int, int] = (10,30),
                W: Tuple[int, int] = (10,100), 
                H: Tuple[int, int] = (10,100), 
                R: Tuple[int, int] = (0,255), 
                G: Tuple[int, int] = (0,255), 
                B: Tuple[int, int] = (0,255), 
                OP: Tuple[float, float] = (0, 1)
                ):
        """
        PyArtConfig
        The acceptable ranges of random values for art generation

        Args:
            SHA (List[int]): The list of accepted shapes (0=circle, 1=rectangle, 3=ellipse)
            X (Tuple[int, int], optional): X Position Range. Defaults to (0,500).
            Y (Tuple[int, int], optional): Y Position Range. Defaults to (0,300).
            RAD (Tuple[int, int], optional): Circle Radius Range. Defaults to (0,100).
            RX (Tuple[int, int], optional): Ellipse Radius X Range. Defaults to (10,30).
            RY (Tuple[int, int], optional): Ellipse Radius Y Range. Defaults to (10,30).
            W (Tuple[int, int], optional): Rectangle Width Range. Defaults to (10,100).
            H (Tuple[int, int], optional): Rectangle Height Range. Defaults to (10,100).
            R (Tuple[int, int], optional): RGB R Range. Defaults to (0,255).
            G (Tuple[int, int], optional): RGB G Range. Defaults to (0,255).
            B (Tuple[int, int], optional): RGB B Range. Defaults to (0,255).
            OP (Tuple[int, int], optional): Opactity. Defaults to (0,1).
        """

        self._data = {}
        
        self._init_data = True # _init_data tells _setattr_ to accept new keys for self._data writing
        self.SHA = SHA
        self.X = RandomRange(*X, False)
        self.Y = RandomRange(*Y, False)
        self.RAD = RandomRange(*RAD, False)
        self.RX = RandomRange(*RX, False)
        self.RY = RandomRange(*RY, False)
        self.W = RandomRange(*W, False)
        self.H = RandomRange(*H, False)
        self.R = RandomRange(*R, False)
        self.G = RandomRange(*G, False)
        self.B= RandomRange(*B, False)
        self.OP = RandomRange(*OP, True)
        self._init_data = False

    def get_config(self) -> Dict[str, RandomRange]:
        """
        Returns a dictionary version of the config data

        Returns:
            Dict[str, RandomRange]: config data
        """
        return self._data.copy()

    def __setattr__(self, name: str, value: Any) -> None:
        """I overrode this so that we also write all config data values to a dict, for ease of formatting"""
        if name != "_init_data" and (self._init_data or name in self._data):
            self._data[name] = value
        
        super().__setattr__(name, value)

    def __str__(self) -> str:
        return "".join([f"{key}: {value}\n" for key, value in self._data.items()])
        
class RandomShape:
    """
    Generates a RandomShape 

    Instance Variables: 
        shape_data (dict[str, int|float]):
            SHA (int): The type of shape. 0=Circle, 1=Rectangle, 3=Ellipse
            X (int): X Position.
            Y (int): Y Position.
            RAD (int): Circle Radius.
            RX (int): Ellipse Radius X.
            RY (int): Ellipse Radius Y.
            W (int): Rectangle Width.
            H (int): Rectangle Height.
            R (int): RGB R.
            G (int): RGB G.
            B (int): RGB B.
            OP (int): Opactity.

    """

    # these are overwritten anyways in init (99 times out of 100) but just as a failsafe
    SHA = 0
    X = 0
    Y = 0
    RAD = 0
    RX = 10
    RY = 10
    W = 10
    H = 10
    R = 0
    G = 0
    B = 0
    OP = 1

    _shape_data = {} # like PyArtConfig, I also write the data to a dictionary for ease of access/formatting

    def __init__(self, art_config: PyArtConfig = PyArtConfig()):
        """
        New RandomShape

        Args:
            art_config (PyArtConfig, optional): The configuration used to generate the random numbers. Will create a new config using PyArtConfig's defaults if not provided.
        """
        self.SHA = art_config.SHA[randint(0, len(art_config.SHA)-1)] # pick a random shape from the list provided
        self._shape_data = {"SHA": self.SHA}

        # pick random shape

        for key, value in art_config.get_config().items():
            # if SHA 
            if key == "SHA": # this has already been handled above
                continue
            if value.is_float == True:
                new_value = round(uniform(value.min, value.max), 1)
            else:
                new_value = randint(value.min, value.max)
            # from the dictionary, update all instance attributes
            self.__setattr__(key, new_value)
            # also write to 
            self._shape_data[key] = new_value

    def __setattr__(self, name: str, value: Any) -> None:
        """having everything also in a dict makes it super easy to format into a string later"""
        if name in self._shape_data:
            self._shape_data[name] = value
        
        super().__setattr__(name, value)
    
    def as_html_component(self) -> HtmlComponent:
        """
        Returns the RandomShape as an HtmlComponent

        Returns:
            HtmlComponent: The converted RandomShape
        """
        if self.SHA == 0: # circle
            return CircleShape(Position(self.X, self.Y), self.RAD, rgb(self.R, self.G, self.B), self.OP)
        elif self.SHA == 1: # rectangle
            return RectangleShape(Position(self.X, self.Y), self.W, self.H, rgb(self.R, self.G, self.B), self.OP)
        elif self.SHA == 3: # ellipse
            return EllipseShape(Position(self.X, self.Y), self.RX, self.RY, rgb(self.R, self.G, self.B), self.OP)

        raise ValueError(f"Incorrect SHA: {self.SHA}")
    def as_Part2_line(self) -> str:
        """
        Returns the RandomShape as a string in a row format

        Returns:
            str: RandomShape string representation
        """
        return "".join([f"{round(value,1) if isinstance(value, float) else value}".rjust(3," ")+" " for key, value in self._shape_data.items()])

    def as_svg(self) -> str:
        """
        Returns the RandomShape as an svg element (as a string)

        Returns:
            str: SVG Element
        """
        return self.as_html_component().string()

    def __str__(self):
        return "".join([f"{key}: {round(value,1) if isinstance(value, float) else value}\n" for key, value in self._shape_data.items()])
            


if __name__ == "__main__":
    c1 = PyArtConfig(
        R=(200,255),
        G=(0,0),
        B=(200,255)
    )

    shape = RandomShape(art_config=c1)
    shape2 = RandomShape(art_config=c1)
    print("S1: "+shape.as_Part2_line()) 
    print("S2: "+shape2.as_Part2_line()) 
    print(shape.as_svg())
    print(shape2.as_svg())
