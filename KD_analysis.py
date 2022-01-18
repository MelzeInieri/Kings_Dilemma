# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 20:23:48 2022

@author: jopwo
"""

# import time
from datetime import datetime
import pickle
import numpy as np

import matplotlib.pyplot as plt

import KD_batchrunning as KDB

def get_datetimestring():
    
    now = datetime.now()
    
    year = datetime.strftime(now, '%Y')[2:]
    
    datetimestring = year+datetime.strftime(now, '%m%d_%H%M')
    
    return datetimestring

def read_from_file(filename):
    
    with open(filename, 'rb') as infile:
        data = pickle.load(infile)
        
    return data

def write_to_file(data, filename = None, overwrite = False):
    
    if filename is None:
        filename = get_datetimestring()+'.pickle'
    
    if overwrite:
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)
    else:
        with open(filename, 'xb') as outfile:
            pickle.dump(data, outfile)

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
    
def evolve_strategies(N, planfile, winfile_in, adjustment_fraction = 0.25, minimum_weight = 0.005, winfile_out = True, show_plot = True):
    '''
    A single iteration of playing N games with weighted plan choices.
    The input is a windata file of a previous run with the same planlist.
    The choice weights are based on the outcome of that run, based on the 
    adjustment_fraction (see adjust_weights in KD_batchrunning)
    The plot shown, if not deactivated, has the previous iteration on the left side
    and the new iteration on the right. 
    Top is relative choice occurrence / weights, bottom is relative winrate.
    The new windata are written to a file that, if file_out is a True instead of
    a string, is based on the old filename.
    '''
    
    windata_in = read_from_file(winfile_in)
    weights_adjusted = KDB.adjust_weights(windata_in[:,:,0], windata_in, adjustment_fraction, minimum_weight)
    
    planlist, players, windata_out, stratdata_out, game_last = KDB.get_new_batch(planfile, N, choice_weights = weights_adjusted)
    
    if show_plot:
        plot_strategy_evolution(windata_in, windata_out)
        
    return planlist, players, windata_in, windata_out, stratdata_out, game_last

def plot_strategy_evolution(windata_in, windata_out):
    '''
    The plot has the old batch on the left side
    and the new iteration on the right. 
    Top is relative choice occurrence / weights, bottom is relative winrate.
    '''
    
    P = np.size(windata_in,0) # index of player
    if P != np.size(windata_out,0):
        raise ValueError("data are not of the same amount of players")
    
    weights_in = windata_in[:,:,0].copy().astype(float)
    weights_out = windata_out[:,:,0].copy().astype(float)
    for p in range(P):
        weights_in[p,:] = weights_in[p,:]/np.max(weights_in[p,:])
        weights_out[p,:] = weights_out[p,:]/np.max(weights_out[p,:])
    
    winrate_in = windata_in[:,:,1]/windata_in[:,:,0]
    winrate_out = windata_out[:,:,1]/windata_out[:,:,0]
    
    fig = plt.figure(dpi = 600)
    ax_in_weights = fig.add_subplot(221)
    ax_in_winrate = fig.add_subplot(223)
    ax_out_weights = fig.add_subplot(222)
    ax_out_winrate = fig.add_subplot(224)
    
    ax_in_weights.set_title("Old run")
    ax_in_weights.set_ylabel("relative occurrence/weights")
    ax_in_winrate.set_ylabel("relative winrate")
    ax_in_winrate.set_xlabel("plan index")
    
    ax_out_weights.set_title("New run")

    ax_out_winrate.set_xlabel("plan index")
    
    ax_in_weights.set_ylim([0,1])
    ax_in_winrate.set_ylim([0,1])
    ax_out_weights.set_ylim([0,1])
    ax_out_winrate.set_ylim([0,1])
    
    ax_in_weights.plot(weights_in.T, linewidth = 0.5)
    ax_in_winrate.plot(winrate_in.T, linewidth = 0.5)
    ax_out_weights.plot(weights_out.T, linewidth = 0.5)
    ax_out_winrate.plot(winrate_out.T, linewidth = 0.5)
    
    plt.tight_layout()
    plt.show

if __name__ == '__main__':
    
    planlist, players, windata_in, windata_out, stratdata_out, game_last = evolve_strategies(100000, 
                                                                                             planfile = 'planlist_strong_1.pickle', 
                                                                                             winfile_in = 'strong_1_stat_01.pickle',
                                                                                             adjustment_fraction = 0.5,
                                                                                             show_plot = False)
    
    plot_strategy_evolution(windata_in,windata_out)