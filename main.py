import kivy
import sys
import os
from kivy import Config

print("yo")
#os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
Config.set('graphics', 'multisamples', '0')

kivy.require('1.10.0')
print(sys.version)

from kivy.app import App
from kivy.uix.button import Label, Button 
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.base import runTouchApp

###############################
import matplotlib
#matplotlib._png = None

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from collections import OrderedDict

###############################


#matplotlib._png = None
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


from eliminate_redundancies3 import veg_aminos_dict2
from food_item_list import Foodlist


#######################
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg



class RootLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'

        self.foods = Foodlist.fl()
        #self.app = Dope()

        self.aminos_dictionary = veg_aminos_dict2

        self.dropdown = DropDown()

        n = 0
       	for index in range(   len(self.aminos_dictionary)        ):
       		#CREATION
            self.btn = Button(text= self.foods[n], size_hint_y=None, height=44)
            n += 1 
            #ABILITY TO SELECT
            self.btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            # ADD TO DROPDOWN
            self.dropdown.add_widget(self.btn)

        self.quantity = TextInput(multiline=False)

        self.mainbutton = Button(text='ingredient1', size_hint=(None, None))
        self.mainbutton.bind(on_release= self.dropdown.open)
        
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.mainbutton, 'text', x))

        ##########
        self.submit = Button(text="Submit", font_size=40)
        self.submit.bind(on_press=self.pressed) 

        ##########

        self.add_widget(self.mainbutton)
        self.add_widget(self.quantity)
        self.add_widget(self.submit) 
        ##########

        
    def pressed(self, instance):
        self.remove_widget(self.mainbutton)
        self.remove_widget(self.quantity)
        self.remove_widget(self.submit)
        
        labels = ['50 percent', '50 percent'] 
        
        # CUSTOMIZE IDEAL AMOUNT OF PROTEIN TO ACHIEVE
        protein_goal_in_grams = 60 # based on user imput            ################################################################################ MAKE DYNAMIC 
        miligrams_per_gram = [55, 106, 153, 185, 212,  237, 262, 280, 287]  # adjusted for chart  (each one adding on top)
        ideal_amount = [ el * protein_goal_in_grams    for el in miligrams_per_gram]  # This checked out, manually after addition 
        #print("ideal amount >>>>>>>>>>>>>>>", ideal_amount )
        
        
        # Enter in the type of food and the amount 
        #ingredient1 = mathtask(veg_aminos_dict2['Radishes, oriental, dried'],177) ################################################ DYNAMIC 
        #ingredient1 = self.mathtask(veg_aminos_dict2[food],int(quantity) )

        listofaminoacidcontent_general = veg_aminos_dict2[self.mainbutton.text]
        # listofaminoacidcontent_general = veg_aminos_dict2[food]   
        listofaminoacidcontent_specific = []
        for aminoacidcontent_general in listofaminoacidcontent_general:
            amino_acid_specific_mg = int(self.quantity.text) * aminoacidcontent_general * 10   # to get to miligrams 
            
            listofaminoacidcontent_specific.append(amino_acid_specific_mg) 

        #print("mathtask, listofaminoacidscontentfothisfoodANDTHEAMOUNT", listofaminoacidcontent_specific)

        amount_of_aminos_mg = listofaminoacidcontent_specific 

        #amount_of_aminos_mg = ingredient1

