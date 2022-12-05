#%%
import os
import pandas as pd
import numpy as np
import seaborn as sns

# load packages
import matplotlib as mpl
import matplotlib.pyplot as plt

# set global parameters
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"

# read package path
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

db_file = os.path.join(BASE_DIR, r".\msdb.db")


def create_cur(db_file):
    """
    def create_cur
    CREATE CONNECTION AND CURSOR FOR THE DATABASE
    
    INPUTS------------------------------------------------------------------------
    db_file         <str> path to the sqlite3 database that will be queried

    RETURNS-----------------------------------------------------------------------
    cur             <sqlite obj> cursor object
    ------------------------------------------------------------------------------
    EXAMPLE:
    
    """
    import sqlite3

    # Connect to database
    conn = sqlite3.connect(db_file)
    conn.row_factory = lambda cursor, row: row[0]

    # Create cursor
    cur = conn.cursor()

    return cur


def get_data(db_file, param_list):
    # Custom query for two bodies
    cur = create_cur(db_file)

    output = pd.DataFrame()

    command = "SELECT * FROM metaBody WHERE sName = 'humerus' OR sName = 'forearm'"

    cur.execute(command)
    output["body"] = cur.fetchall()

    for param in param_list:

        command = (
            "SELECT "
            + param
            + " FROM metaBody WHERE sName = 'humerus' OR sName = 'forearm'"
        )

        cur.execute(command)
        data = cur.fetchall()
        output[param] = data

    return output


#%% All params
param_list = ["nMass", "nCOMx", "nCOMy", "nCOMz", "nIxx", "nIyy", "nIzz"]
output = get_data(db_file, param_list)
df = pd.DataFrame(
    data=output,
    columns=["body", "nMass", "nCOMx", "nCOMy", "nCOMz", "nIxx", "nIyy", "nIzz"],
)
corr = df.corr()
print(corr ** 2)

mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))
f.tight_layout()


# cmap = sns.color_palette(palette="muted", desat=0.5, as_cmap=True)
# Generate a custom diverging colormap
cmap = sns.cubehelix_palette(start=2, rot=0, hue=0, as_cmap=True)
# saturation = 0.4
# cmap = sns.diverging_palette(230, 20, as_cmap=True)

ax1 = plt.subplot(1, 2, 1)
ax1.text(-0.1, 1.1, "A", transform=ax1.transAxes, size=20, weight="bold")

# Draw the heatmap with the mask and correct aspect ratio
h1 = sns.heatmap(
    corr ** 2,
    mask=mask,
    cmap=cmap,
    center=0,
    square=True,
    linewidths=1,
    cbar_kws={"shrink": 0.5},
    vmin=0,
    vmax=1,
    cbar=False,
)
yticks = ["mass", "com (x)", "com (y)", "com (z)", "Ixx", "Iyy", "Izz"]
h1.set_yticklabels(yticks)
h1.set_xticklabels(yticks)
plt.title("Covariance of Body Parameters")

#%% Muscles


def get_muscle_data(db_file, param_list):
    # Custom query for two bodies
    cur = create_cur(db_file)

    param_list = ["nMaxIso", "nOptLen", "nTendonSlackLen", "nPenAngle"]

    output = pd.DataFrame()

    command = "SELECT * FROM metaMuscle WHERE sName = 'BIClong' OR sName = 'TRIlat'"

    cur.execute(command)
    output["muscle"] = cur.fetchall()

    for param in param_list:

        command = (
            "SELECT "
            + param
            + " FROM metaMuscle WHERE sName = 'BIClong' OR sName = 'TRIlat'"
        )

        cur.execute(command)
        data = cur.fetchall()
        output[param] = data

    return output


param_list = ["nMaxIso", "nOptLen", "nTendonSlackLen", "nPenAngle"]
output = get_muscle_data(db_file, param_list)
df = pd.DataFrame(
    data=output,
    columns=["muscle", "nMaxIso", "nOptLen", "nTendonSlackLen", "nPenAngle"],
)

corr = df.corr()
print(corr ** 2)

mask = np.triu(np.ones_like(corr, dtype=bool))

# Generate a custom diverging colormap
# cmap = sns.diverging_palette(230, 20, as_cmap=True)
# cmap = sns.color_palette("icefire", as_cmap=True)
# cmap = sns.color_palette("vlag", as_cmap=True)

ax2 = plt.subplot(1, 2, 2)
ax2.text(-0.1, 1.1, "B", transform=ax2.transAxes, size=20, weight="bold")

# Draw the heatmap with the mask and correct aspect ratio
h2 = sns.heatmap(
    corr ** 2,
    mask=mask,
    cmap=cmap,
    center=0,
    square=True,
    linewidths=0.5,
    cbar_kws={"shrink": 0.5},
    vmin=0,
    vmax=1,
)
yticks = ["max iso. force", "opt. length", "tendon slack length", "pen. angle"]
h2.set_yticklabels(yticks)
h2.set_xticklabels(yticks)

plt.title("Covariance of Muscle Parameters")


plt.show()

