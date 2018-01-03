# -*- coding: utf-8 -*- 
# MIT license
#
# Copyright (C) 2018 by XESS Corporation / Hildo G Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Author information.
__author__ = 'Hildo Guillardi Junior'
__webpage__ = 'https://github.com/hildogjr/'
__company__ = 'University of Campinas - Brazil'

# Libraries.
import wx # wxWidgets for Python.
import webbrowser
import os, subprocess # To access OS commands and run in the shell.
import platform # To check the system platform when open the XLS file.
from distutils.version import StrictVersion # To comparasion of versions.
import re # Regular expression parser.
#import inspect # To get the internal module and informations of a module/class.
from . import __version__ # Version control by @xesscorp.
from .kicost import *  # kicost core functions.
from .distributors import distributors, FakeBrowser,urlopen # Use the configurations alredy made to get KiCost last version.
from .eda_tools import eda_tool, file_eda_match #from . import eda_tools as eda_tools_imports

__all__ = ['kicost_gui', 'kicost_gui_run']

# Guide definitions.
FILE_HIST_QTY = 10
WILDCARD = "BoM compatible formats (*.xml,*.csv)|*.xml;*.csv|"\
			"KiCad/Altium BoM file (*.xml)|*.xml|" \
			"Proteus/Generic BoM file (*.csv)|*.csv"
CONFIG_FILE = 'KiCost' # Config file for Linux and Windows registry key for KiCost configurations.
PAGE_OFFICIAL = 'https://xesscorp.github.io/KiCost/'
PAGE_UPDATE = 'https://pypi.python.org/pypi/kicost' # Page with the last official version.
#https://github.com/xesscorp/KiCost/blob/master/kicost/version.py

