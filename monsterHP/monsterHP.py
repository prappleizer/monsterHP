import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.widgets import TextBox,Button
import pandas as pd
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None' 
#########################################
#
#               monsterHP
#
# a quick+easy live encounter HP tracker
#
#             by Imad Pasha
#
#             02 / 23 / 2020 
#########################################
#
# Example setup 
#
#zombie = Monster('zombie',HP=33,AC=14)
#panther = Monster('panther',37,15)
#acolyte = Monster('acolyte',31,11)
#hag = Monster('hag',65,19)
#
#monster_list =[zombie,panther,acolyte,hag]
#encounter = Encounter(monster_list)
#encounter.run_encounter()
#########################################

plt.close('all')
class Monster():
	'''
	class for instantiating a Monster Object, which contains some basic information
	about a monster (AC and HP, + a name) and which interfaces with an Encounter 
	to show a dynamic bar graph of your monsters' HP in battle.
	'''
	def __init__(self,monster_name,HP,AC):
		'''
		Initialize Monster 
		------------------
		Params: 
			monster_name (string): name to label the bar/textbox for each monster. Shorter is better...
			HP (int/float): value of the monster's initial HP 
			AC (int/float): value for the monster's AC (static, but displayed for ease of viewing)
		Returns:
			None 
		'''
		self.monster_name = monster_name 
		self.HP = HP
		self.init_HP = HP 
		self.AC = AC
	def update_barnum(self,barnum):
		'''
		Tells each monster which mpl bar it is. 
		-------------------
		Params:
		barnum (int): bar number in overall mpl figure corresponding to this monster.
		'''
		self.barnum = barnum

	def create_textbox(self,axes):
		'''
		Create textbox entry space and label for each monster, using input axes calculated from 
		the full monster list supplied to Encounter. 
		--------------------------
		Params:
			axes (array_like): list containing mpl axes argument, e.g., [0.1,0.1,0.8,0.8]
		Returns:
			None
		'''
		self.textboxaxes = plt.axes(axes) 
		self.textboxaxes.text(0.5, 1.2,self.monster_name, horizontalalignment='center',verticalalignment='center', transform=self.textboxaxes.transAxes)
		self.textbox = TextBox(self.textboxaxes,label='',initial='')
		self.textbox.on_submit(self.update_damage)

	def update_damage(self,damage):
		'''
		Method to update the bar on the plot for this monster's HP based on input damage. 
		Negative damage corresponds to gaining HP. 
		---------------------------
		Params: 
			damage (int/float): amount of damage to subtract from the current HP.
		Returns:
			None, but on_submit will run this on <enter> or clicking out of the textbox. Updates the bar width.
		'''
		try:
			sub_value = eval(damage)
		except:
			self.textbox.set_val('')
			return
		self.HP -= sub_value
		bars[self.barnum].set_width(self.HP)

		if self.HP < 0.2 * self.init_HP:
			bars[self.barnum].set_color('r')
		elif self.HP > 0.2 * self.init_HP:
			bars[self.barnum].set_color('C0')
		


		self.textbox.set_val('')

	
