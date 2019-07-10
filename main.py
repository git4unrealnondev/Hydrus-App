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
from kivy.uix.image import AsyncImage
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

import threading
import json
import requests
import urllib.parse
import os
import re
import concurrent.futures


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


<SecondWindow>:
	label: btn1
	navdrawer: navdrawer
	maingrid: maingrid
	search: Search
	close_navdrawer: close_navdrawer
	lbl1: lbl1
	lbl3: lbl3
	on_pre_enter:
		root.load_content()
	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			size_hint: (1, .1)
			opacity: 1
			Button:
				opacity: 0
				text: 'Hello world'
				size_hint: (.1, 1)
				on_press:
					root.label_change('navdrawer')
				Image:
					opacity: 1
					source: 'imgs/Light.jpg'
					center_x: self.parent.center_x
					center_y: self.parent.center_y
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
				size_hint: (.1, .1)
				Button:
					id: lbl1
					text: '0'
				Button:
					id: lbl2
					text: '/'
				Button:
					id: lbl3
					text: '0'
		ScrollView:
			size_hint: 1,.8
			do_scroll_x: False
			do_scroll_y: True
			GridLayout:
				padding: 5
				cols: 3
				spacing: (5,5)
				id: maingrid

		Button:
			size_hint: 1,.1
			id: btn1
			text: 'Logout'
			on_release:

				app.root.current = 'main'
				root.manager.transition.direction = 'down'


	FloatLayout:
		AnchorLayout:
			anchor_x: 'left'
			anchor_y: 'center'
		
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
                            size_hint: (1, .5)
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
                                text: 'test1'
                                on_press:
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

		orientation: 'horizontal'

		BoxLayout:
			opacity: 0
			
			Button:

		Button:
			opacity: 1
			size_hint_x: .2	

			text: 'EE'
			on_press:
				app.root.current = 'second'
				root.manager.transition.direction = 'left'
	BoxLayout:
		size_hint: (1, .9)
		Button:
			text: 'MAIN WINDOW'

""")

def ThreadedFreeConnect(job):
    freeconnect(job[0],job[1],job[2],job[3],job[4],)


def StartThreading(enum , num, query):

	q = Queue()

	for x in range(num):
		t = threading.Thread(target = worker_thread)
		t.daemon = True
		t.start()
	

	if enum == 'freeconnect':
		print (len(query))
		wrknum = len(query) / 5
		t1 = threading.Thread(target=ThreadedFreeConnect(query), name='t1')
		t1.start()
		t1.join()


def Blank(self, ins):
		return

def PullFiles(self, List):
	filelist = []
	maingrid = self.maingrid
	if not List:
		return
	else:
		cnt = 0
		print (len(List))
		for each in List:
			File = freeconnect(ip, 'get_files/thumbnail?file_id=', access_key, each, True)
			#print (str(maingrid.children))
			filelist.append(File)
		return filelist	


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
	def load_content(self):
		print ('hello')

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
					test.bind(on_press=pressed)
					self.add_widget(self.test)
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
	lb1tx = StringProperty('0')
	lb3tx = StringProperty('1')

	IsFocused = False
	maingrid = ObjectProperty(None)
	# When you click in/out the input text box it trigger

	def test(self, test):
		print ('test')
		return

	def on_focus(self, value):
		#print (SecondWindow.IsFocused)
		#self.value = value
		#value = self.value
		global access_key
		global ip
		
		if SecondWindow.IsFocused == True:
			SecondWindow.IsFocused = False
				#print (self.search.text)
			
			if self.search.text == '':
				return
			
			ptags = re.sub(' ','", "',self.search.text)
			ptags = re.sub('^','["',ptags)
			ptags = re.sub('$','"]',ptags)
			ptags = urllib.parse.quote(ptags.encode('utf-8'))

			future = executor.submit(freeconnect, ip, 'get_files/search_files?system_inbox=true&system_archive=true', access_key, '&tags=' + ptags, False)
			print(future.result())

			#r = freeconnect(ip, 'get_files/search_files?system_inbox=true&system_archive=true', access_key, '&tags=' + ptags, False)
			r = future.json()
	
			List = r['file_ids']
			if len(List) == 0:
				return
			
			self.lbl1.text = str(len(List))
			FileList = PullFiles(self, List)
			maingrid = self.maingrid
			childs = []
			cnt = 0

			for child in maingrid.children[:]:	
				childs.append(child)
			if not FileList:
				return

			for Imgs in FileList:
				print ('LOOP')
				if not os.path.exists('tmp/'+ str(List[cnt]) + '.thumbnail'):
					print ('Writing File')
					img = open('tmp/' + str(List[cnt]) + '.thumbnail', 'wb')
					#print (FileList[cnt].content)
					img.write(FileList[cnt].content)
					img.close()
				if not FileList[cnt]:
					return
				if FileList[cnt]:
					try:
						fle = 'GridImgs'+str(cnt)
						childs[49 - cnt].source = 'tmp/' + str(List[cnt]) + '.thumbnail'
					except IndexError:
						print ('Break')
						break
				cnt +=1
			
			cnt = 0
			
				
	
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
			maingrid.add_widget(ImageButton(size_hint_y=None, id='GridImgs' + str(cnt),allow_stretch=True, source='imgs/Light.jpg', on_press=self.test))
			#print ('GridImgs'+str(cnt))
			search = self.search
			search.selection_text
			cnt += 1
	def label_change(self, event):
		self.event = event
		if self.event == "btn1":
			self.label.text = test
			return
		if self.event == "navdrawer":
			self.navdrawer.opacity = 1
			self.navdrawer.size_hint = (.5,1)
			self.close_navdrawer.size_hint = (.5,1)
			return
		if self.event == "close_navdrawer":
			self.navdrawer.opacity = 0
			self.navdrawer.size_hint = (0,1)
			self.close_navdrawer.size_hint = (0,1)
			return


#close_navdrawer

sm = ScreenManager()
sm.add_widget(MainWindow(name='main'))
sm.add_widget(SecondWindow(name='second'))
sm.add_widget(SettingsWindow(name='setting'))

class MyMainApp(App):


	def build(self):
	        return sm


if __name__ == "__main__":
	executor = None

	executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

	MyMainApp().run()

#https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.ko1gn6b40NIt2aRjymUirgHaHa%26pid%3DApi&f=1
