import pytest
import pygame
import monsterpr as mpr

def test_character_start_happy_path():
    """
    happy path test to make sure character starts in the center.
    """
    player = mpr.Character()
    
    assert player.x == player.starting_pos[0]
    assert player.y == player.starting_pos[1]
    
def test_move_up_happy_path():
    """
    happypath test to make sure move_up works correctly
    """
    player = mpr.Character()
    player.move_up()
    assert player.direction == "up"
def test_move_left_happy_path():
    """
    happypath test to make sure move_left works correctly
    """
    player = mpr.Character()
    player.move_left()
    assert player.direction == "left"
def test_move_down_happy_path():
    """
    happypath test to make sure move_down works correctly
    """
    player = mpr.Character()
    player.move_down()
    assert player.direction == "down"

def test_move_right_happy_path():
    """
    happypath test to make sure move_right works correctly
    """
    player = mpr.Character()
    player.move_right()
    assert player.direction == "right"


def test_multiple_movements_edge_case():
    """
    edge case test to make sure multiple movements work correctly
    """
    player = mpr.Character()
    startpos = player.y
    
    player.move_up()
    player.move_up()
    
    assert player.y == startpos - 2 * player.speed
    
def test_character_image_load_happy_path():
    """
    happy path test to make sure character image loads correctly
    """
    player = mpr.Character()
    assert player.base_image is not None
    assert player.image is not None
    
def test_background_image_load_happy_path():
    """
    happy path test to make sure background image loads correctly
    """
    background = mpr.Background(screen=None)
    assert background.images is not None

def test_quote_happy_path():
    """
    happy path test to make sure quote display works correctly
    """
    quote_display = mpr.QuoteDisplay(screen=None)
    quote_display.update_quote() 
    assert quote_display.current_quote != ""
    
def test_author_happy_path():
    """
    happy path test to make sure author display works correctly
    """
    quote_display = mpr.QuoteDisplay(screen=None)
    quote_display.update_quote() 
    assert quote_display.current_author != ""