class Encounter():
	'''
	Class for accumulating Monster objects and plotting them with the ability to
	dynamically subtract/add HP to them and see their AC. 
	'''
	def __init__(self,monster_list):
		'''
		Initialization for encounter class. 
		-----------------------------
		Params:
			monster_list (list): list containing monster objects
		Returns:
			None 
		'''
		self.monster_list = monster_list
	
	def run_encounter(self,left=0.02,bottom=0.2,figsize=(11,6)):
		'''
		Spawns a mpl bar plot with horizontal bars showing the HP for monsters in encounter. 
		This plot dynamically changes based on values entered in text boxes for each monster. 
		-------------------------
		Params: 
			left (default 0.15): float value for left edge of main ax (in figure coords). Useful if 
							 monster name is long and falling off lefthand edge. Right hand edge 
							 will auto-update to leave a small buffer on RHS. 
			bottom (default 0.2): value for bottom edge of main ax. Similar to above. 
			figsize (defualt (11,6)): MPL figsize tuple, sets the total size of figure. 
		'''
		self.fig = plt.figure(figsize=figsize)
		N_monsters = len(self.monster_list)
		if N_monsters < 8:
			#can fit 5 across 
			self.ax = plt.axes([left,bottom,0.98-left,0.9-bottom]) # 0.2 works well for this case. 
			left_edges = np.linspace(0.02,0.98-0.08,N_monsters)
			print(left_edges)
			all_axes = [[i,0.01,0.08,0.075] for i in left_edges]
		else: 
			bottom=0.33
			self.ax = plt.axes([left,bottom,0.98-left,0.9-bottom]) # 0.4 works well for this case. 
			left_edges1 = np.linspace(0.02,0.98-0.08,8)
			all_axes1 = [[i,0.15,0.08,0.075] for i in left_edges1]
			left_edges2 = np.linspace(0.02,0.98-0.08,N_monsters-8)
			all_axes2 = [[i,0.01,0.08,0.075] for i in left_edges2]
			all_axes = all_axes1 + all_axes2
		global bars 
		monster_name_label = ['{} (AC {})'.format(i.monster_name,i.AC) for i in self.monster_list]
		monster_hp_label = [i.HP for i in self.monster_list]
		bars = self.ax.barh(monster_name_label,monster_hp_label,edgecolor='k')
		self.autolabel(bars,monster_name_label,monster_hp_label)
		self.ax.set_yticklabels([])
		plt.gca().invert_yaxis()
		self.ax.set_title('monsterHP: A quick & easy live HP tracker by Imad Pasha',fontsize=19)
		self.ax.set_xlabel('Remaining HP',fontsize=10)
		self.ax.set_facecolor('#d6d6d6')
		for i,monster in enumerate(self.monster_list):
			monster.update_barnum(i)
			monster.create_textbox(all_axes[i])
		plt.show()
	def autolabel(self,rects,m1,m2):
	    # attach some text labels
		for ii,rect in enumerate(rects):

			width =  rect.get_width()

			height = rect.get_height()

			yloc1=rect.get_y() + height /2.0
			yloc2=rect.get_y() + height /2.0
			if (width <= 2):
				# Shift the text to the right side of the right edge
				xloc1 = width + 1
				yloc2=yloc2+0.3
				# Black against white background
				clr = 'black'
				align = 'left'
			else:
				# Shift the text to the left side of the right edge
				xloc1 = 0.98*width
				# White on blue
				clr = 'white'
				align = 'right'
			yloc1=rect.get_y() + height /2.0

			#self.ax.text(xloc1,yloc1, '%s'% (m2[ii]),horizontalalignment=align,
            #                 verticalalignment='center',color=clr,weight='bold',
            #                clip_on=True)
			self.ax.text(0.08,yloc2, '%s'% (m1[ii]),horizontalalignment='left',
                             verticalalignment='center',color=clr,weight='bold',
                             clip_on=True,fontsize=16)



