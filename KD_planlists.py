# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 23:05:54 2022

@author: jopwo
"""

import pickle
from datetime import datetime

def get_datetimestring():
    
    now = datetime.now()
    
    year = datetime.strftime(now, '%Y')[2:]
    
    datetimestring = year+datetime.strftime(now, '%m%d_%H%M')
    
    return datetimestring

def gen_planlist(actions,factions, assumptions = None):
    
    planlist = gen_planlist_all(actions,factions)
    
    if assumptions == 'weak':
        planlist = trunc_planlist_weakly(planlist)
    if assumptions == 'strong_1':
        planlist = trunc_planlist_weakly(planlist)
        planlist = trunc_planlist_strong_1(planlist)
        
    return planlist

def gen_planlist_all(actions,factions):
    
    planlist_all = []
    for i,f in enumerate(factions):
        for j,a1 in enumerate(actions[:-1]):
            for k,a2 in enumerate(actions[j+1:]):
                
                # Remove degeneracy of phase 1
                if a1 == 1 or a1 == 3 or a2 == 2:
                    pass
                
                # Enforce phase 3 rule
                elif a1 in [5,6,7] and a2 in [5,6,7]:
                    pass
                else:
                    planlist_all.append([f, [a1,a2]])
                    
    return planlist_all

def trunc_planlist_weakly(planlist_in):
    '''
    Weak assumptions about combinations of actions and factions nobody would
    consider:
        No action of influence counter to one's faction
        No licht + donker action combination
        No targeting and protecting of same figure
    '''
    
    licht = [5,9,10,11]
    donker = [6,15,16,17]
    commander = [12,15]
    treasurer = [13,16]
    advisor = [14,17]
    
    planlist_out = []
    for p in planlist_in:
            # No influence counter to faction
        if p[0] == 0 and (p[1][0] in donker or p[1][1] in donker):
            pass
        elif p[0] == 1 and (p[1][0] in licht or p[1][1] in licht):
            pass
        
            # No pure licht + pure donker action combo
        elif (p[1][0] in licht and p[1][1] in donker) or (p[1][0] in donker and p[1][1] in licht):
            pass
        
            # no targeting and protecting of same figure
        elif p[1][0] in commander and p[1][1] in commander:
            pass
        elif p[1][0] in treasurer and p[1][1] in treasurer:
            pass
        elif p[1][0] in advisor and p[1][1] in advisor:
            pass
        
        else:
            planlist_out.append(p)
            
    return planlist_out

def trunc_planlist_strong_1(planlist_in):
    '''
    Strong assumptions about combinations of actions and factions nobody would
    consider:
        No gate forces counter to one's faction
        No pure licht or donker if in pas faction
    '''
    
    defense = [0,1]
    attack = [2,3]
    licht_donker = [9,10,11,15,16,17]
    
    planlist_out = []
    for p in planlist_in:
            # No gate forces counter to one's faction
        if p[0] == 0 and (p[1][0] in attack or p[1][1] in attack):
            pass
        elif p[0] == 1 and (p[1][0] in defense or p[1][1] in defense):
            pass
        
            # No pure licht or donker if in pas faction
        elif p[0] == 2 and (p[1][0] in licht_donker or p[1][1] in licht_donker):
            pass
        
        else:
            planlist_out.append(p)
            
    return planlist_out
    

def read_from_file(filename):
    
    with open(filename, 'rb') as infile:
        data = pickle.load(infile)
        
    return data

def write_to_file(data, filename = None):
    
    if filename is None:
        filename = get_datetimestring()+'.pickle'
    
    with open(filename, 'wb') as outfile:
        pickle.dump(data, outfile)

if __name__ == '__main__':
    
    actions = [0,1,
               2,3,
               4,
               5,6,7,
               8,
               9,10,11,
               12,13,14,
               15,16,17]
    
    factions = [0, 1, 2]
    
    planlist_weak = gen_planlist(actions,factions, assumptions = 'weak')
    
    write_to_file(planlist_weak, filename = 'planlist_weak.pickle')
    

                    

                    

                
    
                
    