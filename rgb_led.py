#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
	DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
	Version 2, December 2004

Copyright (C) 2013 Tillo Bosshart

Everyone is permitted to copy and distribute verbatim or modified
copies of this license document, and changing it is allowed as long
as the name is changed.

	DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
	TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

	0. You just DO WHAT THE FUCK YOU WANT TO.
"""

import Adafruit_BBIO.PWM as PWM
from colormath.color_objects import LabColor
from colormath.color_objects import RGBColor
from time import sleep


class rgb_led(object):

	colors = {
		'amber':[255,25,0],
		'black':[0,0,0],
		'blue':[0,0,255],
		'cyan':[0,255,128],
		'green':[0,255,0],
		'magenta':[255,0,180],
		'off':[0,0,0],
		'orange':[255,90,],
		'purple':[255,0.0,200],
		'red':[255,0,0],
		'warmwhite':[255,128,6],
		'white':[255,128,2],
		'yellow':[255,200,0],
	}
	color_rgb = colors['off']

	def __init__(self, red_pin, green_pin, blue_pin,verbose=False):
		super(rgb_led, self).__init__()
		self.r_pin = red_pin
		self.g_pin = green_pin
		self.b_pin = blue_pin
		PWM.start(self.r_pin, 0)
		PWM.start(self.g_pin, 0)
		PWM.start(self.b_pin, 0)
		self.fade_steps = 255
		self.verbose = verbose,

	def __del__(self):
		PWM.cleanup()

	def transition(self,value, maximum, start_point, end_point):
		return start_point + (end_point - start_point)*value/maximum

	def transition3(self,value, maximum, color1, color2):
		r1= self.transition(value, maximum, color1[0], color2[0])
		r2= self.transition(value, maximum, color1[1], color2[1])
		r3= self.transition(value, maximum, color1[2], color2[2])
		return [r1, r2, r3]

	"""Set Colors"""

	def set_color(self,color):
		try:
			self.set_color_rgb(self.colors[color])
		except:
			#print("Color {0} is not defined").format(color)
			pass
	
	def fade_to(self,color,speed=0.1):
		try:
			self.fade_to_rgb(self.colors[color],speed)
		except:
			#print("Color {0} is not defined").format(color)
			pass

	def fade_colors(self,color1,color2,speed=0.1):
		try:
			self.fade_colors_rgb(self.colors[color1],self.colors[color2],speed)
		except:
			#print("Color {0} is not defined").format(color)
			pass


	def set_color_rgb(self, rgbcolor):
		PWM.set_duty_cycle(self.r_pin,rgbcolor[0]/2.55)
		PWM.set_duty_cycle(self.g_pin,rgbcolor[1]/2.55)
		PWM.set_duty_cycle(self.b_pin,rgbcolor[2]/2.55)
		#print(rgbcolor)
		#Storing color
		self.color_rgb = rgbcolor

	def fade_to_rgb(self,rgbcolor,speed=0.1):
		self.fade_colors_rgb(self.color_rgb,rgbcolor,speed)

	def fade_colors_rgb(self,rgbcolor1,rgbcolor2,speed=0.1):
		"""	
		Values for color conversion: Best result for me: 

		target_illuminant=d50
		target_rgb=sRGB

		target_illuminant= 
		'a'  'b' 'c' 'd50' 'd55' 'd65' 'd75' 'e' 'f2' 'f7' 'f11'

		target_rgb=
		'adobe_rgb' 'apple_rgb' 'best_rgb' 'bruce_rgb' 'cie_rgb' 'colormatch_rgb' 'don_rgb_4' 'eci_rgb' 'ekta_space_ps5' 'ntsc_rgb' 'pal_secam_rgb' 'prophoto_rgb' 'smpte_c_rgb' 'srgb' 'wide_gamut_rgb' 
		"""

		rgb1 = RGBColor(rgbcolor1[0],rgbcolor1[1],rgbcolor1[2])
		rgb2 = RGBColor(rgbcolor2[0],rgbcolor2[1],rgbcolor2[2])
		l1 = rgb1.convert_to('lab',target_illuminant='d50')
		l2 = rgb2.convert_to('lab',target_illuminant='d50')
		lab1 =[l1.lab_l,l1.lab_a,l1.lab_b]
		lab2 =[l2.lab_l,l2.lab_a,l2.lab_b]

		for i in range(0,self.fade_steps+1):
			l=self.transition3(i,self.fade_steps,lab1,lab2)
			lab=LabColor(l[0],l[1],l[2])
			r=lab.convert_to('rgb')
			rgb=[r.rgb_r,r.rgb_g,r.rgb_b]
			self.set_color_rgb(rgb)
			sleep(speed)
