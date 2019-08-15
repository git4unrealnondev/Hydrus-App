from kivy.app import App
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics.texture import Texture
from kivy.garden.navigationdrawer import NavigationDrawer as ND
from kivy.clock import Clock, mainthread
from kivy.uix.image import AsyncImage
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.settings import Settings
from kivy.modules import inspector

import threading
import json
import requests
import urllib.parse
import os
import re
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

#http://127.0.0.1:45869

Builder.load_string(
"""
<MainWindow>:
	ipinput: IPinput
	textlayout: textlayout
	xtextlayout: xtextlayout
	on_pre_enter:
		root.readtxt()
	canvas:
		Color:
			rgb: 0,0,0
		Rectangle:
			#rgba: 1,1,1,1
			#source: 'imgs/bk.png'
			size: self.size
	BoxLayout:

		orientation: 'vertical'
		background_normal: ''
		background_color: 0, 1, 0, 1
		AnchorLayout:
			anchor_x: 'center'
			anchor_y: 'top'
			padding: [25, 10, 25 ,10]

			GridLayout:
				size_hint: (.5, .25)
				cols:1
				GridLayout:

					cols: 2
					Label:
						background_color: (1.0, 0.0, 0.0, 1.0)
						text: 'IP: '
					TextInput:
						id: IPinput
						text: '127.0.0.1'
						multiline: False
				Button:

					text: 'Submit'
					on_press:
						root.connect('ipinput')




		GridLayout:
			cols: 1
			AnchorLayout:
				anchor_x: 'center'
				anchor_y: 'center'
				padding: [25, 10, 25 ,10]
				BoxLayout:
					GridLayout:
						size_hint: .8, .2
						id: textlayout
						cols: 1
					GridLayout
						size_hint: .2, .2
						id: xtextlayout
						cols: 1

<FileView>:
	on_pre_enter:
		root.load_content()
	imageref: image
	ScrollView:
		do_scroll_x: False
		do_scroll_y: True
		GridLayout:
			cols: 1
			size_hint_y: None
			height: self.minimum_height
			row_default_height: '40dp'
			FileViewImage:
				size_hint: 1, None
				width: root.width
				height: self.width / self.image_ratio
				size: self.size
				id: image				
			BoxLayout:

				Button:
					text: '<-'
					on_press:
						root.Transition('Left')
				Button:
					opacity: 0
				Button:
					text: '->'
					on_press:
						root.Transition('Right')
			
<SecondWindow>:
	label: btn1
	navdrawer: navdrawer
	maingrid: maingrid
	search: Search
	close_navdrawer: close_navdrawer
	lbl1: lbl1
	lbl3: lbl3
	searching: searching
	on_pre_enter:
		root.load_content()
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			size_hint: (1, .1)
			opacity: 1
			ImageButton:
				keep_ratio: False
				allow_stretch: True
				size: self.parent.size
				x: self.parent.width * .5 - self.width * .5
				source: 'imgs/Hydrus3Bar.png'
				size_hint: (.2, 1)
				on_press:
					root.label_change('navdrawer')
			BoxLayout:
				TextInput:
					id: Search
					text: 'Search'
					multiline: False
					size_hint: (.8, 1)
					on_focus:
						root.on_focus('search')
		AnchorLayout:
			anchor_x: 'center'
			size_hint: (1, .1)
			BoxLayout:
				spacing: 20
				padding: (10,1,10,1)
				Button:
					text: ' <- '
					on_press:
						root.IncrementPage('Left')
				Label:
					id: lbl1
					size_hint: (.25,1)
					text: '0'
				Label:
					id: lbl2
					size_hint: (.25,1)
					text: '-'
				Label:
					id: lbl3
					size_hint: (.25,1)
					text: '0'
				Button:
					text: ' -> '
					on_press:
						root.IncrementPage('Right')

		ScrollView:
			size_hint: 1,.8
			do_scroll_x: False
			do_scroll_y: True
			GridLayout:
				row_default_height: 100
				#col_default_width: 50
				height: self.minimum_height
				size_hint_y: None
				padding: 5
				cols: 3
				spacing: (5,5)
				id: maingrid

		Button:
			size_hint: 1,.1
			id: btn1
			text: 'Logout'
			on_release:
				root.label_change('btn1')
				app.root.current = 'main'
				root.manager.transition.direction = 'down'


	AnchorLayout:
		anchor_x: 'center'
		anchor_y: 'center'
		id: searching
		size_hint: (0,0)
		BoxLayout:
			size_hint: (.3, .15)
			canvas:
				Color:
					rgba: 74/225, 109/255, 186/255, .8 # Hydrus Blue
				Rectangle:
					pos: self.pos
					size: self.size
			Button:
				background_normal: ''
				background_color: 0,0,0,0

				halign: 'center'
				text: 'Searching (This Is Static)'
				
				
					
	FloatLayout:
		AnchorLayout:
			anchor_x: 'left'
			anchor_y: 'center'
			ScrollView:
				id: navdrawer
				size_hint: (0, 1)
				do_scroll_x: False
				do_scroll_y: True

                BoxLayout:

                    size_hint: (1, 1)
                    canvas:
                        Color:
                            rgba: 74/225, 109/255, 186/255, .8 # Hydrus Blue
                        Rectangle:
                            pos: self.pos
                            size: self.size
                    AnchorLayout:
                        anchor_y: 'top'
                        BoxLayout:
                            size_hint: (1, .75)
                            orientation: 'vertical'
                            Button:
                                size_hint: (1, .1)
                                text: 'Settings'
                                on_release:
                                    app.root.current = 'setting'
                                    root.manager.transition.direction = 'right'
                            Button:
                                size_hint: (1, .1)
                                text: 'test1'
                                on_press:
                            Button:
                                size_hint: (1, .1)
                                text: 'test1'
                                on_press:
                            Button:
                                size_hint: (1, .1)
                                text: 'Exit'
                                on_press:
                                    root.triggerexit('exit')
		AnchorLayout:
			anchor_x: 'right'
			anchor_y: 'center'
			Button:
				id: close_navdrawer
				opacity: 0
				text: 'TEST'
				size_hint: (0, 1)
				on_press:
					root.label_change('close_navdrawer')
<SettingsWindow>:
	on_pre_enter:
		root.load_content()
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			canvas:
				Color:
					rgba: 74/225, 109/255, 186/255, .8 # Hydrus Blue
				Rectangle:
					pos: self.pos
					size: self.size
			size_hint: (1,.2)
			BoxLayout:
				size_hint: (.8, 1)
				Button:
					opacity: 0
					
			BoxLayout:
				size_hint: (.2, 1)
				ImageButton:
					keep_ratio: False
					allow_stretch: True
					x: self.parent.width * .5 - self.width * .5
					source: 'imgs/HydrusArrowR.png'
					allow_stretch: True
					size: self.parent.size
					on_press:
						app.root.current = 'second'
						root.manager.transition.direction = 'left'




		BoxLayout:
			size_hint: (1,.8)
			Button:
				hallign: 'center'
				text: root.text

""")

