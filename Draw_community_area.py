#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import matplotlib.cm as cm
import numpy as np


class CArea:
    def __init__(self, n, name="", gridloc=None):
        self.n = n
        self.name = name
        self.gridloc = gridloc

    def __cmp__(self, x):
        return cmp(self.n, x.n)


CAreaGrid = [CArea(9, "Edison Park", (6, 1)),
             CArea(2, "West Ridge", (8, 1)),
             CArea(1, "Rogers Park", (9, 1)),

             CArea(12, "Forest Glen", (6, 2)),
             CArea(13, "North Park", (7, 2)),
             CArea(4, "Lincoln Square", (8, 2)),
             CArea(77, "Edgewater", (9, 2)),

             CArea(76, "O'Hare", (3, 3)),
             CArea(10, "Norwood Park", (7, 3)),
             CArea(11, "Jefferson Park", (8, 3)),
             CArea(14, "Albany Park", (9, 3)),
             CArea(3, "Uptown", (10, 3)),

             CArea(17, "Dunning", (5, 4)),
             CArea(15, "Portage Park", (6, 4)),
             CArea(16, "Irving Park", (7, 4)),
             CArea(21, "Avondale", (8, 4)),
             CArea(5, "North Center", (9, 4)),
             CArea(6, "Lake View", (10, 4)),

             CArea(18, "Montclar", (6, 5)),
             CArea(19, "Belmont Cragin", (7, 5)),
             CArea(20, "Hermosa", (8, 5)),
             CArea(22, "Logan Square", (9, 5)),
             CArea(7, "Lincoln Park", (10, 5)),

             CArea(25, "Austin", (7, 6)),
             CArea(23, "Humboldt Park", (8, 6)),
             CArea(24, "West Town", (9, 6)),
             CArea(8, "Near North Side", (10, 6)),

             CArea(26, "West Garfield Park", (8, 7)),
             CArea(27, "East Garfield Park", (9, 7)),
             CArea(28, "Near West Side", (10, 7)),
             CArea(32, "Loop", (11, 7)),

             CArea(30, "South Lawndale", (8, 8)),
             CArea(29, "North Lawndale", (9, 8)),
             CArea(31, "Lower West Side", (10, 8)),
             CArea(33, "Near South Side", (11, 8)),

             CArea(57, "Archer Heights", (6, 9)),
             CArea(58, "Brighton Park", (7, 9)),
             CArea(59, "McKinley Park", (8, 9)),
             CArea(60, "Bridgeport", (9, 9)),
             CArea(34, "Armour Square", (10, 9)),
             CArea(35, "Douglas", (11, 9)),

             CArea(56, "Garfield Ridge", (5, 10)),
             CArea(63, "Gage Park", (6, 10)),
             CArea(62, "West Edison", (7, 10)),
             CArea(61, "New City", (8, 10)),
             CArea(37, "Fuller Park", (9, 10)),
             CArea(38, "Grand Boulevard", (10, 10)),
             CArea(36, "Oakland", (11, 10)),

             CArea(64, "Clearing", (6, 11)),
             CArea(65, "West Lawn", (7, 11)),
             CArea(66, "Chicago Lawn", (8, 11)),
             CArea(67, "West Englewood", (9, 11)),
             CArea(40, "Washington Park", (10, 11)),
             CArea(39, "Kenwood", (11, 11)),
             CArea(41, "Hyde Park", (12, 11)),

             CArea(68, "Englewood", (8, 12)),
             CArea(69, "Greater Grand Crossing", (9, 12)),
             CArea(45, "Avalon Park", (10, 12)),
             CArea(42, "Woodlawn", (11, 12)),
             CArea(43, "South Shore", (12, 12)),

             CArea(70, "Ashburn", (8, 13)),
             CArea(71, "Auburn Gresham", (9, 13)),
             CArea(44, "Chatham", (10, 13)),
             CArea(47, "Burnside", (11, 13)),
             CArea(48, "Calumet Heights", (12, 13)),
             CArea(46, "South Chicago", (13, 13)),

             CArea(72, "Beverly", (9, 14)),
             CArea(73, "Washington Heights", (10, 14)),
             CArea(49, "Roseland", (11, 14)),
             CArea(50, "Pullman", (12, 14)),
             CArea(51, "South Deering", (13, 14)),
             CArea(52, "East Side", (14, 14)),

             CArea(74, "Mount Greenwood", (10, 15)),
             CArea(75, "Morgan Park", (11, 15)),
             CArea(53, "West Pullman", (12, 15)),
             CArea(54, "Riverdale", (13, 15)),
             CArea(55, "Hegewisch", (14, 15)),

             ]

