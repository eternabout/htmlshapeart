"""
I was a little confused by the need of gen_art in both SvgCanvas and HtmlDocument.
I decided to implement it as follows:
HtmlDocument.gen_art() creates a new SvgCanvas, and then calls the SvgCanvas.gen_art() that actually generates the circless

Also, is this file a little overkill? Probably. But I had fun making it :)
"""

"""

HTML Component of A4

Types / Tuples:
    Size: The namedtuple containing the size information for an Svg Canvas
    Position: The namedtuple containing x and y coordinates
    rgb: The namedtuple representing an rgb value
Classes:
    HtmlDocument: Essentially the main Html handler. It is in charge of file I/O and generating the content of the file on large.
    HtmlComponent: The Super Class for Html elements. You could theoretically make any Html e3lement with it as is, but it is designed for use with created subclasses.
    Raw (HtmlComponent): The HtmlComponent SubClass for raw text. Does not support children.
    Comment (HtmlComponent): The HtmlComponent SubClass for comments. Does not support children.
    SvgCanvas (HtmlComponent): The HtmlComponent SubClass representation of an svg element
    CircleShape (HtmlComponent) : The HtmlComponent SubClass representation of an svg Circle
    

Version 1.2

"""

from collections import namedtuple
from typing import Dict

# Typing Stuff

Size = namedtuple("Size", ["width", "height"])
Position = namedtuple("Position", ["x", "y"])

rgb = namedtuple("rgb", ["red", "green", "blue"]) # lowercase on purpose. Pep8 folk chill out
#override the rgb repr
def rgb_str(object) -> str: 
    return f"rgb({object.red}, {object.green}, {object.blue})"
rgb.__repr__ = rgb_str


# Classes

class HtmlDocument:
    '''
    An HTML Document Handler

    Instance Variables:
        root (HtmlComponent): The <html> HtmlComponent
        head (HtmlComponent): The <head> HtmlComponent
        body (HtmlComponent): The <body> HtmlComponent

    Methods:
        gen_art(self) -> None: Generates the circles required for a4 part 1
        output(self) -> None: writes the HTML to the file
    '''

    def __init__(self, document_name: str = "document") -> None:   
        """
        An HTML Document Handler

        Args:
            document_name (str, optional): The name that will be used for the file. Defaults to "document".
        """
        self._doc_name = document_name 
        self.root = None
        self.head = None
        self.body = None
        
        # if no .html file extension, add one
        if document_name.endswith(".html")==False:
            self._doc_name += ".html"

        # update root, header, and body
        self._generate_skeleton()
        
        # open file for writing
        self._open_file()

    
    # Document Methods
    def _generate_skeleton(self) -> None:
        self.root = HtmlComponent(tag="html")
        self.head = HtmlComponent(tag="head")
        self.root.add(self.head)
        self.body = HtmlComponent(tag="body")
        self.root.add(self.body)

    # Assignment Specific Functions (remove if reusing this file)
    def gen_art(self) -> None:
        """
        Creates an SvgCanvas in the body and calls SvgCanvas.gen_art(), which creates the circles

        Returns:
            SvgCanvas: the SvgCanvas that contains the circles.
        """
        self.head.add(HtmlComponent(tag="title", content="My Art", indented_content=False))

        svg = SvgCanvas(Size(500, 300))
        svg.add(Comment("Define SVG drawing box"))
        self.body.add(svg)

        svg.gen_art()


    # File I/O Methods
    def output(self) -> None:
        self._write(content=self.root.string(), end_char="")
    def _write(self, content: str, end_char: str ="\n") -> None:
        '''writes the given content to self._doc_name'''
        self._file.write(content+end_char)

    def _open_file(self) -> None:
        '''opens the file self._doc_name'''
        self._file = open(self._doc_name, "w")
    
    def _close_file(self) -> None:
        '''closes the file self._doc_name'''
        self._file.close() # close and write file

    def __del__(self):
        self._close_file()