def Blank(self, ins):
		return

def DownloadFiles(self, url, List, Update, PassParams, ext):
	global StopThreads
	filelist = []
	try:
		maingrid = self.maingrid
	except AttributeError:
		print ('Download Files self is not SecondWindo')
	print (self, url, List, Update, PassParams, ext)
	if not List:
		return
	else:
		processes = []
		with ThreadPoolExecutor(max_workers=20) as executor:
			
			for each in List:
				if StopThreads == True:
					executor.cancel()
					return
				File = processes.append(executor.submit(DownloadFilesSlave(self, freeconnect, ip, url, access_key, each, True, Update, PassParams, ext)))
		return filelist	
def DownloadFilesSlave(self, Func, ipaddr, page, key, eachvar , boolTF, Update, PassParams, ext):
	print ('DL Post ID: ' + str(eachvar))
	File = Func(ipaddr, page, key, eachvar, boolTF)
	print ('tmp/' + str(eachvar) + str(ext))
	img = open('tmp/' + str(eachvar) + str(ext), 'wb')
	img.write(File.content)
	img.close()
	time.sleep(.5)
	if Update == None:
		print ('update==none')
	else:
		Load = PassParams[0]
		PassParams.clear()
		PassParams.append(int(eachvar))
		PassParams.append(Load)
		PassParams.append('')	
		Load = ''	
		
		if eachvar in self.listdl:
			Update(self, PassParams[0], PassParams[1], PassParams[2])

		

