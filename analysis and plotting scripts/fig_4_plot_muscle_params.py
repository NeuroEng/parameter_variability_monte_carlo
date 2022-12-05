#%%
import os
import pandas as pd
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


#%% Mass
param_list = ["nMaxIso"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["muscle", "nMaxIso"],)
df_long1 = pd.melt(df, "muscle", var_name="parameters", value_name="value")

#%% COM

param_list = ["nOptLen", "nTendonSlackLen"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["muscle", "nOptLen", "nTendonSlackLen"],)
df_long2 = pd.melt(df, "muscle", var_name="parameters", value_name="value")


#%% Pen Angle
param_list = ["nPenAngle"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["muscle", "nPenAngle"],)
df_long3 = pd.melt(df, "muscle", var_name="parameters", value_name="value")


#%% Plotting


def swarmbox(ax, data):
    sns.set_style("white")
    palette = sns.color_palette("muted")
    colors = [palette[0], palette[3]]
    linewidth = 1
    saturation = 0.4
    whis = 10
    p = sns.boxplot(
        x="parameters",
        hue="muscle",
        y="value",
        data=data,
        ax=ax,
        palette=colors,
        linewidth=linewidth,
        dodge=True,
        saturation=saturation,
        whis=whis,
    )

    sns.swarmplot(
        x="parameters",
        hue="muscle",
        y="value",
        data=data,
        ax=ax,
        color=[0, 0, 0],
        size=4,
        dodge=True,
        alpha=0.5,
        edgecolor="w",
    )

    return p


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
ax1.text(-0.1, 1.1, "A", transform=ax1.transAxes, size=20, weight="bold")
ax2.text(-0.1, 1.1, "B", transform=ax2.transAxes, size=20, weight="bold")
ax3.text(-0.1, 1.1, "C", transform=ax3.transAxes, size=20, weight="bold")

b1 = swarmbox(ax1, df_long1)
b1.legend_.remove()
b1.set_xticklabels(["max iso force"])
ax1.set_ylabel("force (N)")
ax1.set_xlabel("")
sns.despine()

b2 = swarmbox(ax2, df_long2)

b2.legend_.remove()
b2.set_xticklabels(["opt. length", "tendon slack length"])
ax2.set_ylabel("m")
ax2.set_xlabel("")
sns.despine()


b3 = swarmbox(ax3, df_long3)

handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles=handles[0:], labels=["bicep", "tricep"])
b3.set_xticklabels(["pen. angle"])
ax3.set_ylabel("m")
ax3.set_xlabel("")
sns.despine()

plt.tight_layout()
plt.show()
