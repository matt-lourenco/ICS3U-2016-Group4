# Created by: Mr. Coxall
# Created on: Sep 2016
# Created for: ICS3U
# This scene shows the main menu.
# Edited by: Matthew Lourenco
# Dec 14 2016: created game scene. made scene read file to determine scale of sprites
# Dec 15 2016: game 1 functional

from __future__ import division
from scene import *
import ui
import time
from numpy import random
from game_one import *
from game_two import *
from game_three import *
from game_four import *
from game_five import *
from game_six import *
from game_seven import *

class GameScene(Scene):
    def setup(self):
        # this method is called, when user moves to this scene
        
        #These variable are created in order to avoid pointers
        self.size_of_screen_x = self.size.x
        self.size_of_screen_y = self.size.y
        self.center_of_screen_x = self.size_of_screen_x/2
        self.center_of_screen_y = self.size_of_screen_y/2
        
        # read file to determine self.scale of sprites
        shared_variables = open('./shared_variables.txt')
        screen_size = json.load(shared_variables)
        self.scale_of_sprites = screen_size[4]
        shared_variables.close()
        
        # properties
        self.game_over = False
        self.meteor_on_screen = False
        self.game2_count_to_five = False
        self.game2_count = 0
        self.game2_pause_counter = False
        self.game2_pause_count = 0
        
        # create a timer to keep track of how far the player has progressed
        self.start_time = time.time()
        
        # add background color
        background_position = Vector2(self.center_of_screen_x, self.center_of_screen_y)
        self.background = SpriteNode(position = background_position,
                                     color = '#e5e5e5',
                                     parent = self,
                                     size = self.size)
        # set up 7 games
        self.game1 = GameOne(self, self.size_of_screen_x * (1/6), self.size_of_screen_y * (5/6))
        self.game2 = GameTwo(self, self.size_of_screen_x * (5/6), self.size_of_screen_y * (5/6))
        self.game3 = GameThree(self, self.size_of_screen_x * (1/6), self.center_of_screen_y)
        self.game4 = GameFour(self, self.size_of_screen_x * (5/6), self.center_of_screen_y)
        self.game5 = GameFive(self, self.size_of_screen_x * (1/6), self.size_of_screen_y * (1/6))
        self.game6 = GameSix(self, self.size_of_screen_x * (5/6), self.size_of_screen_y * (1/6))
        self.game7 = GameSeven(self, self.center_of_screen_x, self.center_of_screen_y)
        
        self.game1.activate_game()
        
        
    
    def update(self):
        # this method is called, hopefully, 60 times a second
        
        # keep track of which games are active
        if time.time() - self.start_time > 3 and not self.game2.get_game_active() and not self.game_over:
            self.game2.activate_game()
        
        # game 1
        random_game_action_chance = random.randint(0, 1000)
        if self.game1.get_game_active() and not self.meteor_on_screen and random_game_action_chance < 5:
            self.game1.create_meteor(self)
            self.meteor_on_screen = True
        
        for meteor in self.game1.get_meteors():
            if meteor.frame.intersects(self.game1.get_power_core().frame) and not self.game_over:
                self.end_game()
        
        # game 2
        if self.game2.get_game_active() and self.game2.get_button_is_red() and not self.game2.get_game_paused() and not self.game_over and random_game_action_chance >= 5 and random_game_action_chance < 8:
            self.game2.make_button_green()
            self.game2_count_to_five = True
            self.game2_count = 0
        
        if self.game2_count_to_five:
            self.game2_count = self.game2_count + 1
            if self.game2_count == 150:
                self.game2.make_button_red()
                self.game2_count_to_five = False
                self.end_game()
        
        if self.game2_pause_counter:
            self.game2_pause_count = self.game2_pause_count + 1
            print(self.game2_pause_count)
            if self.game2_pause_count == 60:
                self.game2_pause_counter = False
                self.game2.set_game_paused(False)
        
        
    
    def touch_began(self, touch):
        # this method is called, when user touches the screen
        if self.game_over:
            if self.menu_button.frame.contains_point(touch.location):
                self.menu_button.scale = self.menu_button.scale * 0.9
                self.menu_text.scale = self.menu_text.scale * 0.9
        
        # game 2
        if self.game2.get_game_active() and not self.game_over and self.game2.get_button().frame.contains_point(touch.location):
            self.game2.get_button().scale = self.game2.get_button().scale * 0.9
            self.game2.get_button_shadow().scale = self.game2.get_button_shadow().scale * 0.9
    
    def touch_moved(self, touch):
        # this method is called, when user moves a finger around on the screen
        pass
    
    def touch_ended(self, touch):
        # this method is called, when user releases a finger from the screen
        
        # reset scale of buttons
        if self.game_over:
            self.menu_button.scale = self.menu_button_scale
            self.menu_text.scale = self.menu_text_scale
            # dismiss scene when menu button pressed
            if self.menu_button.frame.contains_point(touch.location):
                self.dismiss_modal_scene()
        
        # game 1
        for meteor in self.game1.get_meteors():
            if meteor.frame.contains_point(touch.location) and not self.game_over:
                meteor.remove_from_parent()
                self.game1.get_meteors().remove(meteor)
                self.meteor_on_screen = False
        
        # game 2
        self.game2.get_button().scale = self.scale_of_sprites
        self.game2.get_button_shadow().scale = self.scale_of_sprites
        
        if not self.game_over and self.game2.get_button().frame.contains_point(touch.location):
            if self.game2.get_button_is_red():
                self.end_game()
            elif not self.game2.get_button_is_red():
                self.game2.make_button_red()
                self.game2_count_to_five = False
                self.game2.set_game_paused(True)
                self.game2_pause_counter = True
                self.game2_pause_count = 0
        
    
    def did_change_size(self):
        # this method is called, when user changes the orientation of the screen
        # thus changing the size of each dimension
        pass
    
    def pause(self):
        # this method is called, when user touches the home button
        # save anything before app is put to background
        pass
    
    def resume(self):
        # this method is called, when user place app from background 
        # back into use. Reload anything you might need.
        pass
    
    def end_game(self):
        # this method ends the game
        self.game_over = True
        self.game1.game_over()
        self.game2.game_over()
        self.game3.game_over()
        self.game4.game_over()
        self.game5.game_over()
        self.game6.game_over()
        self.game7.game_over()
        
        # add 'game over' text
        game_over_position = Vector2(self.center_of_screen_x, self.size_of_screen_y * 0.7)
        self.game_over_text = LabelNode(text = 'Game Over',
                                        font = ('futura', 120),
                                        color = '#49db56',
                                        parent = self,
                                        position = game_over_position,
                                        z_position = 8,
                                        scale = self.scale_of_sprites)
        # add menu button
        menu_button_position = Vector2(self.center_of_screen_x, self.center_of_screen_y)
        menu_button_size = Vector2(self.size_of_screen_x * 0.4, self.size_of_screen_y * 0.15)
        menu_button_shape = ui.Path.rounded_rect(0, 0, menu_button_size.x, menu_button_size.y, 60)
        menu_button_shape.line_width = 10 * self.scale_of_sprites
        self.menu_button_scale = self.scale_of_sprites
        self.menu_button = ShapeNode(path = menu_button_shape,
                                     fill_color = '#5564ff',
                                     stroke_color = '#4652d1',
                                     parent = self,
                                     position = menu_button_position,
                                     z_position = 7,
                                     scale = self.menu_button_scale)
        # add menu text
        self.menu_text_scale = self.scale_of_sprites
        self.menu_text = LabelNode(text = 'MENU',
                                   color = '#e2e2e2',
                                   font = ('futura', 60),
                                   parent = self,
                                   position = menu_button_position,
                                   z_position = 8,
                                   scale = self.menu_text_scale)
        
    