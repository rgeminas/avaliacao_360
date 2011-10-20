# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
import matplotlib.patches as patches
from matplotlib.path import Path
from gp_utils.common.models import Member
from matplotlib.figure import Figure
from matplotlib.pyplot import figure, show, rc, grid


def export_bargraph(criteria, evaluee):
    #criteria is a QuerySet of criterion with attributes verbose_name, average, average_board, average_all
    #evaluee is a Member object
    fig=Figure()
    N = len(criteria)
    width = 0.10
    ind = np.arange(N)
    ind2 = np.arange(width, N)
    ind3 = np.arange(width*2, N)
    ax = fig.add_subplot(111)
    
    member = []
    board = []
    all = []
    names = []
    for criterion in criteria:
        member.append(criterion.average)
        board.append(criterion.average_board)
        all.append(criterion.average_all)
        names.append(criterion.verbose_name)
    
    rects1 = ax.bar(ind, member, width, color='r')
    rects2 = ax.bar(ind2, board, width, color='b')
    rects3 = ax.bar(ind3, all, width, color='y')
    
    print(evaluee.board)
    ax.legend( (rects1[0], rects2[0], rects3[0]), (unicode(evaluee), unicode(evaluee.board), 'Geral'))
    
    ax.set_ylim(top=7)
    ax.set_xticks(ind2+width)
    ax.set_xticklabels(names, fontdict=None, minor=False)
    
    return fig

def export_polargraph(criteria, evaluee):

    N = len(criteria)
    
    member = []
    board = []
    all = []
    names = []
    for criterion in criteria:
        member.append(criterion.average)
        board.append(criterion.average_board)
        all.append(criterion.average_all)
        names.append(criterion.verbose_name)    
    
    # force square figure and square axes looks better for polar, IMO
    width, height = matplotlib.rcParams['figure.figsize']
    size = max(width, height)
    # make a square figure
    fig = figure(figsize=(size, size))
    ax = fig.add_axes([0.2, 0.2, 0.6, 0.6], polar=True, axisbg='#d5de9c')
    
    vertices = [(2*i*np.pi/N, member[i]) for i in range(N)]
    vertices.append((0, member[0]))

    codes = [Path.LINETO for i in range(N)]
    codes[0]=Path.MOVETO
    codes.append(Path.CLOSEPOLY)

    thetalabels = [360*i/N for i in range(N)]
    path = Path(vertices, codes)
    patch = patches.PathPatch(path, facecolor='orange', lw=2)
    
    fontproperties = matplotlib.font_manager.FontProperties(size='small')
    #ax.set_theta_offset(2*np.pi/N)
    ax.set_thetagrids(thetalabels, labels=names, fontproperties=fontproperties)
    ax.set_rgrids([1, 2, 3, 4, 5], labels=[''])
    ax.add_patch(patch)
    ax.set_rmax(5.0)
    grid(True)
    
    return fig