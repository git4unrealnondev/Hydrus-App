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
from kivy.clock import Clock, mainthread
from kivy.uix.image import AsyncImage
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.uix.settings import Settings
from kivy.modules import inspector
from kivy.config import ConfigParser
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

import sqlite3
import threading
#import json
import urllib.parse
import os
import re
import time

from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue

#http://127.0.0.1:45869

	#DONE make back button for fileview
	#DONE "Search" text is too small
	#DONE dont clear search text
	#TODO MAKE SETTINGS ACTUALLY DO SOMTHING
	#TODO make settings have option for default grid image spacer
	#DONE MAKE TEXT USE SQLITE
	#TODO make gridimgs use screenspace to find out how many collums to place

def Blank(self, ins):
		return

class SettingsSlider(Widget):
	text = StringProperty()
	key = NumericProperty()
	SliderValue = NumericProperty()
	def __init__(self, text, key):
		super(SettingsSlider, self).__init__()
		self.text = text
		self.key = key
	def sliderUpdate(self, sliderRef):
		self.SliderValue = sliderRef.value
		#print(sliderRef.value, "slider value")
		datacon = data("Everything.db")
		cur = datacon.GiveCon()
		cur.execute("""UPDATE 'Settings' SET Key = ? WHERE SettingName = ?""", (int(sliderRef.value), self.text))
		
		datacon.dbcommit()
		del datacon

		SettingsWindow.reloadSettings(self)

def DownloadFiles(self, url, List, Update, PassParams, ext, currentOffset):
	global StopThreads
	global access_key

	cnt = 0
	if currentOffset != -1:
		self.DLoader = self
	filelist = []
	try:
		maingrid = self.maingrid

		print('currentoffset', currentOffset, 'Self Offset', self.Offset)

	except AttributeError:

		# This should only happen when grid imgs dont need to be updated.
		print ('Download Files self is not SecondWindow')
		headers = {'Hydrus-Client-API-Access-Key': str(access_key)}
		r = UrlRequest('http://' + str(ip) + ':45869' + '/' + str(url) + str(List[0]), req_headers=headers,  timeout=5, file_path='tmp/' + str(List[0]) + str(ext),on_failure=MainWindow.connectFailure, on_error=MainWindow.connectError)
		r.wait()
		return
	if not List:
		return

	cnt = 0

	for each in List:
		headers = {'Hydrus-Client-API-Access-Key': str(access_key)}
		r = UrlRequest('http://' + str(ip) + ':45869' + '/' + str(url) + str(each), req_headers=headers,  timeout=5, file_path='tmp/' + str(each) + str(ext),on_failure=MainWindow.connectFailure, on_error=MainWindow.connectError)
		r.wait()
		valid = True
		#if cnt >= 50:
		#	print ('cnt over 50')
		#	valid = False #Stops any infinite loops
		#	return
		#print ('GRID IMGS UPDATE LISTDL',self.listdl,' two: ',two)
		#while SecondWindow.childs[49-cnt].source == 'imgs/bk.png':
		while valid:
			if cnt >= 50:
				print ('DLFILES BREAK')
				break
			if SecondWindow.childs[49-cnt].source == 'imgs/bk.png':
				#print (one,SecondWindow.childs[cnt])
				print ('Update')
				SecondWindow.UpdateImage('tmp/'+str(each)+str(ext), cnt)	
				#print ('set Child Source')
				
				valid = False
			cnt += 1
	#print (self, url, List, Update, PassParams, ext)
	#if not List:
	#	return
	#else:
	#	processes = []
	#	with ThreadPoolExecutor(max_workers=20) as executor:
	#		
	#		for each in List:
	#			if StopThreads == True:
	#				try:
	#					executor.cancel()
	#				except AttributeError:
	#					print ('Fixed DownloadFiles Thread Stopper by making the thread error') 
	#			
	#				return
	#			File = processes.append(executor.submit(DownloadFilesSlave(self, freeconnect, ip, url, access_key, each, True, Update, PassParams, ext)))
	#	return filelist	