def freeconnect(ip, page, key, tags, Check):
	try:
		headers = {'Hydrus-Client-API-Access-Key': str(key)}
		print ('http://' + str(ip) + ':45869' + '/' + str(page) + str(tags))
		r = requests.get('http://' + str(ip) + ':45869' + '/' + str(page) + str(tags), headers=headers)

	except:
		if not Check == True:
			print ('check != True')
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Is it on or configured correctly?')
			return
		if r.content[0] == 84:
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Please goto  Services->Review->Client-API \n Click Add -> From API request and try again.')
			return
		else:
			return r
	return r

def makepopup(title, text):
	box = BoxLayout(orientation = 'vertical', padding = (10))
	box.add_widget(Label(text = text, halign = 'center', size_hint_y=None, font_size=(11)))
	btn1 = Button(text='Close Me')
	box.add_widget(btn1)
	popup = Popup(title=title, content=box, auto_dismiss=False, size_hint=(.97, .5))
	btn1.bind(on_press = popup.dismiss)
	popup.open()

class ImageButton(ButtonBehavior, Image):
	pass

class Grid(FloatLayout):
	pass

class SettingsWindow(Screen):
	text = 'Lazy Developer - Tell Me what you\nwant to edit\nin the settings\ni am a bad dev'
	def load_content(self):
		print ('Settings Window')

class FileViewImage(ButtonBehavior, Image): # This handles the Touch Events in FileView's main image
	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			Direction = 'None'
			if self.width / 3 >= touch.pos[0]:
				Direction = 'Left'
				App.get_running_app().root.current_screen.Transition(Direction)
			if self.width / 3 * 2 <= touch.pos[0]:
				Direction = 'Right'
				App.get_running_app().root.current_screen.Transition(Direction)
			print (str(touch.pos), self.width, Direction)
			return False

class FileView(Screen):
	position = 0
	image = 'imgs/Light.jpg'
	
	def Transition(self, Direction):
		print (self.position)
		if Direction == 'Left':
			if not FileView.position == 49:
				FileView.position += 1
				FileView.LoadImage(self)
		else:
			if Direction == 'Right':
				if not FileView.position == 0:
					FileView.position -= 1
					FileView.LoadImage(self)
			else:
				print ('FileView - No Valid Direction Specified')

	def load_content(self):
		self.SelfRef = self
		FileView.LoadImage(self)

	def LoadImage(self):
		FileID = FileView.findid(self, FileView.position)
		if os.path.isfile('tmp/' + FileID + '.image'):
			print ('File Exists')
			self.imageref.source = 'tmp/' + FileID + '.image'
			x,y = Window.size
			print ('Image Ratio ',str(self.imageref.image_ratio), 'Window Size', str(Window.size))
		else:
			List = []
			List.append(FileID)
			DownloadFiles(FileView, 'get_files/file?file_id=',List, None, '', '.image')
			self.imageref.source = 'tmp/' + FileID + '.image'
			x,y = Window.size
			print ('Image Ratio ',str(self.imageref.image_ratio), 'Window Size', str(Window.size))

	def findid(self, childpos):
		IDToParse = str(SecondWindow.childs[childpos].source)
		IDToParse = IDToParse.rsplit('/', 1)[-1]
		IDToParse = IDToParse.rsplit('.', 1)[0]
		return IDToParse

	def ViewImage(self):
		print ('ViewImage')

	def test(self):
		print ('ok')

