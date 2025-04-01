
from fractions import Fraction

import sympy

from pyrope import config
from pyrope.dtypes import (
    BoolType, ComplexType, DictType, EquationType, ExpressionType, IntType, GraphicalInteractionType, 
    LinearExpressionType, ListType, MatrixType, OneOfType, PolynomialType,
    RationalType, RealType, SetType, StringType, TupleType, VectorType
)
from pyrope.errors import ValidationError
from pyrope.nodes.node import Node
from pyrope.nodes.widgets import Checkbox, Dropdown, GraphicalHotspot, GraphicalSelectPoint, GraphicalOrder, GraphicalAssociate, GraphicalGapMatch, GraphicalPositionObject, RadioButtons, Slider, Text


class Problem(Node):

    dtype = DictType()

    def __init__(self, template, **ifields):
        Node.__init__(self, template, ifields)

    def assemble(self, **ifields):
        return ifields

    def disassemble(self, ifields):
        return ifields

    @property
    def answers(self):
        ifields = {}
        for name in self.ifields:
            try:
                ifields[name] = self.ifields[name].value
            except ValidationError:
                ifields[name] = None
        return ifields

    def compare(self, LHS, RHS):
        return sum(
            ifield.compare(LHS[name], RHS[name])
            for name, ifield in self.ifields.items()
        ) / len(self.ifields)


class Bool(Node):

    def __init__(self, *, widget=Checkbox(), **kwargs):
        self.dtype = BoolType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Complex(Node):

    def __init__(
        self, *, elementwise=True, i_on_the='right', widget=Text(), **kwargs
    ):
        self.dtype = ComplexType(**kwargs)
        if elementwise is True:
            _ = ElementwiseComplex(
                i_on_the=i_on_the, widget=widget, **kwargs
            )
        else:
            _ = widget
        Node.__init__(self, '<<_>>', {'_': _}, **kwargs)


class ElementwiseComplex(Node):

    def __init__(self, *, i_on_the='right', widget=Text(), **kwargs):
        self.dtype = ComplexType(**kwargs)
        if i_on_the == 'right':
            template = '<<a>> + <<b>> i'
        elif i_on_the == 'left':
            template = '<<a>> + i <<b>>'
        else:
            raise ValueError("Parameter 'i_on_the' must be 'left' or 'right'.")
        Node.__init__(
            self, template, {
                'a': Real(widget=widget, **kwargs),
                'b': Real(widget=widget, **kwargs)
            }, **kwargs
        )

    def assemble(self, **ifields):
        return ifields['a'] + ifields['b'] * 1j

    def disassemble(self, z):
        return {'a': z.real, 'b': z.imag}