class HtmlComponent:
    '''
    The SuperClass for all HTML Element Classes. Designed for creating hyper-specific HTML object abstractions with ease via use of subclasses.  
    
    Reference for direct use of the HtmlComponent class:
        Class Variables:
            tag (str): The html tag. example in <example></example>
            indented_content (bool): Whether the content between tags should be indented

        Instance Variables:
            parent (HtmlComponent): The object above in the Hierachy
            children (list[HtmlComponet]):  The objects below in the Hierarchy
            attributes (Dict[str,str]): The attributes of the HTML element

        Methods:
            add(self, element): Makes the provided element a child of this HtmlComponent object
            new_sub_element(self, HtmlComponent_subclass, **kwargs): Creates a new instance of HtmlComponent_subclass and makes it a child of this object, and passes all **kwargs to the the constructor.
            remove(self): Removes this HtmlComponent from the Hierarchy, and all of it's children
            get_content(self): A generator that yields the initial HTML content
            string(self, indentation=0): Generates and returns the HTML for this object and all of it's childen. The indentation argument is intended as an internal argument only

    Reference for use as a SuperClass:  
        Class Variables:
            tag (str): The html tag. Override this in the SubClass definition to set a new default tag.
            indented_content (bool): Override this to set a new default value.
            _paired (bool): Whether or not the class' main element is paired by default. Override this to set a new default.
        Methods designed to be changed based upon implementation:
            get_content(self): This is the generator that yields the HTML content. It is used in the default string() method in generating the HTML. It needs to return something that is a string or has a string representation.
            _get_attribute_string(self): This returns the string of attribute's used in the HTML tag. It is used in string() to generate the HTML. If you have any specific/required attributes, it useful to override this and update them in the attributes Dict, and then call super's method.  
    
    '''

    tag = "HtmlComponent"
    indented_content = True
    _paired = True

    def __init__(self, parent=None, content: any = None, attributes: Dict[str, str]=None, tag: str = None, paired: bool = None, indented_content: bool = None):
        """
        The SuperClass for all HTML Element Classes

        Args:
            parent (HtmlComponent, optional): The parent element (subclass of HtmlComponent). Defaults to None.
            content (any, optional):  Any initial text that goes between pairs. This always gets outputted first. Designed for quick use. For text that goes after children, use the Raw subclass as a child
            attributes (Dict[str, str], optional): The Dict of attributes for the HTML Element. Defaults to {}.
            tag (str, optional): The tag of the HTML Element. If not provided, it will default to whatever the Class default is.
            paired (bool, optional): True/False whether the HTML element is a paired element. If not provided, it will default to whatever the Class default is (True by standard)
            indented_content (bool, optional): True/False whether the content within tags is indented. If not provided, it will default to the Class defualt is (True by standard)
        """

        # public
        # element hierarchy
        self.parent = parent
        self.children = []

        # html properties
        self._content = content
        if attributes is None:
            attributes = {}
        self.attributes = attributes
        # tag override
        if tag is not None:
            self.tag = tag
        # pair override
        if paired is not None:
            self._paired = paired
        # indented_content override
        if indented_content is not None:
            self.indented_content = indented_content
    
    def add(self, element):
        """
        Makes the given element a child of the HtmlComponent object. 

        Args:
            element HtmlComponent: The Element

        Returns:
            HtmlComponent: Returns the element (seems pointless, but useful for using the HtmlComponent constructor in the argument)
        """
        if not isinstance(element, HtmlComponent):
            return None
        
        element.parent = self

        self.children.append(element)

        return element

    def remove(self):
        """Removes element and any sub elements from the hierarchy"""
        if self.parent is not None and isinstance(self.parent, HtmlComponent):
            self.parent.children.remove(self)
        
        for child in self.children:
            if isinstance(child, HtmlComponent):
                child.remove()
    
    def get_content(self):
        """
        Yields the content of the HtmlComponent
        When designing subclasses, note that this method is used in the generation of HTML.  

        Yields:
            str: Content
        """
        if self._content is not None:
            if type(self._content)==str:
                yield self._content

    
    def _get_attribute_string(self) -> str:
        """Returns the string used in HtmlComponent.string()"""
        attribute_string = "".join([f" {key}=\"{value}\"" for key, value in self.attributes.items()])
        return attribute_string
    
    def string(self, indentation_level=0) -> str:
        """
        Coverts the HtmlComponent object and it's children to HTML

        Args:
            indentation_level (int, optional): Only used in recursion. Defaults to 0.

        Returns:
            str: The HTML
        """
        tabs = "    "*(indentation_level)

        attribute_str = self._get_attribute_string()

        html_string = tabs + f"<{self.tag}{attribute_str}>"

        if self._paired:
            for content in self.get_content():
                # check if indentation is required
                if self.indented_content == True:
                    html_string += "\n"+tabs+"    "
                html_string += content
            for element in self.children:
                # no matter if indented content is true or false, children content is placed on new line
                html_string += "\n"+element.string(indentation_level=indentation_level+1)

            # if indentation, create new line after for closing tag
            if self.indented_content == True:
                html_string += "\n"+tabs

            html_string += f"</{self.tag}>"
        else:
            html_string += "\n"
        
        return html_string
    