class MyForm ( wx.Frame ):
	
	def __init__( self, parent ):
		#### **  Begin of the guide code generated by wxFormBulilder software, avaliable in <https://github.com/wxFormBuilder/wxFormBuilder/>  ** ####
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"KiCost", pos = wx.DefaultPosition, size = wx.Size( 446,351 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Files" ), wx.HORIZONTAL )
		
		m_comboBox_filesChoices = []
		self.m_comboBox_files = wx.ComboBox( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Files", wx.DefaultPosition, wx.DefaultSize, m_comboBox_filesChoices, 0 )
		self.m_comboBox_files.SetToolTip( u"BoM file(s) to scrape." )
		
		sbSizer2.Add( self.m_comboBox_files, 1, wx.ALL, 5 )
		
		self.m_button_openfile = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Chooose BoM", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_openfile.SetToolTip( u"Open a BoM file." )
		
		sbSizer2.Add( self.m_button_openfile, 0, wx.ALL, 5 )
		
		
		bSizer3.Add( sbSizer2, 0, wx.EXPAND|wx.TOP, 5 )
		
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"Distributors to scrape" ), wx.VERTICAL )
		
		m_checkList_distChoices = [wx.EmptyString]
		self.m_checkList_dist = wx.CheckListBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_checkList_distChoices, 0 )
		self.m_checkList_dist.SetToolTip( u"Web distributor (or local) to scrape the prices." )
		
		sbSizer3.Add( self.m_checkList_dist, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer4.Add( sbSizer3, 1, wx.EXPAND|wx.TOP|wx.LEFT, 5 )
		
		wSizer1 = wx.WrapSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer31 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"EDAs" ), wx.VERTICAL )
		
		m_listBox_edatoolChoices = []
		self.m_listBox_edatool = wx.ListBox( sbSizer31.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBox_edatoolChoices, 0 )
		self.m_listBox_edatool.SetToolTip( u"EDA files supported by KiCost (automacally selected when file is opened)." )
		
		sbSizer31.Add( self.m_listBox_edatool, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( sbSizer31, 1, wx.TOP|wx.RIGHT|wx.EXPAND, 5 )
		
		self.m_button_run = wx.Button( self.m_panel1, wx.ID_ANY, u"KiCost it!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button_run.SetToolTip( u"Rum KiCost as a terminal." )
		
		bSizer6.Add( self.m_button_run, 0, wx.ALL, 5 )
		
		self.m_checkBox_openXLS = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"Open spreadsheet", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_openXLS.SetToolTip( u"Open the spreadsheet after finish the KiCost process." )
		
		bSizer6.Add( self.m_checkBox_openXLS, 0, wx.ALL, 5 )
		
		
		wSizer1.Add( bSizer6, 1, wx.EXPAND|wx.RIGHT, 5 )
		
		
		bSizer4.Add( wSizer1, 1, wx.EXPAND, 5 )
		
		
		bSizer3.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		
		self.m_panel1.SetSizer( bSizer3 )
		self.m_panel1.Layout()
		bSizer3.Fit( self.m_panel1 )
		self.m_notebook1.AddPage( self.m_panel1, u"BoM", True )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		wSizer2 = wx.WrapSizer( wx.HORIZONTAL )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText2 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Parallel process", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer9.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_spinCtrl_np = wx.SpinCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 30, 0 )
		self.m_spinCtrl_np.SetToolTip( u"Set the number of parallel processes used for web scraping part data." )
		
		bSizer9.Add( self.m_spinCtrl_np, 0, wx.ALL, 5 )
		
		self.m_checkBox_overwrite = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Overwrite file", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_overwrite.SetValue(True) 
		self.m_checkBox_overwrite.SetToolTip( u"Allow overwriting of an existing spreadsheet." )
		
		bSizer9.Add( self.m_checkBox_overwrite, 0, wx.ALL, 5 )
		
		
		wSizer2.Add( bSizer9, 1, wx.TOP|wx.LEFT, 5 )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Scrap retries", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer11.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_spinCtrl_retries = wx.SpinCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 4, 200, 0 )
		self.m_spinCtrl_retries.SetToolTip( u"Specify the number of attempts to retrieve part data from a website." )
		
		bSizer11.Add( self.m_spinCtrl_retries, 0, wx.ALL, 5 )
		
		self.m_checkBox_quite = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Quiet mode", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_quite.SetValue(True) 
		self.m_checkBox_quite.SetToolTip( u"Enable quiet mode with no warnings." )
		
		bSizer11.Add( self.m_checkBox_quite, 0, wx.ALL, 5 )
		
		
		wSizer2.Add( bSizer11, 1, wx.TOP|wx.RIGHT, 5 )
		
		
		bSizer8.Add( wSizer2, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Extra commands", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer8.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.m_textCtrlextracmd = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_textCtrlextracmd.SetToolTip( u" Here use the kicost extra commands. In the terminal/command type`kicost --help` to check the list." )
		
		bSizer8.Add( self.m_textCtrlextracmd, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel2.SetSizer( bSizer8 )
		self.m_panel2.Layout()
		bSizer8.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"KiCost config", False )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_bitmap_icon = wx.StaticBitmap( self.m_panel3, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_bitmap_icon, 0, wx.ALL, 5 )
		
		bSizer111 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText_version = wx.StaticText( self.m_panel3, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_version.Wrap( -1 )
		bSizer111.Add( self.m_staticText_version, 1, wx.ALL, 5 )
		
		self.m_staticText_update = wx.StaticText( self.m_panel3, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_update.Wrap( -1 )
		bSizer111.Add( self.m_staticText_update, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( bSizer111, 1, wx.EXPAND, 5 )
		
		
		bSizer2.Add( bSizer10, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText_credits = wx.StaticText( self.m_panel3, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_credits.Wrap( -1 )
		bSizer2.Add( self.m_staticText_credits, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
		
		
		self.m_panel3.SetSizer( bSizer2 )
		self.m_panel3.Layout()
		bSizer2.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, u"About", False )
		
		bSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.app_close )
		self.m_notebook1.Bind( wx.EVT_NOTEBOOK_PAGE_CHANGED, self.wxPanel_change )
		self.m_comboBox_files.Bind( wx.EVT_COMBOBOX, self.m_comboBox_files_selecthist )
		self.m_button_openfile.Bind( wx.EVT_BUTTON, self.button_openfile )
		self.m_button_run.Bind( wx.EVT_BUTTON, self.button_run )
		self.m_bitmap_icon.Bind( wx.EVT_LEFT_DOWN, self.m_bitmap_icon_click )
		
		#### **  End of the guide code generated by wxFormBulilder software, avaliable in <https://github.com/wxFormBuilder/wxFormBuilder/>  ** ####
		
		self.set_properties()
		self.updatedChecked = False
	
	def __del__( self ):
		pass

	# Virtual event handlers, overide them in your derived class

	#----------------------------------------------------------------------
	def app_close( self, event ):
		event.Skip()
		self.save_properties()

	#----------------------------------------------------------------------
	def m_bitmap_icon_click( self, event ):
		event.Skip()
		webbrowser.open(PAGE_OFFICIAL)

	#----------------------------------------------------------------------
	def wxPanel_change( self, event ):
		event.Skip()
		if event.GetSelection()==2: # Is the last page (about page).
			self.checkUpdate()

	#----------------------------------------------------------------------
	def m_comboBox_files_selecthist( self, event):
		event.Skip()
		self.updateEDAselection()

	#----------------------------------------------------------------------
	def updateEDAselection( self ):
		''' Update the EDA selection in the listBox based on the comboBox actual text '''
		fileNames = re.split('" "', self.m_comboBox_files.GetValue()[1:-1])
		if len(fileNames)==1:
			eda = file_eda_match(fileNames[0])
			if eda:
				self.m_listBox_edatool.SetSelection( self.m_listBox_edatool.FindString(eda) )
		elif len(fileNames)>1:
			# Check if all the EDA are the same. For different ones,
			# the guide is not able now to deal, need improvement
			# on `self.m_listBox_edatool`.
			eda = file_eda_match(fileNames[0])
			for fName in fileNames[1:]:
				if file_eda_match(fName) != eda:
					return
			if eda:
				self.m_listBox_edatool.SetSelection( self.m_listBox_edatool.FindString(eda) )

	#----------------------------------------------------------------------
	def checkUpdate( self ):
		''' Check for updates '''
		if not self.updatedChecked:
			self.m_staticText_update.SetLabel('Checking by updates...')
			
			try:
				req = FakeBrowser(PAGE_UPDATE)
				response = urlopen(req)
				html = response.read()
				offical_last_version = re.findall('kicost (\d+\.\d+\.\d+)', str(html), flags=re.IGNORECASE)[0]
				if StrictVersion(offical_last_version) > StrictVersion(__version__):
					self.m_staticText_update.SetLabel('New version (v.'
						+ offical_last_version
						+ ') founded.\nClick <here> to update.')
					self.m_staticText_update.Bind( wx.EVT_LEFT_UP, self.m_staticText_update_click )
				else:
					self.m_staticText_update.SetLabel('KiCost is up to date.')
				
				self.updatedChecked = True
			except:
				self.m_staticText_update.SetLabel('Update information not founded.')

	#----------------------------------------------------------------------
	def m_staticText_update_click( self, event ):
		event.Skip()
		print('Download the update and install -- missing, running manually')
		webbrowser.open(PAGE_UPDATE)

	#----------------------------------------------------------------------
	def button_openfile( self, event ):
		""" Create and show the Open FileDialog """
		event.Skip()
		
		actualDir = (os.getcwd() if self.m_comboBox_files.GetValue() else \
			os.path.dirname(os.path.abspath( self.m_comboBox_files.GetValue() )) )
		
		dlg = wx.FileDialog(
			self, message="Select BoMs",
			defaultDir=actualDir, 
			defaultFile="",
			wildcard=WILDCARD,
			style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
			)
		if dlg.ShowModal() == wx.ID_OK:
			paths = dlg.GetPaths()
			fileBOM = ' '.join(['"' + file + '"' for file in paths])
			if self.m_comboBox_files.FindString(fileBOM)==wx.NOT_FOUND:
				self.m_comboBox_files.Insert( fileBOM, 0 )
			self.m_comboBox_files.SetValue( fileBOM )
			try:
				self.m_comboBox_files.Delete(FILE_HIST_QTY-1) # Keep 10 files on history.
			except:
				pass
			self.updateEDAselection()
		dlg.Destroy()

	#----------------------------------------------------------------------
	def button_run( self, event ):
		''' Run KiCost '''
		event.Skip()
		self.save_properties() # Save the current graphical configuration before call the KiCost motor.
		self.run() # Run KiCost.

	#----------------------------------------------------------------------
	def run( self ):
		# Get the current distributors to scrape.
		choisen_dist = list(self.m_checkList_dist.GetCheckedItems())
		if choisen_dist:
			choisen_dist = [self.m_checkList_dist.GetString(idx) for idx in choisen_dist]
			choisen_dist = ' --include ' + ' '.join(choisen_dist)
		else:
			choisen_dist = ''
		command = ("kicost"
			+ " -i " + self.m_comboBox_files.GetValue()
			+ " -np " + str(self.m_spinCtrl_np.GetValue()) # Parallels process scrapping.
			+ " -rt " + str(self.m_spinCtrl_retries.GetValue()) # Retry time in the scraps.
			+ " -w" * self.m_checkBox_overwrite.GetValue()
			+ " -q" * self.m_checkBox_quite.GetValue()
			+ choisen_dist
			)
		if self.m_listBox_edatool.GetStringSelection():
			command += " -eda " + self.m_listBox_edatool.GetStringSelection()
		if self.m_textCtrlextracmd.GetValue():
			command += ' ' + self.m_textCtrlextracmd.GetValue()
		
		if self.m_checkBox_openXLS.GetValue():
			spreadsheet_file = os.path.splitext( re.sub('"', '', self.m_comboBox_files.GetValue()) )[0] + '.xlsx'
			if platform.system()=='Linux':
				command += ' && xdg-open ' + '"' + spreadsheet_file + '"'
			elif platform.system()=='Windows':
				command += ' && explorer ' + '"' + spreadsheet_file + '"'
			elif platform.system()=='Darwin': # Mac-OS
				command += ' && open -n ' + '"' + spreadsheet_file + '"'
			else:
				print('Not recognized OS.')
		
		command += '&' # Run as other process.
		print("Running: ", command)
		subprocess.call(command, shell=True) # `os.system`not accept the "&&"

	#----------------------------------------------------------------------
	def set_properties(self):
		''' Set the current proprieties of the graphical elements '''
		
		actualDir = os.path.dirname(os.path.abspath(__file__)) # Application dir.
		
		# Set the aplication windows title and configurations
		self.SetTitle('KiCost v.' + __version__)
		self.SetIcon(wx.Icon(actualDir + os.sep + 'kicost.ico', wx.BITMAP_TYPE_ICO))
		
		# Current distrubutors module recognized.
		distributors_list = [*sorted(list(distributors.keys()))]
		self.m_checkList_dist.Clear()
		self.m_checkList_dist.Append(distributors_list)
		for idx in range(len(distributors_list)):
			self.m_checkList_dist.Check(idx,True) # All start checked (after is modifed by the configuration file).
		
		# Current EDA tools module recoginized.
		#eda_names = [o[0] for o in inspect.getmembers(eda_tools_imports) if inspect.ismodule(o[1])]
		eda_names = [*sorted(list(eda_tool.keys()))]
		self.m_listBox_edatool.Clear()
		self.m_listBox_edatool.Append(eda_names)
		
		# Credits and other informations, search by `AUTHOR.rst` file.
		self.m_staticText_version.SetLabel( 'KiCost version ' + __version__ )
		self.m_bitmap_icon.SetIcon(wx.Icon(actualDir + os.sep + 'kicost.ico', wx.BITMAP_TYPE_ICO))
		try:
			credits_file = open(actualDir + os.sep+'..'+os.sep + 'kicost-' + __version__ + '.dist-info' + os.sep + 'AUTHOR.rst')
			credits = credits_file.read()
			credits_file.close()
		except:
			credits = '''=======
			Credits
			=======\n
			Development Lead
			----------------
			* XESS Corporation <info@xess.com>\n
			Contributors
			------------
			* Oliver Martin: https://github.com/oliviermartin
			* Timo Alho: https://github.com/timoalho
			* Steven Johnson: https://github.com/stevenj
			* Diorcet Yann: https://github.com/diorcety
			* Giacinto Luigi Cerone https://github.com/glcerone
			* Hildo Guillardi Júnior https://github.com/hildogjr
			* Adam Heinrich https://github.com/adamheinrich
			'''
			credits = re.sub('[\t, ]+', '', credits)
		self.m_staticText_credits.SetLabel( credits
			+ '\nGraphical interface by ' + __author__ )
		
		# Recovery the last configurations used (found the folder of the file by the OS).
		self.restore_properties()
		
		# Files in the history.
		#if not self.m_comboBox_files.IsListEmpty(): # If have some history, set to the last used file.
		#	self.m_comboBox_files.IsListEmpty(0)

	#----------------------------------------------------------------------
	def restore_properties(self):
		''' Restore the current proprieties of the graphical elements '''
		try:
			configHandle = wx.Config(CONFIG_FILE)
			
			entryCount = 0
			while True:
				entry = configHandle.GetNextEntry(entryCount)
				if not entry[0]:
					break
				entryCount+=1 #Count the entry numbers and go to next one in next iteration.
				entry = entry[1]
				
				try:
					# Find the wxPython element handle to access the methods.
					wxElement_handle = self.__dict__[entry]
					# Each wxPython object have a specific parameter value
					# to be saved and restored in the software initialization.
					if isinstance(wxElement_handle, wx._core.TextCtrl):
						wxElement_handle.SetValue( configHandle.Read(entry) )
					elif isinstance(wxElement_handle, wx._core.CheckBox):
						wxElement_handle.SetValue( (True if configHandle.Read(entry)=='True' else False) )
					elif isinstance(wxElement_handle, wx._core.CheckListBox):
						value = re.split(',', configHandle.Read(entry) )
						for idx in range(wxElement_handle.GetCount()): # Reset all checked.
							wxElement_handle.Check(idx, False)
						for dist_checked in value: # Check only the founded names.
							idx = wxElement_handle.FindString( dist_checked )
							if idx!=wx.NOT_FOUND:
								wxElement_handle.Check(idx, True)
					elif isinstance(wxElement_handle, wx._core.SpinCtrl):
						wxElement_handle.SetValue( int(configHandle.Read(entry)) )
					elif isinstance(wxElement_handle, wx._core.ComboBox):
						value = re.split(',', configHandle.Read(entry) )
						for element in value:
							if element:
								wxElement_handle.Append( element )
					elif isinstance(wxElement_handle, wx._core.ListBox):
						wxElement_handle.SetSelection( wxElement_handle.FindString( configHandle.Read(entry) ) )
					elif isinstance(wxElement_handle, wx._core.Notebook):
						wxElement_handle.SetSelection( int(configHandle.Read(entry)) )
					# Others wxWidgets graphical elements with not saved configurations.
					#elif isinstance(wxElement_handle, wx._core.):
					#elif isinstance(wxElement_handle, wx._core.):configHandle
					#elif isinstance(wxElement_handle, wx._core.StaticBitmap):
					#elif isinstance(wxElement_handle, wx._core.Panel):
					#elif isinstance(wxElement_handle, wx._core.Button):
					#elif isinstance(wxElement_handle, wx._core.StaticText):
				except KeyError:
					continue
				
			del configHandle # Close the file / Windows registry sock.
		except:
			print('Configurations not recovered.')

	#----------------------------------------------------------------------
	def save_properties(self):
		''' Save the current proprieties of the graphical elements '''
		try:
			configHandle = wx.Config(CONFIG_FILE)
			
			# Sweep all elements in `self()` to find the grafical ones
			# instance of the wxPython and salve the specific configuration.
			for wxElement_name, wxElement_handle in self.__dict__.items():
				try:
					# Each wxPython object have a specific parameter value
					# to be saved and restored in the software initialization.
					if isinstance(wxElement_handle, wx._core.TextCtrl):
						configHandle.Write(wxElement_name, wxElement_handle.GetValue() )
					elif isinstance(wxElement_handle, wx._core.CheckBox):
						configHandle.Write(wxElement_name, ('True' if wxElement_handle.GetValue() else 'False') )
					elif isinstance(wxElement_handle, wx._core.CheckListBox):
						value = [wxElement_handle.GetString(idx) for idx in wxElement_handle.GetCheckedItems()]
						configHandle.Write(wxElement_name, ','.join(value) )
					elif isinstance(wxElement_handle, wx._core.SpinCtrl):
						configHandle.Write(wxElement_name, str(wxElement_handle.GetValue()) )
					elif isinstance(wxElement_handle, wx._core.ComboBox):
						value = [wxElement_handle.GetString(idx) for idx in range(wxElement_handle.GetCount())]
						configHandle.Write(wxElement_name, ','.join(value) )
					elif isinstance(wxElement_handle, wx._core.ListBox):
						configHandle.Write(wxElement_name, wxElement_handle.GetStringSelection() )
					elif isinstance(wxElement_handle, wx._core.Notebook):
						configHandle.Write(wxElement_name, str(wxElement_handle.GetSelection()) )
					# Others wxWidgets graphical elements with not saved configurations.
					#elif isinstance(wxElement_handle, wx._core.):configHandle
					#elif isinstance(wxElement_handle, wx._core.StaticBitmap):
					#elif isinstance(wxElement_handle, wx._core.Panel):
					#elif isinstance(wxElement_handle, wx._core.Button):
					#elif isinstance(wxElement_handle, wx._core.StaticText):
				except KeyError:
					continue
			
			del configHandle # Close the file / Windows registry sock.
		except:
			print('Configurations not salved.')





#######################################################################

def kicost_gui():
	''' Load the graphical interface '''
	app = wx.App(redirect=False)
	frame = MyForm(None)
	frame.Show()
	app.MainLoop()

def kicost_gui_run(fileName):
	''' Execute the `fileName`under KiCost loading the graphical interface '''
	app = wx.App(redirect=False)
	frame = MyForm(None)
#	frame.Show()
	frame.m_comboBox_files.SetValue('"' + '", "'.join(fileName) + '"')
	frame.updateEDAselection()
	frame.run()
#	app.MainLoop()