#def DownloadFilesSlave(self, Func, ipaddr, page, key, eachvar , boolTF, Update, PassParams, ext):
#	print ('DL Post ID: ' + str(eachvar))
#	File = Func(ipaddr, page, key, eachvar, boolTF)
#	print ('tmp/' + str(eachvar) + str(ext))
#	img = open('tmp/' + str(eachvar) + str(ext), 'wb')
#	img.write(File.content)
#	img.close()
#	time.sleep(.5)
#	if Update == None:
#		print ('update==none')
#	else:
#		Load = PassParams[0]
#		PassParams.clear()
#		PassParams.append(int(eachvar))
#		PassParams.append(Load)
#		PassParams.append('')	
#		Load = ''	
#		if eachvar in self.listdl:
#			Update(self, PassParams[0], PassParams[1], PassParams[2])

def freeconnect(ip, page, key, tags, Check):
	try:
		headers = {'Hydrus-Client-API-Access-Key': str(key)}
		print ('http://' + str(ip) + ':45869' + '/' + str(page) + str(tags))

		r = UrlRequest('http://' + str(ip) + ':45869' + '/' + str(page) + str(tags), req_headers=headers,  timeout=5, on_failure=connectFailure, on_error=connectError)
		r.wait()
		#r = requests.get('http://' + str(ip) + ':45869' + '/' + str(page) + str(tags), headers=headers)
		print ('rdone')
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

# Handles FreeConnect Errors
def connectError():
	print ('connecterror')
def connectFailure():
	print('connectfail')

#def freeconnectPassthrough(self, *args):
	
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
	ScrollList = []

	def pickSettings(self, numone, numtwo):
		global settingsList
		if numtwo == None:
			return settingsList[numone]
		return settingsList[numone][numtwo]

	def reloadSettings(self):
		print ('RELOAD SETTINGS')
		global settingsList
		c = data('Everything.db')
		Names = data.Execute(c, "select SettingName from Settings").fetchall()
		Literals = data.Execute(c, "select Literal from Settings").fetchall()
		Keys = data.Execute(c, "select Key from Settings").fetchall()
		toolTips = data.Execute(c, "select toolTips from Settings").fetchall()
		settingsList = []
		settingsList.append(Names)
		settingsList.append(Literals)
		settingsList.append(Keys)
		settingsList.append(toolTips)
		return

	def load_content(self):
		cnt = 0
		SettingsWindow.reloadSettings(self)
		Names = SettingsWindow.pickSettings(self, 0, None)
		Literal = SettingsWindow.pickSettings(self, 1, None)
		Keys = SettingsWindow.pickSettings(self, 2, None)

		# Clears settings scrollwheel from children
		self.ids.Scroll.clear_widgets(children=None)

		for each in Names:
			print ('load_content', cnt, each[0])
			slider = SettingsSlider(Names[cnt][0], Keys[cnt][0])
			print (slider.text, 'slider text')
			self.ids.Scroll.add_widget(slider)
			cnt += 1

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
			DownloadFiles(FileView, 'get_files/file?file_id=',List, None, '', '.image', -1)
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


class data:
	def __init__(self, dbname, **kwargs):
		self.con=sqlite3.connect(dbname)
	def __del__(self, **kwargs):
		self.con.close()
	def dbcommit(self, **kwargs):
		self.con.commit()
	def createtable(self, **kwargs):
		self.con.execute('create table db(ind,w)')
		self.dbcommit()

	def GiveCon(self):
		return self.con

	def Execute(self, string, *argv):
		for arg in argv:
        		print ("another arg through *argv :", arg)
		return self.con.execute(string)

	def WriteSettings(self, string1, string2, string3, *argv):
		self.con.execute("""INSERT INTO 'Settings' (SettingName, Literal, Key) VALUES (?, ?, ?);""", (str(string1), str(string2), str(string3)))
		self.dbcommit()
	def Write(self, string1, string2, *argv):
		self.con.execute("""INSERT INTO 'StoredData' (IP, Key) VALUES (?, ?);""", (str(string1), str(string2)))
		self.dbcommit()
	def Close(self):
		self.con.close()