class Comment(HtmlComponent):
    """
    An HTML Comment HtmlComponent
    Cannot have children HtmlComponents.
    The children list does nothing, as does the add method.

    Instance Variables:
        text (str): The content of the comment

    Overrides the string method
    """
    _paired = False
    def __init__(self, text: str, parent: HtmlComponent=None):
        """
        Creates a new HTML comment. 
        Despite being an HtmlComponent, it cannot have children HtmlComponents (as it is a comment).
        As such, the children list is set to None, and calling Comment.add() will do nothing and return None

        Args:
            text (str): The content of the comment.
            parent (HtmlComponent, optional): The parent HtmlComponent. Defaults to None.
        """
        self.text = text

        if parent is not None:
            self.parent = parent
        
        self.children = None 

    def add(self) -> None:
        '''Cannot add children to a Comment element. If called, this returns None'''
        return None
    
    def string(self, indentation_level=0):
        tabs = "    "*(indentation_level)
        html_string = tabs+f"<!--{self.text}-->"
        return html_string
    
class Raw(HtmlComponent):
    """
    Not related to the assignment.

    My quick and hacky implementation of adding raw text between HTML tags.
    Naturally, this class wasn't designed to have children, so do not give it any or else weird behavour may occur.
    The current limitation of HtmlComponent is that the content output always goes before the children. What if you want text after? 
    That is what this is for.
    If I want to work on this for fun outside of this assignment, I would include this in the main implementation. Otherwise, this works for now.

    """
    def __init__(self, text: str, parent: HtmlComponent=None):
        """
        Creates Raw Text that can be put between children HtmlComponents 

        Args:
            text (str): The text content
            parent (HtmlComponent, optional): Parent HtmlComponent. Defaults to None.
        """
        self.text = text

        if parent is not None:
            self.parent = parent
        
        self.children = None 

    def add(self) -> None:
        '''Cannot add children to a Comment element. If called, this returns None'''
        return None
    
    def string(self, indentation_level=0):
        html_string = ""
        tabs = "    "*(indentation_level)
        first_line = True

        for line in self.text.splitlines():
            if first_line == False:
                html_string += "\n"
            html_string += tabs+line
            first_line = False

        return html_string


class CircleShape(HtmlComponent):
    """
    An SVG Circle HtmlComponent

    Note: key attributes relating to the circles properties contained within the instance's attributes Dict are 
    overwritten by the corresponding instance variables by _get_attribute_string in order to update them before output

    """
    tag="circle"
    indented_content = False

    def __init__(self, position: Position, radius: int, fill: rgb = rgb(255,0,0), fill_opacity: float = 1.0, attributes: Dict[str, str] = {}, **kwargs):
        """
        An SVG Circle HtmlComponent

        Args:
            position (Position): the circle's position
            radius (int): the circle's radius
            fill (rgb, optional): the circle's colour. Defaults to bright red.
            fill_opacity (float, optional): the fill opacity. Defaults to 1.0.
            attributes (Dict[str, str], optional): any HTML attributes. Defaults to {}.
        
        Extra keywords are passed to HtmlComponent
        """
        self.position = position
        self.radius = radius
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.attributes = attributes

        super().__init__(**kwargs)

    def _get_attribute_string(self) -> str:
        # update attributes with necessry class specific attributes
        self.attributes["cx"] = self.position.x
        self.attributes["cy"] = self.position.y
        self.attributes["r"] = self.radius
        self.attributes["fill"] = str(self.fill)
        self.attributes["fill-opacity"] = self.fill_opacity

        return super()._get_attribute_string()

# Make a Rectangle Class
class RectangleShape(HtmlComponent):
    """
    An SVG Rectangle HtmlComponent

    Note: key attributes relating to the rectangle's properties contained within the instance's attributes Dict are 
    overwritten by the corresponding instance variables by _get_attribute_string in order to update them before output

    """
    tag="rect"
    indented_content = False

    def __init__(self, position: Position, width: int, height: int, fill: rgb = rgb(255,0,0), fill_opacity: float = 1.0, attributes: Dict[str, str] = {}, **kwargs):
        """
        An SVG Rectangle HtmlComponent

        Args:
            position (Position): the rectangle's position
            width (int): the rectangle's width
            height (int): the rectangle's height
            fill (rgb, optional): the rectangle's colour. Defaults to bright red.
            fill_opacity (float, optional): the fill opacity. Defaults to 1.0.
            attributes (Dict[str, str], optional): any HTML attributes. Defaults to {}.
        
        Extra keywords are passed to HtmlComponent
        """
        self.position = position
        self.width = width
        self.height = height
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.attributes = attributes

        super().__init__(**kwargs)

    def _get_attribute_string(self) -> str:
        # update attributes with necessry class specific attributes
        self.attributes["x"] = self.position.x
        self.attributes["y"] = self.position.y
        self.attributes["width"] = self.width
        self.attributes["height"] = self.height
        self.attributes["fill"] = str(self.fill)
        self.attributes["fill-opacity"] = self.fill_opacity

        return super()._get_attribute_string()

