import math

# load packages
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import string
import opensim as osim

# set global parameters
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["font.family"] = "Arial"


def set_model_posture(model, posture_list):

    inx_posture = 0
    for coord in model.getCoordinateSet():
        coord.set_default_value(posture_list[inx_posture])
        inx_posture += 1

    return model


def mobl_model():

    BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

    model_file = os.path.join(BASE_DIR, r".\model files\MOBL_ARMS_fixed_41.osim")

    model = osim.Model(model_file)

    elbow_dof = model.getCoordinateSet().get("elbow_flexion")
    print(elbow_dof.getName())

    triceps_length = []
    biceps_length = []

    triceps_tendon = []
    biceps_tendon = []

    triceps_ma = []
    biceps_ma = []

    for elbow_angle in range(0, 140, 10):

        posture_list = [0, 0, 0, elbow_angle * math.pi / 180]
        model = set_model_posture(model, posture_list)
        state = model.initSystem()

        model.equilibrateMuscles(state)

        triceps = model.getMuscles().get("TRIlat")
        triceps_length.append(triceps.getFiberLength(state))
        triceps_tendon.append(triceps.getTendonLength(state))
        triceps_ma.append(triceps.computeMomentArm(state, elbow_dof))

        biceps = model.getMuscles().get("BIClong")
        biceps_length.append(biceps.getFiberLength(state))
        biceps_tendon.append(biceps.getTendonLength(state))
        biceps_ma.append(biceps.computeMomentArm(state, elbow_dof))

    return (
        triceps_length,
        biceps_length,
        triceps_tendon,
        biceps_tendon,
        triceps_ma,
        biceps_ma,
    )


def ncan_model():

    BASE_DIR = os.path.join(os.path.dirname(__file__), "..")

    model_file = os.path.join(BASE_DIR, r".\model files\new_trial.osim")

    model = osim.Model(model_file)

    elbow_dof = model.getCoordinateSet().get("elbow_flexion")
    print(elbow_dof.getName())

    triceps_length = []
    biceps_length = []

    triceps_tendon = []
    biceps_tendon = []

    triceps_ma = []
    biceps_ma = []

    for elbow_angle in range(0, 140, 10):

        posture_list = [0, 0, 0, elbow_angle * math.pi / 180]
        model = set_model_posture(model, posture_list)
        state = model.initSystem()

        model.equilibrateMuscles(state)

        triceps = model.getMuscles().get("TriLat")
        triceps_length.append(triceps.getFiberLength(state))
        triceps_tendon.append(triceps.getTendonLength(state))
        triceps_ma.append(triceps.computeMomentArm(state, elbow_dof))

        biceps = model.getMuscles().get("BicLong")
        biceps_length.append(biceps.getFiberLength(state))
        biceps_tendon.append(biceps.getTendonLength(state))
        biceps_ma.append(biceps.computeMomentArm(state, elbow_dof))

    return (
        triceps_length,
        biceps_length,
        triceps_tendon,
        biceps_tendon,
        triceps_ma,
        biceps_ma,
    )


(
    triceps_length,
    biceps_length,
    triceps_tendon,
    biceps_tendon,
    triceps_ma,
    biceps_ma,
) = ncan_model()

(
    mobl_triceps_length,
    mobl_biceps_length,
    mobl_triceps_tendon,
    mobl_biceps_tendon,
    mobl_triceps_ma,
    mobl_biceps_ma,
) = ncan_model()

plt.figure(figsize=(8, 6), dpi=200)

#%% Muscle Lengths
ax1 = plt.subplot(1, 3, 1)
ax1.text(-0.1, 1.1, "A", transform=ax1.transAxes, size=20, weight="bold")
plt.plot(
    range(0, 140, 10),
    triceps_length,
    linestyle="solid",
    color="#ff1f5b",
    label="tricep",
)
plt.plot(
    range(0, 140, 10), biceps_length, linestyle="solid", color="#009ade", label="bicep",
)
plt.plot(
    range(0, 140, 10),
    mobl_triceps_length,
    linestyle=(0, (3, 5, 1, 5)),
    color="#000000",
    label="MOBL tricep",
)
plt.plot(
    range(0, 140, 10),
    mobl_biceps_length,
    linestyle=(0, (5, 10)),
    color="#000000",
    label="MOBL bicep",
)

ax = plt.gca()
ax.set_box_aspect(1)
ax.text(
    -0.1,
    1.1,
    string.ascii_uppercase[0],
    transform=ax.transAxes,
    size=20,
    weight="bold",
)
plt.title("Muscle Lengths")
plt.ylabel("length (m)")
plt.xlabel("elbow angle (deg)")
# plt.legend()

#%% Tendon Length

ax2 = plt.subplot(1, 3, 2)
ax2.text(-0.1, 1.1, "B", transform=ax2.transAxes, size=20, weight="bold")
plt.plot(
    range(0, 140, 10),
    triceps_tendon,
    linestyle="solid",
    color="#ff1f5b",
    label="tricep",
)
plt.plot(
    range(0, 140, 10), biceps_tendon, linestyle="solid", color="#009ade", label="bicep",
)

plt.plot(
    range(0, 140, 10),
    mobl_triceps_tendon,
    linestyle=(0, (3, 5, 1, 5)),
    color="#000000",
    label="MOBL tricep",
)
plt.plot(
    range(0, 140, 10),
    mobl_biceps_tendon,
    linestyle=(0, (5, 10)),
    color="#000000",
    label="MOBL bicep",
)

ax = plt.gca()
ax.set_box_aspect(1)
ax.text(
    -0.1,
    1.1,
    string.ascii_uppercase[1],
    transform=ax.transAxes,
    size=20,
    weight="bold",
)
plt.title("Tendon Lengths")
plt.ylabel("length (m)")
plt.xlabel("elbow angle (deg)")
# plt.legend()


ax3 = plt.subplot(1, 3, 3)
ax3.text(-0.1, 1.1, "C", transform=ax3.transAxes, size=20, weight="bold")

plt.plot(
    range(0, 140, 10), triceps_ma, color="#ff1f5b", label="tricep",
)
plt.plot(
    range(0, 140, 10), biceps_ma, color="#009ade", label="bicep",
)

plt.plot(
    range(0, 140, 10),
    mobl_triceps_ma,
    linestyle=(0, (3, 5, 1, 5)),
    color="#000000",
    label="MOBL tricep",
)
plt.plot(
    range(0, 140, 10),
    mobl_biceps_ma,
    linestyle=(0, (5, 10)),
    color="#000000",
    label="MOBL bicep",
)

ax = plt.gca()
ax.set_box_aspect(1)
ax.text(
    -0.1,
    1.1,
    string.ascii_uppercase[2],
    transform=ax.transAxes,
    size=20,
    weight="bold",
)
plt.title("Muscle Moment Arms")
plt.ylabel("moment arm length (m)")
plt.xlabel("elbow angle (deg)")
plt.legend()

plt.tight_layout()
plt.show()