class MainWindow(Screen):
	def readtxt(self):
		if os.path.exists('txt') == False:
			os.makedirs('./txt/')
			os.makedirs('./tmp/')
			c = data('Everything.db')
			data.Execute(c, '''CREATE TABLE StoredData (IP text, Key text)''')
			data.Execute(c, '''CREATE TABLE Settings (SettingName text, Literal text, Key test, toolTips text)''')
			data.WriteSettings(c, 'GridNum', 'FALSE', '3', 'maingrids item number width')
			data.Close(c)
		else:
			for child in [child for child in self.textlayout.children]:
				self.textlayout.remove_widget(child)
			for child in [child for child in self.xtextlayout.children]:
				self.xtextlayout.remove_widget(child)
		c = data('Everything.db')
		conn = data.GiveCon(c)
		cur = conn.cursor()
		List = cur.execute("select * from StoredData").fetchall() # Connects To Everything.db and pulls IP's and ther accesskeys
		IPS = cur.execute("select IP from StoredData").fetchall()
		KEYS = cur.execute("select Key from StoredData").fetchall()
		print ('List ',len (List))
		print ('IPS',IPS)
		print ('KEYS',KEYS)
		data.Close(c)
		cnt = 0
		while cnt < len(List):
			print (KEYS[cnt])
			if not str(KEYS[cnt]) == "('None',)":
				self.textlayout.add_widget(Button(text='Saved Entry: ' + str(IPS[cnt][0]), id=str(cnt), on_press=self.pressed))
				self.xtextlayout.add_widget(Button(text='X', on_press=self.Delete, id=str(cnt)))
			cnt += 1
		return
				
	def connect(self, event):
		self.event = event
		global access_key
		global ip
		ip = self.ipinput.text
		ReqHeader = {'User-Agent': 'Hydrus Utilize - Mobile'}
		try:
			r = UrlRequest('http://' + self.ipinput.text + ':45869' + '/request_new_permissions?name=Hydrus%20Mobile%20App&basic_permissions=[0,1,2,3,4]', req_headers=ReqHeader, on_success=MainWindow.connectContinue, timeout=5, on_failure=MainWindow.connectFailure, on_error=MainWindow.connectError)
			#print ('r',r)
			#r = requests.get('http://' + self.ipinput.text + ':45869' + '/request_new_permissions?name=Hydrus%20Mobile%20App&basic_permissions=[0,1,2,3,4]', headers=ReqHeader)
		#except:
		except Exception as e: 
			makepopup('Tell DEV THIS MW CON.',str(type(e)) + str(e) + ' ' + str(e.args))
			return
	
	# Client Isnt accepting any new Connections
	def connectFailure(self, *args):
		makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Please goto  Services->Review->Client-API \n Click Add -> From API request and try again.')
		return
	# Issue making connection to server either IP or firewall misconfigured
	def connectError(self, *args):
		makepopup('Connection Failure','ERROR CANT \n CONNECT TO SERVER')
		return
	# Connection From connect was good, This node parses and writes valid info into local database.
	def connectContinue(self,*args):
		print (args[0])
		if args[0] != 84: # Old error checking code, just leaving it in case...
			access_key = args[0].get("access_key")
			c = data('Everything.db')
			urlString = str(self.url).split('/', 5)[2]
			urlString = str(urlString).split(':', 2)[0]
			data.Write(c, str(urlString), access_key)
			data.Close(c)
		else:
			makepopup('ConnectContinue', 'Error Unknown PassTrough')
			return

		# Makes the screen transition towards the second screen
		sm.current='second'
		sm.transition.direction = 'up'

	def Delete(self, instance):
		c = data('Everything.db')
		conn = data.GiveCon(c)
		cur = conn.cursor()
		List = cur.execute("select * from StoredData").fetchall() # Connects To Everything.db and pulls IP's and ther accesskeys
		IPS = cur.execute("select IP from StoredData").fetchall()
		KEYS = cur.execute("select Key from StoredData").fetchall()
		key = str(KEYS[int(instance.id)][0])
		cur.execute("DELETE FROM StoredData WHERE Key = (?)", (str(KEYS[int(instance.id)][0]),))
		data.dbcommit(c)
		data.Close(c)
		self.textlayout.clear_widgets(children=None)
		MainWindow.readtxt(self)

	def pressed(self, instance): # Gets Called from the dynamically created buttons.
		self.instance = instance
		global access_key
		global ip
		c = data('Everything.db')
		conn = data.GiveCon(c)
		cur = conn.cursor()
		IPS = cur.execute("select IP from StoredData").fetchall()
		KEYS = cur.execute("select Key from StoredData").fetchall()
		data.Close(c)

		ip = IPS[int(instance.id)][0]
		access_key = KEYS[int(instance.id)][0]

		try:
			r = freeconnect(IPS[int(instance.id)][0], 'verify_access_key', KEYS[int(instance.id)][0], '', False)
		except:
			makepopup('Failed to connect', 'Failed to make connection to Hydrus Client \n Please check if API KEY is valid \n Hydrus keys expire every 24 hrs')
			return
		print ('r',r)
		if r == 'Did not find an entry for that access key!':
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
	OneTrigger = True
	label_size = int(15)
	LocalFiles = []
	listdl = []
	SettingsWindow.reloadSettings('BEANS')
	settings = settingsList

	#print ('loaded list',loadedsettingsList[2][0])
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
				self.DLoader.cnt = 0
		if str(event) == 'Right':
			gtrthen = self.Offset + 1

			if SecondWindow.childs[0].source != 'imgs/bk.png': # Stops User from going right until their page is filled

				if len(self.listdl) > gtrthen * 50:
					self.Offset += 1
					SecondWindow.ClearAndUpdateGrid(self)
					self.DLoader.cnt = 0

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
		#self.LocalFiles = [int(os.path.splitext(filename)[0]) for filename in os.listdir('tmp/')]

		while not self.LocalFiles:
			print ('no local files')
			time.sleep(.5)
		print ('LENGTH LOCAL FILES', self.LocalFiles)
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
		global access_key
		self.ids.searching.size_hint = (1, 1)
		print (str(SecondWindow.ptags))
		r = freeconnect(ip, 'get_files/search_files?', access_key, '&tags=' + SecondWindow.ptags, False)
		self.searching.size_hint = (0, 0)
		self.ConnSuccessful = True
		List = r.result.get("file_ids")
		if len(List) == 0:
			return
		print (str(len(List)))
		SecondWindow.listdl = List
		num = str(len(List))
		self.update_label_text('1', num)
		SecondWindow.three = str(len(List))
		CurrentFiles = [int(os.path.splitext(filename)[0]) for filename in os.listdir('tmp/')]
		CurrentFiles = [x for x in CurrentFiles if x in List] # Seperates files that we have locally, doesn't allow other files from other searches to get inside.
		self.LocalFiles = CurrentFiles
		ListToDL = [Files for Files in List if Files not in CurrentFiles]
		print ('listtodl', ListToDL)
		temp = [List]
		currentOffset = self.Offset
		FileList = DownloadFiles(SecondWindow, 'get_files/thumbnail?file_id=',ListToDL, SecondWindow.GridImgsUpdateImage, temp, '.thumbnail', currentOffset)
		#self.DLoader = FileList
		#print ('DLOADER',DLoader)
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
			if self.OneTrigger == True:
				self.search.text = ''
			SecondWindow.IsFocused = True
			self.OneTrigger = False

	def load_content(self): # Used for drawing Images
		global settingsList

		maingrid = self.maingrid
		cnt = 0
		# Waits till settingsList is populated
		while not settingsList:
			print ('load content')
			SettingsWindow.reloadSettings('BEANS')

			time.sleep(.5)
			print ('waiting for settings list')
		if self.settings != settingsList:

			self.settings = settingsList
		print ('settingslist', settingsList)

		self.ids.maingrid.clear_widgets(children=None)

		maingrid.cols = settingsList[2][0][0]

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
			#self.label.text = 'test'
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

Builder.load_file('app.kv')

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
	global settingsList
	settingsList = []
	
	MyMainApp().run()
