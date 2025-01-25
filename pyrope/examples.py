
from fractions import Fraction
from math import prod

import sympy

from pyrope.nodes.dtype_nodes import (
    Equation, Expression, GraphicInteraction, Bool, Int, List, Problem, Rational, Set, String
)

from pyrope.core import Exercise


class EquationExample(Exercise):

    def problem(self):
        return Problem(
            """
            The Pythagorean Theorem reads <<equation>>.
            """,
            equation=Equation(symbols='a,b,c')
        )

    def the_solution(self):
        return sympy.parse_expr('Eq(a**2+b**2,c**2)')


class ExpressionExample(Exercise):

    def problem(self):
        return Problem(
            """
            Einstein's most famous formula, relating Energy $E$ and mass $m$
            via the speed of light $c$, reads $E=$<<RHS>>.
            """,
            RHS=Expression(symbols='m,c')
        )

    def the_solution(self):
        return sympy.parse_expr('m*c**2')


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

#TODO jupyter view collapses on running cell
class HotspotExampleUK(Exercise):
    '''
    Example of a Hotspot Interaction
    '''

    def problem(self):
        #TODO path should be done dependant on notebook/lab
        #TODO make sure to use creative common licensed pngs as example
        
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
        
        #TODO use id as well -> dict instead of list? 
        icon_coords = ["120,305", "200,130", "200,200", "300,350", "310,380", "355,410", "285,460", "230,440", "270,290"]
        
        graphic_ = GraphicInteraction(type='hotspot', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Select all marked UK airports that have an average of 100+ outgoing flights per day.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
        
    #TODO validate all coords in solution are part of input are in solution
    def the_solution(self):
        return ["200,130", "200,200", "300,350"]
    
    #TODO scores

class HotspotExamplePlants(Exercise):
    '''
    Example of a Hotspot Interaction
    '''

    def problem(self):
        #TODO path should be done dependant on notebook/lab
        background = {
            "src":'../tree/media/plantcell_map.png',
            "width":700, 
            "height":700
        }
        
        icon = {
            "src":'../tree/media/exclmark_icon.png', 
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

class HotspotExample3(Exercise):
    '''
    Example of a Hotspot Interaction
    '''

    def problem(self):
        #TODO path should be done dependant on notebook/lab
        background = {
            "src":'../tree/media/white_square.png',
            "width":400, 
            "height":400
        }
        
        icon = {
            "src":'../tree/media/exclmark_icon.png', 
            "width":25, 
            "height":25
        }
        
        icon_coords=["10,20", "60,60", "100,100", "200,300", "300,200"]
        
        graphic_ = GraphicInteraction(type='hotspot', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Mark all POI on the image.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60", "100,100"]
    
#TODO more fleshed out examples
class SelectPointExample(Exercise):
    '''
    Example of a Select Point Interaction
    '''

    #TODO also use 'debug' mode to verify areas -> outline
    def problem(self):
        background = {
            "src":'../tree/media/white_square.png',
            "width":400, 
            "height":400
        }
        
        icon = {
            "src":'../tree/media/pin_icon.png', 
            "width":12, 
            "height":12
        }
        
        graphic_ = GraphicInteraction(type='select_point', background_src=background, icon_src=icon)
        return Problem(
            '''
            Select all regions.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60", "100,100"]
    
#TODO replace png icons with svgs
class GraphicOrderExample(Exercise):
    '''
    Example of a Order Interaction
    '''

    def problem(self):
        background = {
            "src":'../tree/media/white_square.png',
            "width":400, 
            "height":400
        }
        
        icon = {
            "src":'../tree/media/circle_icon.svg',
            "width":15, 
            "height":15
        }
        
        icon_coords=["10,20", "60,60", "100,100", "200,300", "300,200"]
        
        graphic_ = GraphicInteraction(type='order', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Mark the correct order of all POIs.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60", "100,100"]
    
class GraphicOrderExample2(Exercise):
    '''
    Example of a Order Interaction using bigger icons
    '''

    #TODO also use 'debug' mode to verify areas -> outline
    def problem(self):
        background = {
            "src":'../tree/media/white_square.png',
            "width":400, 
            "height":400
        }
        
        icon = {
            "src":'../tree/media/circle_icon.svg',
            "width":70, 
            "height":70
        }
        
        icon_coords=["10,20", "60,60", "100,100", "200,300", "300,200"]
        
        graphic_ = GraphicInteraction(type='order', background_src=background, icon_src=icon, all_coords=icon_coords)
        return Problem(
            '''
            Mark the correct order of all POIs.
            
            <<graphic>>
            ''',
            graphic=graphic_
        )
    
    def the_solution(self):
        return ["60,60", "100,100"]