import os
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# set global parameters
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"

sns.set_style("whitegrid")

cmap = "PuBuGn"
# read package path
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

data_file = os.path.join(BASE_DIR, r".\sim_results.csv")

data = pd.read_csv(data_file, sep=",")

sorted_data = data.sort_values("kin_error")

df = sorted_data[sorted_data < 999]

sc = plt.scatter(df["tri_error"], df["bi_error"], 10, c=df["kin_error"], cmap=cmap)
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
# ax.set_aspect("equal", adjustable="box")
plt.axis("square")
plt.xlabel("tricep error")
plt.ylabel("biicep error")
ax.set_ylim(0, 0.8)
ax.set_xlim(0, 0.8)

b = plt.colorbar(sc, label="kinematic error")
unity = np.linspace(0, 0.8, 10)
plt.plot(unity, unity, "k--")

plt.show()

print(data)

# calculate CV

mean_bic = np.mean(df["bi_error"])
std_bic = np.std(df["bi_error"])
cv_bic = std_bic / mean_bic
print("bicep cv:", cv_bic)

mean_tri = np.mean(df["tri_error"])
std_tri = np.std(df["tri_error"])
cv_tri = std_tri / mean_tri
print("tricep cv:", cv_tri)
