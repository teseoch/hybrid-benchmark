import json
import matplotlib.pyplot as plt


with open("../combined.json", "r") as f:
    data = json.load(f)


pyramids = []
prisms = []
tets = []
num_bases = []
mat_sizes = []

err_l2 = []
err_lp = []

times = []

for entry in data:
    success = entry["solver_info"]["solver_info"] == "Success"

    if not success:
        print(f"FAILED: {entry['args']['geometry']['mesh']}")

    pyrs = entry["count_pyramid"]
    prsms = entry["count_prism"]
    tets_ = entry["count_simplex"]

    num_elems = pyrs + prsms + tets_

    pyramids.append(pyrs/num_elems)
    prisms.append(prsms/num_elems)
    tets.append(tets_/num_elems)

    mat_sizes.append(entry["mat_size"])
    num_bases.append(entry["num_bases"])

    err_l2.append(entry["err_l2"])
    err_lp.append(entry["err_lp"])

    times.append(entry["time_solving"])


plt.scatter(times, err_l2)
plt.xlabel("Time (s)")
plt.ylabel("L2 error")
plt.yscale("log")
plt.show()

plt.hist([prisms, pyramids, tets], bins=10)
plt.legend(["Prisms", "Pyramids", "Tets"])
plt.xlabel("Fraction of elements")
plt.show()

plt.hist(num_bases, bins=20)
plt.xlabel("Number of bases")
plt.show()