class Launcher():
	'''
	FrontEnd class which allows for the interactive entry of monsters into the system.
	'''
	def __init__(self):
		self.names = ['']
		self.HPs = ['']
		self.ACs = ['']
		self.filepaths = ['']
		self.monster_list = []
		self.nhits = 0
	def name_on_submit(self,text):
		try:
			self.names[-1] = text
		except:
			return
	
	def HP_on_submit(self,text):
		try:
			self.HPs[-1] = eval(text)
		except:
			return
	def AC_on_submit(self,text):
		try:
			self.ACs[-1] = eval(text)
		except:
			return

	def loadfile(self,text):
		try:
			self.filepaths.append(text)
		except:
			return

	def on_loadbutton(self,x):
		if hasattr(self,'message'):
			self.message.set_visible(False)
		try:
			self.loaded = np.genfromtxt(self.filepaths[-1],delimiter=',',dtype=None)
			self.message = self.ax.text(0.05,0.02,'Data file loaded successfully!',fontsize=10)
			self.load_box.set_val('')
			for i in self.loaded:
				m = Monster(i[0],i[1],i[2])
				self.monster_list.append(m)
		except IOError as IO_error:
			print(IO_error)
			self.message = self.ax.text(0.05,0.02,'Error loading file: {}',format(IO_error),fontsize=10,color='r')
			self.load_box.set_val('')
		except ValueError as value_err:
			self.message = self.ax.text(0.05,0.02,'Error loading file: issue with formatting',fontsize=10,color='r')
			print(value_err)
			self.load_box.set_val('')

	def on_button(self,x):
		m = Monster(self.names[-1],self.HPs[-1],self.ACs[-1])
		self.name.set_val('')
		self.HP.set_val('')
		self.AC.set_val('')
		self.monster_list.append(m)
		#self.ax.text(0.2,0.45-0.2*self.nhits,'{} | {} | {}'.format(m.monster_name,m.HP,m.AC),fontsize=15)
		self.ax.text(0.05,0.55-0.04*self.nhits,'{}.'.format(self.nhits+1))
		self.ax.text(0.3,0.55-0.04*self.nhits,'{}'.format(m.monster_name),transform=self.ax.transAxes,horizontalalignment='center')
		self.ax.text(0.562,0.55-0.04*self.nhits,'{}'.format(m.HP),transform=self.ax.transAxes,horizontalalignment='center')
		self.ax.text(0.69,0.55-0.04*self.nhits,'{}'.format(m.AC),transform=self.ax.transAxes,horizontalalignment='center')

		self.nhits+=1

	def on_go(self,x):
		plt.close('all')
		self.encounter = Encounter(self.monster_list)
		self.encounter.run_encounter()


	def launch(self,figsize=(5,7)):
		'''
		Use a GUI interface to enter monsters in to use in the HP tracker, or load from CSV???.  
		'''
		self.fig = plt.figure(figsize=figsize)
		self.ax = self.fig.add_axes([0,0,1,1])
		self.ax.set_axis_off()
		self.ax.text(0.5,0.85,'monsterHP',fontsize=32,transform=self.ax.transAxes,horizontalalignment='center')
		self.ax.text(0.5,0.8,'an easy dynamic HP tracker',fontsize=15,transform=self.ax.transAxes,horizontalalignment='center')
		self.ax.text(0.5,0.75,'by Imad Pasha',fontsize=10,transform=self.ax.transAxes,horizontalalignment='center')
		self.ax_name = self.fig.add_axes([0.05,0.6,0.45,0.08])
		self.ax.text(0.3,0.69,'Name',transform=self.ax.transAxes,horizontalalignment='center')
		self.name = TextBox(self.ax_name,'')
		self.name.on_submit(self.name_on_submit)
		self.HP_ax = self.fig.add_axes([0.52,0.6,0.1,0.08])
		self.HP = TextBox(self.HP_ax,'')
		self.HP.on_submit(self.HP_on_submit)
		self.ax.text(0.55,0.69,'HP',transform=self.ax.transAxes,horizontalalignment='left')
		self.AC_ax = self.fig.add_axes([0.64,0.6,0.1,0.08])
		self.AC = TextBox(self.AC_ax,'')
		self.AC.on_submit(self.AC_on_submit)
		self.ax.text(0.66,0.69,'AC',transform=self.ax.transAxes,horizontalalignment='left')

		self.ax_button = self.fig.add_axes([0.88,0.6,0.09,0.08])
		self.button = Button(self.ax_button,'+')
		self.button.on_clicked(self.on_button)
		
		self.ax_start_encounter = self.fig.add_axes([0.88-0.14,0.05,0.22,0.08])
		self.start_button = Button(self.ax_start_encounter,'Go!')
		self.start_button.on_clicked(self.on_go)

		self.ax_loadfile = self.fig.add_axes([0.05,0.05,0.55,0.08])
		self.load_box = TextBox(self.ax_loadfile,'')
		self.load_box.on_submit(self.loadfile)
		self.load_file_button_ax = self.fig.add_axes([0.62,0.05,0.08,0.08])
		self.load_file_button = Button(self.load_file_button_ax,'+')
		self.load_file_button.on_clicked(self.on_loadbutton)
		self.ax.text(0.05,0.14,'or, load a csv file...')
		#plt.show()


if __name__ == "__main__":
	l = Launcher()
	l.launch()
	



