
from fractions import Fraction
from math import prod

import sympy

from pyrope.nodes.dtype_nodes import (
    Equation, Expression, GraphicInteraction, Bool, Int, List, Problem, Rational, Set, String
)

from pyrope.core import Exercise

"""
class EquationExample(Exercise):

    def problem(self):
        return Problem(
            '''
            The Pythagorean Theorem reads <<equation>>.
            ''',
            equation=Equation(symbols='a,b,c')
        )

    def the_solution(self):
        return sympy.parse_expr('Eq(a**2+b**2,c**2)')


class ExpressionExample(Exercise):

    def problem(self):
        return Problem(
            '''
            Einstein's most famous formula, relating Energy $E$ and mass $m$
            via the speed of light $c$, reads $E=$<<RHS>>.
            ''',
            RHS=Expression(symbols='m,c')
        )

    def the_solution(self):
        return sympy.parse_expr('m*c**2')
"""

class IntExample(Exercise):

    def problem(self):
        return Problem(
            '''
            If there are five apples and you take away three,
            how many do you have?

            <<number>>
            ''',
            number=Int(minimum=0, maximum=5)
        )

    def the_solution(self):
        return 3

    def feedback(self, number):
        return 'You took three apples, so you have three!'


class SetExample(Exercise):
    '''
    Use a set if the order of the items you ask for does not matter.
    '''

    def preamble(self):
        return r'You know that $2+2=2\times2$.'

    def problem(self):
        return Problem(
            '''
            Find a set of three different integers whose sum is equal to their
            product.

            <<numbers>>
            ''',
            numbers=Set(count=3)
        )

    def a_solution(self):
        return {1, 2, 3}

    def scores(self, numbers):
        return sum(numbers) == prod(numbers)

"""
class RationalExample(Exercise):

    def problem(self):
        return Problem(
            '''
            A half is a third of it. What is it?

            <<number>>
            ''',
            number=Rational()
        )

    def the_solution(self):
        return Fraction(3, 2)


class StaticExample(Exercise):
    '''
    For simplicity, let us start with a static exercise, i.e. one which is the
    same every time we run it.

    Note that the user's answer is automatically scored, if we provide the
    sample solution, since PyRope scores one point per correct input field by
    default.
    '''

    preamble = __doc__

    def problem(self):
        return Problem(
            '''
            What is the answer to the Ultimate Question of Life, The Universe,
            and Everything?

            <<answer>>
            ''',
            answer=String(strip=True)
        )

    def the_solution(self):
        return 'fourty-two'


class ParsingExample(Exercise):
    '''
    PyRope accepts valid Python expressions for standard data types. So you
    can, for example, use scientific notation, such as '1e21'.
    '''

    preamble = __doc__

    def problem(self):
        return Problem(
            '''A 'Sextillion' equals <<answer>>. ''', answer=Int()
        )

    def the_solution(self):
        return 1e21


class FeedbackExample(Exercise):
    '''
    It is possible to give feedback with PyRope. To use adaptive feedback,
    you can pass your parameters and user answers to the 'feedback' method.
    '''

    preamble = __doc__

    def problem(self):
        return Problem(
            '''
            One grandmother, two mothers, two daughters and one granddaughter
            go to the cinema and buy one ticket each. How many tickets do they
            have to buy in total?

            <<number>>
            ''',
            number=Int()
        )

    def the_solution(self):
        return 3

    def feedback(self, number):
        if number == 3:
            return "You knew the riddle, didn't you?"
        return (
            "The grandmother is also a mother and the mother is also "
            "a daughter."
        )

"""
class TrivialExample(Exercise):
    '''
    For the sake of completeness, let us finish with a trivial example, one
    without any input fields. Admittedly, this does not make much sense. But
    your students will love it, as it gives them points for free. Note that
    we have to provide scores, since they can not be deduced from input fields.
    '''

    preamble = __doc__

    def problem(self):
        return Problem('Free lunch!')

    def scores(self):
        return 100

