from carbon_converter import *

import pandas as pd

df = pd.read_feather("df.feather")
df = df[df["giregion"]=="McLaren Vale"]

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

df.to_csv("df.csv")