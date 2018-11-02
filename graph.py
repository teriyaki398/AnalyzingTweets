import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random

with open("../Output/Statistics", "r") as f:
    statis = f.read().split("\n")[:-1]
statis = [i.split(" ") for i in statis]

# remove 0 ~ FILTER 
FILTER = 4

data = []
label = []
# sorted by the number of favorites
statis = sorted(statis, key=lambda x: int(x[1]))
for i in statis:
    if int(i[1]) <= FILTER:
        continue
    else:
        data.append(int(i[1]))
        label.append(i[0])
data = data[::-1]
label = label[::-1]

legends = ["%3d : @%s" % (data[i], label[i]) for i in range(len(label))]

plt.style.use("ggplot")
plt.rcParams.update({"font.size": 15})

size = (10,7)
temp = cm.Pastel1(np.arange(9))
col = []
for i in range(len(data)):
    col.append(temp[i % 9])

plt.figure(figsize=size, dpi=100)

plt.pie(data, colors=col, counterclock=False, startangle=90, autopct=lambda p:'{:.1f}%'.format(p) if p>=5 else '')

plt.subplots_adjust(left=0, right=0.7)
plt.legend(legends, fancybox=True, loc="center left", bbox_to_anchor=(0.9,0.5))
plt.axis("equal")
plt.savefig("../Output/figure.png", bbox_inches="tight", pad_inches=0.05)