######################################################################################################################
######################################################################################################################
######################################################################################################################
        
        # adjust it to graph / 
        # user input + dictionary produces a list / 
    
        # I) we need to adjust these values to make it suitable for graph / 

        # initialize 
        amount_of_aminos_mg_adjusted_to_graph = []
        
        
        if amount_of_aminos_mg[0] <= ideal_amount[0]:
            amount_of_aminos_mg_adjusted_to_graph = [amount_of_aminos_mg[0]]
            amount_of_aminos_mg_adjusted_to_graph__overflow = [0]
        else    :
            amount_of_aminos_mg_adjusted_to_graph__overflow = [amount_of_aminos_mg[0] - ideal_amount[0]]
            amount_of_aminos_mg_adjusted_to_graph.append(ideal_amount[0]) 


        ####
        #### ! Wait- is the initializing necessary? i range(8) starts from 0 or 1? 
        #### 
        for i in range(8):
            if ideal_amount[i] + amount_of_aminos_mg[i+1] <= ideal_amount[i+1]:

                amount_of_aminos_mg_adjusted_to_graph.append( ideal_amount[i] + amount_of_aminos_mg[i+1]  )
                amount_of_aminos_mg_adjusted_to_graph__overflow.append(0)

            else:
               # numofmorecharts = ideal_amount[i+1] // (ideal_amount[i] + amount_of_aminos_mg[i+1])  # Later, uncomment to find meals past "lunch, dinner" 
        
                fakeamountindv =  amount_of_aminos_mg[i+1] - (ideal_amount[i+1] - ideal_amount[i]) 
                amount_of_aminos_mg_adjusted_to_graph.append(ideal_amount[i+1])
                amount_of_aminos_mg_adjusted_to_graph__overflow.append(  ideal_amount[i] + ((ideal_amount[i] + amount_of_aminos_mg[i + 1]) - ideal_amount[i+1]) )
        
        
        
        # II) Assigning values of graph / 

        #print(amount_of_aminos_mg, "<<<<<<<<<<<<<<<  amount <<<<<<<<<<<<<<<<<<<<< ")
        #print(a, "<<<<<<<<<<<<<<< aminos <<<<<<<<<<<<<<<<<<<<<<<<<<<")
        #print(ideal_amount, "<<<<<<<<<<<<< ideal amount <<<<<<<<<<<<<")
        leu, lys, phen, val, thre, iso, meth, hist, tryp = amount_of_aminos_mg_adjusted_to_graph
        #print(amount_of_aminos_mg_adjusted_to_graph, "<<<<<<<<<  amount adjustd <<<<<<<<<<<<<")
            
        
        leu2, lys2, phen2, val2, thre2, iso2, meth2, hist2, tryp2 = amount_of_aminos_mg_adjusted_to_graph__overflow
        #print(amount_of_aminos_mg_adjusted_to_graph__overflow, "<<<<<<<<<<<<<< amount adjusted2 <<<<<<<<<<<<<")
            
            
        leu_ideal, lys_ideal, phenideal, val_ideal, thre_ideal, iso_ideal, meth_ideal, hist_ideal, tryp_ideal  = ideal_amount
            
        leucinefull=  [leu,leu2]
        leucineideal = [leu_ideal,leu_ideal]
            
        lysinefull = [lys, lys2]
        lysine_ideal=  [lys_ideal, lys_ideal]
            
        phenylalaninfull = [phen, phen2]
        phenylalanin_ideal = [phenideal, phenideal] 
            
        valinefull = [val, val2]
        valine_ideal=  [val_ideal, val_ideal]
            
        threoninefull = [thre, thre2]
        threonine_ideal =  [thre_ideal, thre_ideal]
        
        isoleucinefull = [iso, iso2]

        isoleucine_ideal =  [iso_ideal, iso_ideal]
        
        methioninefull = [meth, meth2]
        methionin_ideal =  [meth_ideal, meth_ideal]
        
        histidinefull = [hist, hist2]
        histidine_ideal = [hist_ideal, hist_ideal]
        
        tryptophanefull = [tryp, tryp2]
        tryptophan_ideal =  [tryp_ideal, tryp_ideal]
        
        
        # III) making the graph graphic 
     
        self.width = 0.35       # the width of the bars: can also be len(x) sequence
        self.figsdsds, self.ax = plt.subplots()  # What is figsds? 
  
        #plt.bar(x_pos, height, color=(0.2, 0.4, 0.6, 0.6))\
            
            
        self.ax.bar(labels, tryptophan_ideal, self.width, label='tryptophan_ideal',  color=['red', 'red'], edgecolor = 'white')  
        self.ax.bar(labels, tryptophanefull, self.width, label='tryptophanefull',  color=['black', 'black'])  
        
        self.ax.bar(labels, histidine_ideal, self.width, label='histidine_ideal', color= ['red', 'red'], edgecolor = 'white' )
        self.ax.bar(labels, histidinefull, self.width, label='histidinefull', color= ['black', 'black'] )
        
        self.ax.bar(labels, methionin_ideal, self.width, label='methionin_ideal', color= ['red', 'red'], edgecolor = 'white')
        self.ax.bar(labels, methioninefull, self.width, label='methioninefull', color= ['black', 'black'] )
        
        self.ax.bar(labels, isoleucine_ideal, self.width, label='isoleucineempty', color= ['red', 'red'], edgecolor = 'white')
        self.ax.bar(labels, isoleucinefull, self.width, label='isoleucinefull', color= ['black', 'black'] )
        
        self.ax.bar(labels, threonine_ideal, self.width, label='threonineempty', color= ['red', 'red'], edgecolor = 'white')
        self.ax.bar(labels, threoninefull, self.width, label='threoninefull', color= ['black', 'black'] )
        
        self.ax.bar(labels, valine_ideal, self.width, label='valineempty', color= ['red', 'red'], edgecolor = 'white')
        self.ax.bar(labels, valinefull, self.width, label='valinefull', color= ['black', 'black'] )
        
        
        self.ax.bar(labels, phenylalanin_ideal, self.width, label='phenylalanineempty', color= ['red', 'red'], edgecolor = 'white')
        self.ax.bar(labels, phenylalaninfull, self.width, label='phenylalaninfull', color= ['black', 'black'] )
        
        self.ax.bar(labels, lysine_ideal, self.width, label='lysine', color= ['red', 'red'], edgecolor = 'white' )
        self.ax.bar(labels, lysinefull, self.width, label='lysinefull', color= ['black', 'black'] )
        
        self.ax.bar(labels, leucineideal, self.width, label='leucine', color= ['red', 'red'], edgecolor = 'white'  )
        self.ax.bar(labels, leucinefull, self.width, label='leucinefull', color= ['black', 'black']  )
            
        self.ax.set_ylabel('Amino Acids')
        self.ax.set_title('Amino Acids percentage of food')
        self.ax.legend()
        
        #plt.show() # 2/28: mooting this to try to do it kivy way 


        #self.box = BoxLayout()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf())) 
        #runTouchApp(self.box) 



class Dumbclass(App):
    def build(self):
        return RootLayout()


Dumbclass().run()