CAreaGrid.sort()


def name_to_abbrev(n):
    # simple abbreviator for capitalized names
    abrv = ""
    words = n.split()
    for word in words:
        if word in ['North', 'South', 'East', 'West', 'Near']:
            abrv += words[0][0]
        elif word == 'Mount':
            abrv += "Mt"
        elif word == 'Park':
            abrv += 'Pk'
        elif word == 'Side':
            abrv += "Sd"
        elif word == "O'Hare":
            abrv = "ORD"
        elif len(abrv) > 2:
            abrv += word[0]
        else:
            cons = [x for x in word.lower()[1:] if x not in "aeiou"]
            abrv += word[0][0] + cons[0]
    return abrv


def CAPatches(label="abbrev", data_labels=[], data_fmt="%s", font_size="small", scale=[]):
    """Returns a matplotlib collection of patches. Also makes labels by default."""

    patches = []

    if len(data_labels) > 0 and len(data_labels) != 77:
        raise ValueError, "Must have 77 labels"
    if not len(data_labels) > 0:
        data_labels = [None] * 77
    if not len(scale) > 0:
        scale = [1] * 77

    for carea, data_label, sc in zip(CAreaGrid, data_labels, scale):
        # Add a fancy box
        fancybox = mpatches.FancyBboxPatch(
            [carea.gridloc[0] - 0.5, carea.gridloc[1] - 0.75], 0.8 * sc, 0.8 * sc,
            boxstyle=mpatches.BoxStyle("Round", pad=0.05))
        # if data_label:
        #    plt.text(carea.gridloc[0], carea.gridloc[1] - .5, data_fmt % data_label, ha="center", size=font_size)
        if label == "abbrev":
            plt.text(carea.gridloc[0], carea.gridloc[1], name_to_abbrev(carea.name), ha="center", size=font_size)
        elif label == "number":
            plt.text(carea.gridloc[0], carea.gridloc[1], carea.n, ha="center", size="small")
        patches.append(fancybox)
    return PatchCollection(patches)


def draw_community_area(crime_pred, save_flag, filename,self):
    fig = plt.figure(0)
    fig.clf()
    ax = plt.axes()
    img = plt.imread("chicago map.jpg")
    ax.imshow(img, extent=[0, 23, 20, 0])
    plt.axis([3, 12, 20, 0])
    # Pick values for each CA
    values = crime_pred/max(crime_pred)
    crime_pred = np.int_(crime_pred)
    scales = np.ones(77)
    collection = CAPatches(label="abbrev",  data_labels=crime_pred, data_fmt="%0.2f", scale=scales)
    # Color the CAs using the prediction values
    collection.set_cmap(cm.Reds)
    collection.set_array(np.array(values))
    collection.set_alpha(1)

    ax.add_collection(collection)
    plt.axis('equal')
    plt.axis('off')
    fig.suptitle('Crime rates Heatmap in Chicago', fontsize=18, fontweight='bold')
    if self.crime_type == 'ALL':
        crime_type = self.crime_type + ' crimes'
    else:
        crime_type = self.crime_type
    period_str = str(self.period)
    ax.set_title('Training data: ' + self.start_month + '-' + self.end_month + ',  Crime type: ' + crime_type + ',  Period to predict: ' + period_str + ' Week')
    if save_flag == 1:
        fig.savefig(filename)
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    mng.window.title('Crime rates Heatmap')
    mng.window.wm_iconbitmap('Logo.ico')
    mng.window.resizable(0, 0)
    plt.show()
