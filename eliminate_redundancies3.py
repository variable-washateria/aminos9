

from foodandamount import veg_aminos_dict
import itertools
from collections import OrderedDict
import re


tpl_veg_aminos_dict = list(veg_aminos_dict.items())

'''
print("********************")
print(tpl_veg_aminos_dict[0][0])
print("********************")
print(tpl_veg_aminos_dict[:3])
print("********************")
print("********************")
print("********************")
'''
#just to initilalize it, will append to it later 
grouped_list = [ (tpl_veg_aminos_dict[0][0][:3] , tpl_veg_aminos_dict[0][1])   ]

counts = [0]
#print("wat", grouped_list[-1][0][:3])

list_of_aminos_lists = []
list_of_identical_aminos = []
count2 = 1000 # not important- filler
mg_per_gram = [55,51,47,32,27,25,25,18,7]
# must initialize reference

reference = [(0.267, 0.267),  (0.214, 0.214), ( 0.0,  0.0),( 0.145,  0.145), (0.134, 0.134), (0.143, 0.143), (0.0, 0.0),( 0.0,  0.0),( 0.0, 0.0)]
for key, value in tpl_veg_aminos_dict:

	# if we're hitting a new food item: /
	# we need a  i) we need a new reference ii) and to append (key,value) to grouped_list /
	if key[:3] != grouped_list[-1][0][:3]:

		# i) new reference /
		reference = []
		i = 0 
		for el in value:
			potential_protein = (el * 200) / mg_per_gram[i]  # for a 200 gram serving of this food, this is the highest amount of pretein this amino acid can complete
			two_gram_range = (          (potential_protein - 2), (potential_protein + 2) )
			two_gram_range_in_mg = (   (two_gram_range[0] * (el*200 ))   ,    (two_gram_range[1] * (el*200 ))            ) 
			range_in_mg_per_gram =  (  (two_gram_range_in_mg[0] / 200  )         ,    (two_gram_range_in_mg[1] / 200 )                  )
			reference.append(range_in_mg_per_gram) 
		i += 1

	# ii) appending (key, value)  to grouped_list / 	
		grouped_list.append((key, value)) 

	# if we're at the same food item: /
	# we need to check if the amino acid is similar /
	# 
	if key[:3] == grouped_list[-1][0][:3]:
		counts[-1] += 1		

		# i)  is the amino acid similar? 
		# A) we assume it is at first / B) but if just one amino acid is outside the range, the whole set is deemed "similar = False" / C) we then make a new reference for the remaining items of same food name
		# Note: by making a new reference and checking the remaining food items, this assumes that disimilar amino-acid foods of same name will be grouped together according to alphabet
		# this can run into errors // for example- take x, y, z / if y is new group, z is checking reference of y- it may be different but in reality may similar to x  
		similar = True 
		j = 0
		for el in value:

			if not(   el >= reference[j][0] and el <= reference[j][1] ): 
				similar = False
			j += 1    

		if similar == False:
			grouped_list.append((key,value))
			reference = []
			i = 0 
			for el in value:
				potential_protein = (el * 200) / mg_per_gram[i]  # for a 200 gram serving of this food, this is the highest amount of pretein this amino acid can complete
				two_gram_range = (          (potential_protein - 2), (potential_protein + 2) )
				two_gram_range_in_mg = (   (two_gram_range[0] *(el*200 ))   ,    (two_gram_range[1] * (el*200 ))            ) 
				range_in_mg_per_gram =  (  (two_gram_range_in_mg[0] / 200  )         ,    (two_gram_range_in_mg[1] / 200 )                  )
				reference.append(range_in_mg_per_gram) 


		if similar == True:
			# grouped_list.append((value)) # kinda a weird thing- why append silmiar values? and can't anyways- it breaks 
			count2 += 1


		similar = False 



#Now let's take out the extraneous white space (the "       " at the end of each food item. )  # We could have done this before but we didn't


grouped_list_modified = [ell for el in grouped_list for ell in el ]

lst2 = []
i = 0 
for el in range(   0, len(grouped_list_modified)  , 2)       :
	newword =  re.sub(r'\s{3,}',"",grouped_list_modified[i])
	lst2.append(newword)

	i += 2
#print("LIST 2", lst2)
lst3 = []
i = 1 
for el in range(   0, len(grouped_list_modified)  , 2)       :
	lst3.append(grouped_list_modified[i])
	i += 2


grouped_list  = list(zip(lst2,lst3))


# we have to put grouped_list back in dictionary form / 
# in future revision, eliminate a step/ 
# list > dict > list > dict is redundant 

veg_aminos_dict2 = OrderedDict() 
for key, value in grouped_list:
	veg_aminos_dict2[key] = value



tpl_veg_aminos_dict = list(veg_aminos_dict2.items())

i = 0 
#print(tpl_veg_aminos_dict[0])
fooditemlist = []
for key, value in tpl_veg_aminos_dict:
	fooditemlist.append(key)
	#if "frozen" in key:

	i += 1