# Make an Ellipse Class
class EllipseShape(HtmlComponent):
    """
    An SVG Ellipse HtmlComponent

    Note: key attributes relating to the ellipse's properties contained within the instance's attributes Dict are 
    overwritten by the corresponding instance variables by _get_attribute_string in order to update them before output

    """
    tag="ellipse"
    indented_content = False

    def __init__(self, position: Position, rx: int, ry: int, fill: rgb = rgb(255,0,0), fill_opacity: float = 1.0, attributes: Dict[str, str] = {}, **kwargs):
        """
        An SVG Ellipse HtmlComponent 

        Args:
            position (Position): the ellipse's position
            rx (int): the ellipse's x radius
            ry (int): the ellipses's y radius
            fill (rgb, optional): the ellipse's colour. Defaults to bright red.
            fill_opacity (float, optional): the fill opacity. Defaults to 1.0.
            attributes (Dict[str, str], optional): any HTML attributes. Defaults to {}.
        
        Extra keywords are passed to HtmlComponent
        """
        self.position = position
        self.rx = rx
        self.ry = ry
        self.fill = fill
        self.fill_opacity = fill_opacity
        self.attributes = attributes

        super().__init__(**kwargs)

    def _get_attribute_string(self) -> str:
        # update attributes with necessry class specific attributes
        self.attributes["cx"] = self.position.x
        self.attributes["cy"] = self.position.y
        self.attributes["rx"] = self.rx
        self.attributes["ry"] = self.ry
        self.attributes["fill"] = str(self.fill)
        self.attributes["fill-opacity"] = self.fill_opacity

        return super()._get_attribute_string()


# Make a SvgCanvas class with tags as svg
class SvgCanvas(HtmlComponent):
    """
    An SVG Html Element

    Instance Variable:
        size (Size): the size of the canvas
        attributes (Dict[str, str]): HTML Attributes
    
    Methods
        gen_art(self) -> None: Generates the circles required by Assignment Part 1
    
    """
    tag="svg"
    def __init__(self, size: Size, attributes: Dict[str, str] = {}, **kwargs):
        """
        An SVG Html Element

        Args:
            size (Size): The sizing information for the SvgCanvas
            attributes (Dict[str, str], optional): Any HTML Attributes

        
        Extra keywords are passed to HtmlComponent
        """
        self.size = size
        self.attributes = attributes
        super().__init__(**kwargs)

    
    def _get_attribute_string(self) -> str:
        self.attributes["width"] = self.size.width
        self.attributes["height"] = self.size.height
        return super()._get_attribute_string()

    def gen_art(self) -> None:
        '''Generates circles required by Part 1'''
        for i in range(5):
            circle_x = 50 + 100 * i
            circle_y_red = 50
            circle_y_blue = 250
            circle_red = CircleShape(Position(circle_x, circle_y_red), 50, fill=rgb(255, 0, 0), fill_opacity=1)
            circle_blue = CircleShape(Position(circle_x, circle_y_blue), 50, fill=rgb(0, 0, 255), fill_opacity=1)
            self.add(circle_red)
            self.add(circle_blue)

class SvgText(HtmlComponent):
    """
    SVG Text HtmlComponent

    Note: key attributes in attributes Dict are overwritten by corresponding instance variables upon output
    """
    tag = "text"

    def __init__(self, position: Position, content: str = None, indented_content: bool = False, parent: HtmlComponent = None, **kwargs):
        """
        SVG Text HtmlComponent

        Args:
            position (Position): The position of the text
            content (str, optional): The initial text content. Defaults to None.
            indented_content (bool, optional): Whether or not the content is indented. Defaults to False.
            parent (HtmlComponent, optional): The parent element. Defaults to None.
        """
        self.x = position.x
        self.y = position.y 
        self.indented_content = indented_content
        self.parent = parent

        super().__init__(content=content, **kwargs)

    def _get_attribute_string(self) -> str:
        self.attributes["x"] = self.x
        self.attributes["y"] = self.y
        return super()._get_attribute_string()

    
if __name__ == "__main__":
    # my test code
    doc = HtmlDocument()

    svg = doc.body.add(SvgCanvas(Size(500, 300)))
    circle = CircleShape(
        Position(25,25),
        50,
        rgb(150,0,255)
    )
    svg.add(circle)

    svg.add(Comment("Test"))

    doc.body.add(Raw("<b>test</b>"))
    doc.body.add(Raw("Another raw element?\nYep!"))
    
    changed_text = doc.body.add(Raw("ABC"))
    changed_text.text = "DEF"
    rect = RectangleShape(
        Position(100,100),
        100,
        50,
        rgb(255, 0, 0)
    )
    el = EllipseShape(
        Position(300,100),
        100,
        50,
        rgb(255, 255, 0)
    )
    svg.add(rect)
    svg.add(el)

    txt = SvgText(Position(10,20), content="hello")
    svg.add(txt)

    doc.output()