class MainWindow(Screen):
	def readtxt(self):
		Text = os.path.exists('txt')
		if Text == False:
			os.makedirs('./txt/')
			os.makedirs('./tmp/')
			f = open("./txt/main.txt","w+")
			f.write('')
			f.close()
			f = open("./txt/1.txt","w+")
			f.write('')
			f.close()
			f = open("./txt/2.txt","w+")
			f.write('')
			f.close()
			f = open("./txt/3.txt","w+")
			f.write('')
			f.close()
			f = open("./txt/4.txt","w+")
			f.write('')
			f.close()
		else:
			for child in [child for child in self.textlayout.children]:
				print (child)
				self.textlayout.remove_widget(child)
			for child in [child for child in self.xtextlayout.children]:
				print (child)
				self.xtextlayout.remove_widget(child)
			txtlst = ['main', '1', '2', '3', '4']
			for each in txtlst:

				b = os.path.getsize('txt/' + str(each) + '.txt')

				f = open('txt/' + str(each) + '.txt', 'r')
				read = f.read()
				f.close()
				if b > 0:
					print (each + str(b))
					self.textlayout.add_widget(Button(text='Saved Entry: ' + str(txtlst.index(each)), id='dynbtn' + str(txtlst.index(each)), on_press=self.pressed))
					self.xtextlayout.add_widget(Button(text='X', on_press=self.Delete, id='dynbtn' + str(txtlst.index(each))))
				
	def connect(self, event):
		self.event = event
		global access_key
		global ip
		ip = self.ipinput.text
		ReqHeader = {'User-Agent': 'Hydrus Utilize - Mobile'}
		try:
			r = requests.get('http://' + self.ipinput.text + ':45869' + '/request_new_permissions?name=Hydrus%20Mobile%20App&basic_permissions=[0,1,2,3,4]', headers=ReqHeader)
		except:
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Is it on or configured correctly?')
			return
		if r.content[0] != 84:
			r = json.loads(r.content)
			access_key = r['access_key']
			txtlst = ['main', '1', '2', '3', '4']
			for each in txtlst:
				e = os.path.getsize('txt/' + str(each) + '.txt')
				f = open('txt/' + str(each) + '.txt', 'a')
				if e > 0:
					print (each + 't')
					test = Button(text='Saved Entry: ' + str(txtlst.index(each)))
					test.bind(on_press=self.pressed)
					self.add_widget(test)
					f.close()
				else:
					f.write(self.ipinput.text + ', ' + access_key)
					print (each)
					f.close()
					break
		else:
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Please goto  Services->Review->Client-API \n Click Add -> From API request and try again.')
			return
		# Makes the screen transition towards the second screen
		sm.current='second'
		sm.transition.direction = 'up'

	def Delete(self, instance):
		self.instance = instance
		if instance.id == 'dynbtn0':
			act = 'main'
		if instance.id == 'dynbtn1':
			act = '1'
		if instance.id == 'dynbtn2':
			act = '2'
		if instance.id == 'dynbtn3':
			act = '3'
		if instance.id == 'dynbtn4':
			act = '4'
		try:
			os.remove('txt/'+act+'.txt')
		except FileNotFoundError:
			print ('File' + act + 'Not Found')
		file = open('txt/'+act+'.txt', 'w+')
		file.close()
		self.textlayout.clear_widgets(children=None)
		MainWindow.readtxt(self)

	def pressed(self, instance): # Gets Called from the dynamically created buttons.
		self.instance = instance
		global access_key
		global ip
		if instance.id == 'dynbtn0':
			act = 'main'
		if instance.id == 'dynbtn1':
			act = '1'
		if instance.id == 'dynbtn2':
			act = '2'
		if instance.id == 'dynbtn3':
			act = '3'
		if instance.id == 'dynbtn4':
			act = '4'
		f = open('txt/' + str(act) + '.txt', 'r')

		read = f.read()
		ip = read.split(',', 1)[0]  # maxsplit = 1;
		ak = read.split(',', 1)[1]  # maxsplit = 1;
		ak = ak.replace("\n", "")
		ak = ak.replace(" ", "")
		access_key = ak
		try:
			r = freeconnect(ip, 'verify_access_key', access_key, '', False)
		except:
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Please check if API KEY is valid \n Hydrus keys expire every 24 hrs')
			return
		if r.text == 'Did not find an entry for that access key!':
			return
		if r == None:
			return
		sm.current='second'
		sm.transition.direction = 'up'

	def draw_background(self, *args):
		self.canvas.before.clear()
		with self.canvas.before:
			Color(.4, .4, .4, 1)
			texture = CoreImage("tile.png").texture
			texture.wrap = 'repeat'
			nx = float(widget.width) / texture.width
			ny = float(widget.height) / texture.height
			Rectangle(pos=widget.pos, size=widget.size, texture=texture, tex_coords=(0, 0, nx, 0, nx, ny, 0, ny))