class Dict(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = DictType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Expression(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = ExpressionType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Equation(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = EquationType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Int(Node):

    def __init__(self, *, widget=None, **kwargs):
        self.dtype = IntType(**kwargs)
        if widget is None:
            if (
                self.dtype.minimum is not None and
                self.dtype.maximum is not None
            ):
                widget = Slider(self.dtype.minimum, self.dtype.maximum)
            else:
                widget = Text()
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


Integer = Int


class Matrix(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = MatrixType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Vector(Matrix):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = VectorType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class MultipleChoice(Node):

    def __init__(self, questions, choices, *, widget=None, **kwargs):
        self.dtype = DictType(**kwargs)
        if not isinstance(questions, set) or len(questions) == 0:
            raise ValueError("'questions' has to be a non-empty set.")
        if not isinstance(choices, set) or len(choices) <= 1:
            raise ValueError(
                "'choices' has to be a set with at least two elements."
            )
        if widget is None:
            if len(choices) <= config.maximal_radio_buttons:
                widget = RadioButtons(*choices, vertical=False)
            else:
                widget = Dropdown(*choices)
        ifields = {
            f'question_{i}': OneOf(*choices, widget=widget)
            for i in range(len(questions))
        }
        self.mapping = {
            question: ifield_name
            for question, ifield_name in zip(questions, ifields.keys())
        }
        # "\n\n" creates a new paragraph in Markdown.
        # "  \n" renders a line break in Markdown.
        template = '\n\n'.join([
            f'{question}  \n<<{ifield_name}>>'
            for question, ifield_name in self.mapping.items()
        ])
        self.mapping |= {
            ifield_name: question
            for question, ifield_name in self.mapping.items()
        }
        Node.__init__(self, template, ifields, **kwargs)

    def assemble(self, **ifields):
        return {
            self.mapping[name]: value
            for name, value in ifields.items()
        }

    def disassemble(self, questions):
        return {
            self.mapping[question]: value
            for question, value in questions.items()
        }


class Natural(Int):

    def __init__(self, *, with_zero=True, **kwargs):
        if not isinstance(with_zero, bool):
            raise ValueError("'with_zero' must be boolean.")
        minimum = 0
        if not with_zero:
            minimum = 1
        Int.__init__(self, minimum=minimum, **kwargs)


class OneOf(Node):

    def __init__(self, *args, widget=None, **kwargs):
        self.dtype = OneOfType(options=args)
        if widget is None:
            if len(args) <= config.maximal_radio_buttons:
                widget = RadioButtons(*args)
            else:
                widget = Dropdown(*args)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Polynomial(Node):

    def __init__(
        self, *, degree=None, elementwise=False, widget=Text(), **kwargs
    ):
        self.dtype = PolynomialType(degree=degree, **kwargs)
        if elementwise is True:
            _ = ElementwisePolynomial(degree, widget=widget, **kwargs)
            Node.__init__(self, '<<_>>', {'_': _}, **kwargs)
        else:
            Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class ElementwisePolynomial(Node):

    def __init__(self, degree, *, widget=Text(), **kwargs):
        self.dtype = PolynomialType(degree=degree, elementwise=True, **kwargs)
        self.degree = degree
        if self.degree is None:
            raise ValueError(
                'Cannot render polynomials with an arbitrary degree '
                'elementwise.'
            )
        if len(self.dtype.symbols) >= 2:
            raise NotImplementedError(
                'Cannot render polynomials with more than one symbol '
                'elementwise.'
            )
        self.symbol = next(iter(self.dtype.symbols))
        tokens = [
            f'<<x_{i}>>${self.symbol}^{"{"}{i}{"}"}$'
            for i in range(self.degree, 1, -1)
        ]
        if self.degree >= 1:
            tokens.append(f'<<x_1>>${self.symbol}$')
        tokens.append('<<x_0>>')
        template = ' + '.join(tokens)
        Node.__init__(
            self, template, {
                f'x_{i}': Rational(elementwise=False, widget=widget, **kwargs)
                for i in range(0, self.degree + 1)
            }
        )

    def assemble(self, **ifields):
        return sympy.Poly.from_dict({
            i: ifields[f'x_{i}'] for i in range(0, self.degree + 1)
        }, self.symbol)

    def disassemble(self, value):
        coeffs = value.all_coeffs()[::-1]
        return {
            f'x_{i}': coeffs[i] for i in range(0, self.degree + 1)
        }


class LinearExpression(Node):

    def __init__(self, *, elementwise=False, widget=Text(), **kwargs):
        self.dtype = LinearExpressionType(elementwise=elementwise, **kwargs)
        if elementwise is True:
            _ = ElementwiseLinearExpression(widget=widget, **kwargs)
            Node.__init__(self, '<<_>>', {'_': _}, **kwargs)
        else:
            Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class ElementwiseLinearExpression(ElementwisePolynomial):

    def __init__(self, **kwargs):
        ElementwisePolynomial.__init__(self, 1, **kwargs)
        self.dtype = LinearExpressionType(elementwise=True, **kwargs)

    def disassemble(self, value):
        coeffs = value.all_coeffs()[::-1]
        if value.degree() == 0:
            coeffs.append(0)
        return {
            f'x_{i}': coeffs[i] for i in range(0, self.degree + 1)
        }


class Rational(Node):

    def __init__(self, *, elementwise=True, widget=Text(), **kwargs):
        self.elementwise = elementwise
        self.dtype = RationalType(**kwargs)
        if self.elementwise is True:
            _ = ElementwiseRational(widget=widget, **kwargs)
        else:
            _ = widget
        Node.__init__(self, '<<_>>', {'_': _}, **kwargs)


class ElementwiseRational(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = RationalType(**kwargs)
        Node.__init__(
            self, '<<a>> / <<b>>', {
                'a': Int(widget=widget, **kwargs),
                'b': Natural(widget=widget, with_zero=False, **kwargs)
            }, **kwargs
        )

    def assemble(self, **ifields):
        return Fraction(ifields['a'], ifields['b'])

    def disassemble(self, q):
        return {'a': q.numerator, 'b': q.denominator}


class Real(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = RealType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Set(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = SetType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class String(Node):

    def __init__(self, *, widget=Text(), **kwargs):
        self.dtype = StringType(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class Tuple(Node):

    dtype = TupleType

    def __init__(self, widget=Text(), **kwargs):
        self.dtype = self.dtype(**kwargs)
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)


class List(Tuple):

    dtype = ListType

class GraphicInteraction(Node):
    """
    A class that creates interactive graphical widgets in JavaScript.
    It initializes different types of graphical interaction widgets based on the provided type.
    """
    
    dtype = GraphicalInteractionType

    def __init__(self, *, type, background_src, icon_src, all_coords = [], widget=None, **kwargs):
        """
        Initializes a graphical interaction widget.
        
        Parameters:
        - type (str): The type of graphical interaction. Must be one of:
            'hotspot', 'select_point', 'order', 'associate', 'gap_match', or 'position_object'.
        - background_src (dictionary): The background source (path to an image (local through jupyter or url), along with width and height properties) that will be used for the widget.
        - icon_src (dictionary): The icon source (path to an image (local through jupyter or url), along with width and height properties) that will be used for icon elements (that are either provided on init or created during the usage) for the widget. Not all icons need to be interacted with necessarily for calculating the solution. 
        - all_coords (list, optional): A list of (x,y) coordinates to place initial icons, used for the following interaction types:
            'hotspot', 'order', 'associate' and 'gap_match'.
        - widget (optional): A pre-initialized widget (if provided, it is used instead of creating a new one).

        Raises:
        - ValueError: If an invalid `type` is provided.
        
        Validation:
        - The solution to the widgets has to be provided in one of the following ways:
            'hotspot', 'gap_match': the coordinates of initialized icons not in order
                (e.g. ["20,30","40,60","70,40"] - three icons that have to be activated: (40,60), (20,30), (70,40) and (70,40), (40,60), (20,30) would be correct for instance) 
            'order': the coordinates of initialized icons in order
                (e.g. ["20,30","40,60","70,40"] - three icons that have to be activated in the order: (20,30), (40,60), (70,40)) 
            'associate': the coordinates of initialized icon pairs not in order
                (e.g. ["20,30,40,60"] - a single icon pair (20,30) and (40,60) that has to be connected by the user - order is not relevant, adding reversed pairs of pairs that were already added results in unsolvable exercises) 
            'select_point', 'position_object': coordinate pairs, that represent the upper-left and lower-right corners of an area in which one icon has to be placed, the center of the icon is used for validation
                (e.g. ["100,100,200,200"] - a single area with upper left (100,100) and lower right (200,200) coordinates) 
        
        """
        
        if widget is None:
            match type:
                case 'hotspot':
                    self.dtype = self.dtype(mode='set', **kwargs)
                    widget = GraphicalHotspot(background_src, icon_src, all_coords)
                case 'select_point':
                    self.dtype = self.dtype(mode='area', **kwargs)
                    widget = GraphicalSelectPoint(background_src, icon_src)
                case 'order':
                    self.dtype = self.dtype(mode='list', **kwargs)
                    widget = GraphicalOrder(background_src, icon_src, all_coords)
                case 'associate':
                    self.dtype = self.dtype(mode='reversible_set', **kwargs)
                    widget = GraphicalAssociate(background_src, icon_src, all_coords)
                case 'gap_match':
                    self.dtype = self.dtype(mode='set', **kwargs)
                    widget = GraphicalGapMatch(background_src, icon_src, all_coords)
                case 'position_object':
                    self.dtype = self.dtype(mode='area', **kwargs)
                    widget = GraphicalPositionObject(background_src, icon_src)
                case _ :
                    raise ValueError("'type' has to be one of 'hotspot', 'select_point', 'order', 'associate', 'gap_match' or 'position_object'")
        Node.__init__(self, '<<_>>', {'_': widget}, **kwargs)