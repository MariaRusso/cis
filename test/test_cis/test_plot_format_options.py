'''
Module to test the plot formatting options
'''
from jasmin_cis.plot import plot
from jasmin_cis.parse import parse_args
from nose.tools import istest, raises
import iris
from data import *

def make_cube(filename, variable = None):
    if variable is None:
        variable = iris.AttributeConstraint(name = valid_variable_in_valid_filename)
    cube = iris.load_cube(filename, variable) 
    cube = list(cube.slices([ coord for coord in cube.coords() if coord.points.size > 1]))[0]
    return cube 

@istest
def can_set_line_colour_to_valid_colour():   
    cube = make_cube(valid_1d_filename)
    plot([cube], out_filename = out_filename, **{"color" : "green"})
    
@istest
@raises(ValueError)
def should_raise_value_error_with_invalid_colour():   
    cube = make_cube(valid_1d_filename)
    plot([cube], out_filename = out_filename, **{"color" : "greenn"})
    
@istest
def should_not_raise_error_if_colour_is_specified_for_invalid_chart_type(): # Simply discard the colour specified 
    cube = make_cube(valid_2d_filename)
    plot([cube], out_filename = out_filename, **{"color" : "greenn"})  
    
@istest
def can_set_line_width_to_valid_width():   
    cube = make_cube(valid_1d_filename)
    plot([cube], out_filename = out_filename, **{"linewidth" : 40})   
    
@istest
def can_set_line_style_to_valid_style():   
    cube = make_cube(valid_1d_filename)
    plot([cube], out_filename = out_filename, **{"linestyle" : "dashed"})   
    
@istest
def can_set_colour_map_to_valid_colour():   
    cube = make_cube(valid_2d_filename)
    plot([cube], out_filename = out_filename, **{"cmap" : "RdBu"})
    