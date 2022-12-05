import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, resample
import seaborn as sns

# set global parameters
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"

sns.set_style("white")
palette = sns.color_palette("muted")
colors = [palette[0], palette[3]]
saturation = 0.4

# read package path
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")


def read_sto(filename):
    import numpy as np

    fid = open(filename, "r")
    txt = fid.read()
    txt_list = txt.split("\n")

    header_end_index = txt_list.index("endheader")

    data_str = txt_list[header_end_index + 2 : len(txt_list)]
    fieldnames_str = txt_list[header_end_index + 1]
    fieldnames = np.char.split(fieldnames_str, sep="\t")
    fieldnames = fieldnames.tolist()

    data = np.char.split(data_str, sep="\t")
    data = data.tolist()
    data = np.stack(np.array(data[0 : len(data) - 1], dtype=float))

    # data_out = np.array([v.replace(',', '') for v in data], dtype=np.float32)

    return data, fieldnames


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def smooth(y, box_pts):
    box = np.ones(box_pts) / box_pts
    y_smooth = np.convolve(y, box, mode="same")
    return y_smooth


results_dir = os.path.join(BASE_DIR, r".\data")

fig = plt.figure()
# gs = fig.add_gridspec(2, 2)

tri_all = []
bi_all = []
bool_kin = True

for subdir, dirs, files in os.walk(results_dir):

    for name in dirs:
        trial_dir = os.path.join(results_dir, name)

        try:

            # kinematic results
            kin_file = os.path.join(trial_dir, "_states.sto")
            kin_data, fieldnames = read_sto(kin_file)
            time = kin_data[:, 0]
            elbow_data = kin_data[:, 7]

            kin_resample = resample(elbow_data, 500)
            # ax1 = fig.add_subplot(gs[:, 0])

            ax1 = plt.subplot(3, 1, 1)
            # plt.plot(time, elbow_data, color="blue", alpha=0.1)

            if bool_kin:
                desired_kin_file = os.path.join(BASE_DIR, r".\sigmoidal_flexion.mot")
                desired_kin_data, _ = read_sto(desired_kin_file)
                time = desired_kin_data[:, 0]
                desired_kin = desired_kin_data[:, 1]
                resampled_desired = resample(desired_kin, 500)
                plt.plot(time, desired_kin, color="black", linewidth=2)
                plt.ylabel("elbow angle (rad)")
                plt.title("desired kinematics")
                bool_kin = False
                ax1.spines["right"].set_visible(False)
                ax1.spines["top"].set_visible(False)

            # simulation results
            sim_file = os.path.join(trial_dir, "_controls.sto")

            sim_data, fieldnames = read_sto(sim_file)

            time = sim_data[:, 0]
            # low pass filtering
            fs = len(sim_data[:, 1]) / 2
            cutoff = 50
            # tri_data = butter_lowpass_filter(sim_data[:, 1], cutoff, fs, order=5)
            # bi_data = butter_lowpass_filter(sim_data[:, 2], cutoff, fs, order=5)

            # not filtered
            tri_data = sim_data[:, 1]
            bi_data = sim_data[:, 2]

            # resampling
            tri_resample = resample(tri_data, 2000)
            bi_resample = resample(bi_data, 2000)

            tri_all.append(tri_resample)
            bi_all.append(bi_resample)

            # plotting
            # time = np.linspace(0, 2, 500)
            # ax3 = fig.add_subplot(gs[0, 1])
            ax2 = plt.subplot(3, 1, 2)
            plt.plot(
                time, tri_data, color="k", alpha=0.5, linewidth=0.08,
            )
            plt.ylim(0, 1)
            plt.title("tricep activity")
            plt.ylabel("activation (a.u.)")
            ax1.set_xticklabels([])
            # plt.xlabel("time (s)")

            # ax3 = fig.add_subplot(gs[1, 1])
            plt.subplot(3, 1, 3)
            plt.plot(
                time, bi_data, color="k", alpha=0.5, linewidth=0.08,
            )
            plt.ylim(0, 1)
            plt.title("bicep activity")
            plt.ylabel("activation (a.u.)")
            plt.xlabel("time (s)")
        except:
            pass

tri_std = np.std(tri_all, axis=0)
bi_std = np.std(bi_all)
time_norm = np.linspace(0, 2, 2000)

ax2 = plt.subplot(3, 1, 2)
ax2.fill_between(
    time_norm,
    np.mean(tri_all, axis=0) + tri_std,
    np.mean(tri_all, axis=0) - tri_std,
    alpha=0.2,
    linewidth=0,
    color=colors[1],
)
plt.plot(
    time_norm, np.mean(tri_all, axis=0), linewidth=2, color=colors[1],
)

ax3 = plt.subplot(3, 1, 3)
ax3.fill_between(
    time_norm,
    np.mean(bi_all, axis=0) + bi_std,
    np.mean(bi_all, axis=0) - bi_std,
    alpha=0.2,
    linewidth=0,
    color=colors[0],
)
plt.plot(
    time_norm, np.mean(bi_all, axis=0), linewidth=2, color=colors[0],
)

ax2.spines["right"].set_visible(False)
ax2.spines["top"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.spines["top"].set_visible(False)

# inset
axins = ax3.inset_axes([0.5, 0.5, 0.45, 0.45])

axins.fill_between(
    time_norm,
    np.mean(bi_all, axis=0) + bi_std,
    np.mean(bi_all, axis=0) - bi_std,
    alpha=0.2,
    linewidth=0,
    color=colors[0],
)
axins.plot(
    time_norm, np.mean(bi_all, axis=0), linewidth=2, color=colors[0],
)

x1, x2, y1, y2 = 0.5, 1.5, 0, 0.1
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
# axins.set_xticklabels([])
# axins.set_yticklabels([])

ax3.indicate_inset_zoom(axins, edgecolor="black")

ax1.text(-0.1, 1.1, "A", transform=ax1.transAxes, size=20, weight="bold")
ax2.text(-0.1, 1.1, "B", transform=ax2.transAxes, size=20, weight="bold")
ax3.text(-0.1, 1.1, "C", transform=ax3.transAxes, size=20, weight="bold")

plt.tight_layout()
plt.show()
