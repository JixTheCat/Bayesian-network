from carbon_converter import *

import numpy as np
import pandas as pd

df = pd.read_feather("df.feather")
df = df[df["giregion"]=="McLaren Vale"]
# df = df[df["giregion"]=="Barossa Valley"]
# df = df[df["data_year_id"]=="2021/2022"]

###################################
# We insert values for emissions
#
# We convert the use of fuels into CO2E
# This includes both scope1 and scope 2 in the totals, as well as separate columns for comparison.
df["irrigation_energy_diesel"] = df["irrigation_energy_diesel"].div(1000).apply(diesel_irrigation)
df["diesel_vineyard"] = df["diesel_vineyard"].div(1000).apply(diesel_vehicle)
df["petrol_vineyard"] = df["petrol_vineyard"].div(1000).apply(petrol_vehicle)
df["lpg_vineyard"] = df["lpg_vineyard"].div(1000).apply(lpg_vehicle)
df["biodiesel_vineyard"] = df["biodiesel_vineyard"].div(1000).apply(biodiesel_vehicle)

df["scope1"] = df["irrigation_energy_diesel"]\
    + df["diesel_vineyard"]\
    + df["petrol_vineyard"]\
    + df["lpg_vineyard"]\
    + df["biodiesel_vineyard"]

df = df[["area_harvested", "tonnes_grapes_harvested", "water_used", "scope1"]]

#################
# area_harvested:

#  count    1196.000000
# mean       28.203892
# std        98.008156
# min     -2639.000000
# 25%         6.150000
# 50%        13.000000
# 75%        27.630000
# max       603.000000
# Name: area_harvested, dtype: float64

#########################
# tonnes_grapes_harvested:

#  count    1196.000000
# mean      207.696812
# std       378.606458
# min         0.000000
# 25%        34.747500
# 50%        79.675000
# 75%       196.260000
# max      3600.000000
# Name: tonnes_grapes_harvested, dtype: float64

##############
# water_used:

#  count     1196.000000
# mean       115.856636
# std       1475.894398
# min          0.000000
# 25%          5.800000
# 50%         14.278500
# 75%         35.312500
# max      47086.000000
# Name: water_used, dtype: float64

#########
# scope1:

#  count      1196.000000
# mean      15645.899814
# std       35327.725501
# min           0.000000
# 25%        1154.825490
# 50%        4354.729749
# 75%       12018.837443
# max      335636.600238
# Name: scope1, dtype: float64

# log transform
df = (df+1).apply(np.log)

decs = {}
for col in df.columns:
    decs[col] = {"mean": df[col].mean(), "std": df[col].std()}

# Scale and centre
df = df - df.mean()
df = df/df.std()

for col in df.columns:
    print("\n\n")
    print("{} mean: {}".format(col, np.exp(decs[col]["mean"])))
    print("{} std: {}".format(col, np.exp(decs[col]["std"])))

df.to_csv("df.csv")