class HotspotExampleUK(Exercise):
    '''
    Example of a Hotspot Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/uk_map.png',
            "width":400, 
            "height":600
        }
        
        icon = {
            "src":'../tree/media/plane_icon.svg', 
            "width":25, 
            "height":25
        }
        
        icon_coords = ["120,305", "200,130", "200,200", "300,350", "310,380", "355,410", "285,460", "230,440", "270,290"]
        
        graphic_ = GraphicInteraction(type='hotspot', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Select all marked UK airports that have an average of 100+ outgoing flights per day.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
        
    def the_solution(self):
        return ["200,130", "200,200", "300,350"]
    

class HotspotExamplePlants(Exercise):
    '''
    Example of a Hotspot Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/plantcell_map.png',
            "width":700, 
            "height":700
        }
        
        icon = {
            "src":'../tree/media/exclamation-circle.svg', 
            "width":25, 
            "height":25
        }
        
        icon_coords=["250,225", "365,210", "185,251", "335,425", "330,320", "230,360"]
        
        graphic_ = GraphicInteraction(type='hotspot', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Select all marked cell organelles that have a double membrane.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
        
    def the_solution(self):
        return ["230,360", "250,225", "335,425"]

class SelectPointExampleAfricaVolcanos(Exercise):
    '''
    Example of a Select Point Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/africa_blank_map.png',
            "width":585, 
            "height":600
        }
        
        icon = {
            "src":'../tree/media/geo-alt-fill.svg', 
            "width":20, 
            "height":20
        }
        
        graphic_ = GraphicInteraction(type='select_point', background_src=background, icon_src=icon)
        return Problem(
            '''
            Select all regions in africa, in which active volacons reside.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60,100,100", "250,190,350,290"]
    
class GraphicOrderExampleBinaryTree(Exercise):
    '''
    Example of a Order Interaction
    '''

    def problem(self):
        #img source https://mathcenter.oxford.emory.edu/site/cs171/binarySearchTrees/
        background = {
            "src":'../tree/media/binary_tree_map.png',
            "width":657, 
            "height":438
        }
        
        icon = {
            "src":'../tree/media/circle-fill_icon.svg',
            "width":35, 
            "height":35
        }
        
        icon_coords=["383,27", "60,292", "222,114", "113,202", "94,381", "327,202", "239,381", "598,202", "490,202", "60,292", "274,292", "526,292", "383,292", "455,292", "546,114"]
        
        graphic_ = GraphicInteraction(type='order', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Flatten the binary tree into a linked list, choose the order of nodes within the resulting list.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["94,381", "60,292", "113,202", "222,114", "239,381", "274,292", "327,202", "383,292", "383,27", "455,292", "490,202", "526,292", "546,114", "598,202"]

class GraphicAssociateExampleUK(Exercise):
    '''
    Example of a Associate Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/uk_map.png',
            "width":400, 
            "height":600
        }
        
        icon = {
            "src":'../tree/media/plane_icon.svg', 
            "width":25, 
            "height":25
        }
        
        icon_coords = ["120,305", "200,130", "200,200", "300,350", "310,380", "355,410", "285,460", "230,440", "270,290"]
        
        graphic_ = GraphicInteraction(type='associate', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Mark all existing direct flight connections between uk airports.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    #either direction works
    def the_solution(self):
        return ["120,305,200,130", "310,380,355,410"]
    

class GraphicGapMatchExampleUK(Exercise):
    '''
    Example of a Gap Match Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/uk_map.png',
            "width":400, 
            "height":600
        }
        
        icon = {
            "src":'../tree/media/plane_icon.svg', 
            "width":25, 
            "height":25
        }
        
        icon_coords = ["120,305", "200,130", "200,200", "300,350", "310,380", "355,410", "285,460", "230,440", "270,290"]
        
        graphic_ = GraphicInteraction(type='gap_match', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Select all UK airports that have an average of 100+ outgoing flights per day.
            Fill the gaps by dragging the icon over the correct ones.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["200,200", "300,350", "310,380"]

    
class GraphicPositionObjectExampleAfricaVolcanos(Exercise):
    '''
    Example of a Position Object Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/africa_blank_map.png',
            "width":400, 
            "height":400
        }
        
        icon = {
            "src":'../tree/media/exclamation-circle.svg',
            "width":22, 
            "height":22
        }
        
        graphic_ = GraphicInteraction(type='position_object', background_src=background, icon_src=icon)
        return Problem(
            '''
            Choose all regions that contain an active volacno in africa.
            Position the object on the right correctly over the image.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60,70,70"]