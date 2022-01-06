# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 20:23:48 2022

@author: jopwo
"""

import pickle
import numpy as np

import matplotlib.pyplot as plt

def read_from_file(filename):
    
    with open(filename, 'rb') as infile:
        data = pickle.load(infile)
        
    return data

def player_plot(data, player, ylim = True):
    plt.figure(dpi=600)
    ax = plt.axes()
    
    N = np.size(data,1)
    
    win_fractions = np.zeros(N)
    for i in range(N):
        win_fractions[i] = data[player,i,1]/data[player,i,0]
        
    ax.plot(win_fractions)
    ax.set_title("Player "+str(player))
    ax.set_ylabel("win fraction of plan")
    if ylim:
        ax.set_ylim([0,1])
    
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    
    data = read_from_file('strong_1_stat_01.pickle')
    
    player_plot(data,4, ylim = True)