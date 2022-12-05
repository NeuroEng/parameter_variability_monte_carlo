#%%
import os
import pandas as pd
import msdb
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

    param_list = ["nMass", "nCOMx", "nCOMy", "nCOMz", "nIxx", "nIyy", "nIzz"]

    output = pd.DataFrame()

    command = "SELECT * FROM metaBody WHERE sName = 'upper arm' OR sName = 'forearm'"

    cur.execute(command)
    output["body"] = cur.fetchall()

    for param in param_list:

        command = (
            "SELECT "
            + param
            + " FROM metaBody WHERE sName = 'upper arm' OR sName = 'forearm'"
        )

        cur.execute(command)
        data = cur.fetchall()
        output[param] = data

    return output


#%% Mass
param_list = ["nMass"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["body", "nMass"],)
df_long1 = pd.melt(df, "body", var_name="parameters", value_name="value")

#%% COM

param_list = ["nCOMx", "nCOMy", "nCOMz"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["body", "nCOMx", "nCOMy", "nCOMz"],)
df_long2 = pd.melt(df, "body", var_name="parameters", value_name="value")

#%% Inertia
param_list = ["nIxx", "nIyy", "nIzz"]
output = get_data(db_file, param_list)
df = pd.DataFrame(data=output, columns=["body", "nIxx", "nIyy", "nIzz"],)
df_long3 = pd.melt(df, "body", var_name="parameters", value_name="value")


#%% Plotting


def swarmbox(ax, data):
    sns.set_style("white")
    palette = sns.color_palette("muted")
    colors = [palette[1], palette[2]]
    hue_order = ["upper arm", "forearm"]
    linewidth = 1
    saturation = 0.4
    whis = 10
    p = sns.boxplot(
        x="parameters",
        hue="body",
        y="value",
        data=data,
        ax=ax,
        palette=colors,
        linewidth=linewidth,
        dodge=True,
        saturation=saturation,
        hue_order=hue_order,
        whis=whis,
    )

    sns.swarmplot(
        x="parameters",
        hue="body",
        y="value",
        data=data,
        ax=ax,
        color=[0, 0, 0],
        size=4,
        dodge=True,
        hue_order=hue_order,
        alpha=0.5,
        edgecolor="w",
    )

    return p


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
ax1.text(-0.1, 1.1, "A", transform=ax1.transAxes, size=20, weight="bold")
ax2.text(-0.1, 1.1, "B", transform=ax2.transAxes, size=20, weight="bold")
ax3.text(-0.1, 1.1, "C", transform=ax3.transAxes, size=20, weight="bold")

p = swarmbox(ax1, df_long1)

p.legend_.remove()
p.set_xticklabels(["mass"])
ax1.set_ylabel("kg")
ax1.set_xlabel("")
sns.despine()

p2 = swarmbox(ax2, df_long2)


handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles=handles[0:2], labels=labels[0:])
p2.set_xticklabels(["x", "y", "z"])
ax2.set_ylabel("m")
ax2.set_xlabel("center-of-mass")
sns.despine()

p3 = swarmbox(ax3, df_long3)

p3.legend_.remove()
p3.set_xticklabels(["xx", "yy", "zz"])
ax3.set_ylabel("m")
ax3.set_xlabel("inertia")
sns.despine()

plt.tight_layout()
plt.show()