class SecondWindow(Screen):
	IsFocused = False
	maingrid = ObjectProperty(None)
	lbl3 = ObjectProperty(None)
	ConnSuccessful = False
	Offset = 0
	LocalFiles = []
	listdl = []
	def triggerexit(self, event):
		global StopThreads
		global ThreadList
		StopThreads = True
		ThreadList = []
		while StopThreads == True:
			if not ThreadList:
				StopThreads = False
		App.get_running_app().stop()

	def IncrementPage(self, event):
		if self.ConnSuccessful == True:
			print ('I AM CONNECTED ')
		else:
			return
		if str(event) == 'Left':
			if self.Offset != 0:
				self.Offset -= 1
				SecondWindow.ClearAndUpdateGrid(self)
		if str(event) == 'Right':
			gtrthen = self.Offset + 1
			if len(self.listdl) > gtrthen * 50:
				self.Offset += 1
				SecondWindow.ClearAndUpdateGrid(self)

	def ClearAndUpdateGrid(self):
		global ThreadList
		Thread = threading.Thread(target=self.ClearAndUpdateGridFunc, args=()).start()
		ThreadList.append(Thread)
		return

	def ClearAndUpdateGridFunc(self):
		SecondWindow.PopSourcesFunc(self)
		SecondWindow.FileDisplay(self)

	def PopSources(self):
		global ThreadList
		Thread = threading.Thread(target=self.PopSourcesFunc, args=()).start()
		ThreadList.append(Thread)
		return

	def PopSourcesFunc(self):
		cnt = 0
		valid = True
		while valid == True:
			if cnt >= 51:
				valid = False	
			SecondWindow.childs[49-cnt].source = 'imgs/bk.png'
			SecondWindow.UpdateImage('imgs/bk.png', cnt)
			cnt += 1
		return

	def StartFileShowThread(self):
		global ThreadList
		Thread = threading.Thread(target=self.FileDisplay, args=(self,)).start()
		ThreadList.append(Thread)
		return

	def StartFileSearchThread(self):
		global ThreadList
		Thread = threading.Thread(target=self.FileSearch, args=(self,)).start()
		ThreadList.append(Thread)
		return

	def test(self, test):
		if not str(test.source) == 'imgs/bk.png':
			print ('test.source is ',str(test.source))
			FileView.position = int(SecondWindow.childs.index(test))
			self.manager.current = 'fileviewer'
			return
		return

	def FileDisplay(self, *kwargs):
		## Waits till LocalFiles files are populated
		while not self.LocalFiles:
			time.sleep(.5)
		print ('BREAK')
		cnt = 0
		valid = True
		while valid == True:
			if cnt >= 50:
				valid = False
				return
			if cnt == len(self.LocalFiles):
				valid = False
				return
			#print ('loop', SecondWindow.childs[49-cnt].source)
			if SecondWindow.childs[49-cnt].source == 'imgs/bk.png':
				CurrentOffset = self.Offset * 50
				
				print ('Current Offset ', CurrentOffset, len(self.LocalFiles))
				SecondWindow.UpdateImage('tmp/'+str(self.LocalFiles[cnt + CurrentOffset]) +'.thumbnail', cnt)
			else:
				print ('Childs Source Is ',SecondWindow.childs[49-cnt].source)
			cnt += 1

	def GridImgsUpdateImage(self, one, two, three):
		print ('gridimgsupdateimage')
		cnt = 0
		valid = True
		
		#TODO CHECK IF THE UPDATED ITEMS ARE ALREADY IN THE LIST OF SOURCES
		#NON ESSENTIAL WILL FIX LATER
		cnt = 0
		while valid == True:
			if cnt >= 50:
				valid = False #Stops any infinite loops
				return
			#print ('GRID IMGS UPDATE LISTDL',self.listdl,' two: ',two)
			if SecondWindow.childs[49-cnt].source == 'imgs/bk.png':
				#print (one,SecondWindow.childs[cnt])
				SecondWindow.UpdateImage('tmp/'+str(one)+'.thumbnail',cnt)	
				#print ('set Child Source')
				valid = False
			
			cnt += 1

	def FileSearch(self, *kwargs):
		self.ids.searching.size_hint = (1, 1)
		print (str(SecondWindow.ptags))
		r = freeconnect(ip, 'get_files/search_files?', access_key, '&tags=' + SecondWindow.ptags, False)
		self.searching.size_hint = (0, 0)
		self.ConnSuccessful = True
		print ('r.done')
		r = r.json()
		List = r['file_ids']
		if len(List) == 0:
			return
		print (str(len(List)))
		SecondWindow.listdl = List
		num = str(len(List))
		self.update_label_text('1', num)
		SecondWindow.three = str(len(List))
		CurrentFiles = [int(os.path.splitext(filename)[0]) for filename in os.listdir('tmp/')]
		CurrentFiles = [x for x in CurrentFiles if x in List]
		self.LocalFiles = CurrentFiles
		ListToDL = [Files for Files in List if Files not in CurrentFiles]
		print ('listtodl', ListToDL)
		temp = [List]
		FileList = DownloadFiles(SecondWindow, 'get_files/thumbnail?file_id=',ListToDL, SecondWindow.GridImgsUpdateImage, temp, '.thumbnail')
		self.DLoader = FileList
		if not FileList:
			return
		cnt = 0	

	# When you click in/out the input text box it trigger	
	def on_focus(self, value):
		global access_key
		global ip
		global ThreadList
		if SecondWindow.IsFocused == True:
			SecondWindow.IsFocused = False
			if self.search.text == '':
				return
			ptags = re.sub(' ','", "',self.search.text)
			ptags = re.sub('^','["',ptags)
			ptags = re.sub('$','"]',ptags)
			SecondWindow.ptags = urllib.parse.quote(ptags.encode('utf-8'))
			cnt = 0
			valid = True
			while valid == True:
				if cnt >= 52:
					valid = False
				SecondWindow.UpdateImage('imgs/bk.png', cnt)
				cnt += 1
			self.LocalFiles = []
			SecondWindow.StartFileSearchThread(self)
			SecondWindow.StartFileShowThread(self)
		else:
			SecondWindow.IsFocused = True
			self.search.text = ''
        #print (SecondWindow.test) # Debugging for clicking in search bar

	def load_content(self): # Used for drawing Images
		maingrid = self.maingrid
		cnt = 0
		for but in range(50):
			#maingrid.add_widget(Button(size_hint_y=None, id='GridImgs' + str(cnt),background_normal='imgs/Light.jpg',background_down='imgs/Light.jpg'))
			#maingrid.add_widget(Image(size_hint_y=None, id='GridImgs' + str(cnt),allow_stretch=True, source='imgs/Light.jpg'))
			maingrid.add_widget(ImageButton(size_hint_y = 1,keep_ratio = True, allow_stretch = True, id = 'GridImgs' + str(cnt), source ='imgs/bk.png', on_press = self.test))
			#print ('GridImgs'+str(cnt))
			search = self.search
			search.selection_text
			cnt += 1

		maingrid = SecondWindow.maingrid
		childs = []
		try:
			for child in self.ids.maingrid.children[:]:	
				childs.append(child)
			SecondWindow.childs = childs
		except AttributeError:
			print ('FILE DISPLAY ATTRIBUTE ERROR') ## This Shouldn't happen under NORMAL USE
			return

	def label_change(self, event):
		self.event = event
		if self.event == "btn1":
			self.label.text = 'test'
			return
		if self.event == "navdrawer":
			self.navdrawer.opacity = 1
			self.navdrawer.size_hint = (.75,1)
			self.close_navdrawer.size_hint = (.25,1)
			return
		if self.event == "close_navdrawer":
			self.navdrawer.opacity = 0
			self.navdrawer.size_hint = (0,1)
			self.close_navdrawer.size_hint = (0,1)
			return

	@mainthread
	def update_label_text(self, lb1, lb3):
		self.lbl1.text = str(lb1)
		self.lbl3.text = str(lb3)
		return

	@mainthread
	def UpdateImage(tiny,num):
		#print (str(tiny), str(num))
		SecondWindow.childs[49 - num].source = str(tiny)

		return

#close_navdrawer

sm = ScreenManager()
sm.add_widget(MainWindow(name='main'))
sm.add_widget(FileView(name='fileviewer'))
sm.add_widget(SecondWindow(name='second'))
sm.add_widget(SettingsWindow(name='setting'))


class MyMainApp(App):
	def on_stop(self):
		global StopThreads
		StopThreads = True
		self.root.stop = threading.Event()
		self.root.stop.set()
	def build(self):
	        return sm


if __name__ == "__main__":
	global StopThreads
	StopThreads = False
	global ThreadList
	ThreadList = []
	MyMainApp().run()

#https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.ko1gn6b40NIt2aRjymUirgHaHa%26pid%3DApi&f=1
