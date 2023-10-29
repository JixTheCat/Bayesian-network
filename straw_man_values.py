"""This is a script to prepare values for the strawman model

We want these values to be based in some sense of reality so that the discussion can ensue in a reasonable course. That way people have the potential to agree with some of the values compared to just disagreeing completely with everything.

It is also important that we establish some sense of validity to our resesarch. That the values we can derive are based in reality and somewhat defensible, however the workshop acts to strengthen both our understanding of these values and our ability to model the reality of affects and outcomes in vineyards.
"""

####################
# Data preparation #
####################
# We being with similar data preparation to the the linear models data prep.

from carbon_converter import *

import pandas as pd
import numpy as np

df = pd.read_feather("df.feather")

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

df["area_harvested"] = df["area_harvested"]*10000

df_floats = df.select_dtypes(float)
df_o = df.select_dtypes("O")
df_int = df.select_dtypes(int)

for col in df_floats.columns:
    #We make an exception for gross margin as people can lose money
    if col == "gross_margin": 
        continue
    df_floats.loc[df_floats[col]<1, col] = np.nan 

######
# NOTE
#
# We have exceptional difference here.
# We take all variables as a ratio of area.
# This is because this is how viticulturalists refer 
# to their numbers almost always.
for col in df_floats.columns:
    # We don't want to divide area by itself.
    if col == "area_harvested": 
        continue
    df_floats[col] = df_floats[col].div(df_floats["area_harvested"]).copy()

df_floats = (df_floats).apply(np.log)

df_floats = df_floats - df_floats.mean()
df_floats = df_floats/df_floats.std()

df_floats = df_floats.replace({np.inf: np.nan, -np.inf: np.nan})

df = pd.concat([df_floats, df_o, df_int], axis=1)

################################################
################################################

# We find the proportions below the mean!

# I looked at doing this via a function but it was
# rather cumbersome. It is incredibly inefficient to do it
# as singular pandas operations but at least a bit more
# verbose as to what is going on and easier to check.

def pr_root_node(df, node):
    # We set nans to -10 to show that they are less than 0.
    df = df.replace({np.nan: -10})
    high = len(df[
    (df[node]>0)
    ].index)/len(df)
    return {
        "high": high
    , "low": 1-high
    }


def pr_child_node(df: pd.DataFrame, node: str, parent: str):
    ok = df[df[node].notnull()] 
    length = len(ok[ok[parent].notnull()])
    return {
        "high": 
        len(ok[
        (
            (ok[node]>0) # H
        ) & 
        (
            (ok[parent].notnull())
        )
        ])/length
        , "low": len(ok[
        (
            (ok[node]<0)
        ) & 
        (
            (ok[parent].notnull())
        )
        ])/length
    }

###############
# Cover Crops #
###############
# length = len(df)

# this is sanity checked there are no values of -10 in the dataframe

# we will reset this after cover crops as a nan here represents not utilising that type of cover crop!
cover_crops = [
    "bare_soil"
    , "permanent_cover_crop_native"
    , "permanent_cover_crop_non_native"
    , "permanent_cover_crop_volunteer_sward"
    , "annual_cover_crop"
]

for node in cover_crops:
    high, low = pr_root_node(df, node).values()
    print("{}:\n\t high: {}\n\t low: {}".format(node, high, low))

##############
# Water

# It is important to narrow the values down first so that you are dealing with proportions relavant to the slice of data you are working with and not the whole thing. We want sums to 100%.

# you have to set the length to the field you measure or the proportions are incorrect.
pr_child_node(df_slice, "water_used", "bare_soil")
# 0.40559440559440557 # H
# 0.5944055944055944 # L
pr_child_node(df_slice, "water_used", "permanent_cover_crop_native")
# 0.47535596933187296 # H
# 0.524644030668127 # L
pr_child_node(df, "water_used", "permanent_cover_crop_non_native")
# 0.3810650887573965 # H
# 0.6189349112426036 # L
pr_child_node(df, "water_used", "permanent_cover_crop_volunteer_sward")
# 0.42350332594235035 # H
# 0.5764966740576497 # L
pr_child_node(df, "water_used", "annual_cover_crop")
# 0.45770392749244715 # H
# 0.5422960725075529 # L

##############
# Fuel
df["fuel"] = df["petrol_vineyard"].replace({np.nan: 0}) + df["diesel_vineyard"].replace({np.nan: 0})

df_slice = df[
    (df["petrol_vineyard"].notnull()) |
    (df["diesel_vineyard"].notnull())
] 


print("fuel:")
for cover_crop in cover_crops:
    high, low = pr_child_node(df_slice, "fuel", cover_crop).values()
    print("{}:\n\t high: {}\n\t low: {}".format(cover_crop, high, low))

# fuel:
# bare_soil:
#          high: 0.5573997233748271
#          low: 0.4426002766251729
# permanent_cover_crop_native:
#          high: 0.5265536723163842
#          low: 0.47344632768361583
# permanent_cover_crop_non_native:
#          high: 0.56062424969988
#          low: 0.43937575030012005
# permanent_cover_crop_volunteer_sward:
#          high: 0.48218972628421447
#          low: 0.5178102737157855
# annual_cover_crop:
#          high: 0.5481425322213799
#          low: 0.4518574677786202

#####################
# We do electricity #
#####################

df_slice = df[
    (df["electricity_vineyard"].notnull()) |
    (df["total_irrigation_electricity"].notnull())
]

df_slice["electricity"] = \
    df_slice["electricity_vineyard"].replace({np.nan: 0}).copy() +\
    df_slice["total_irrigation_electricity"].replace({np.nan: 0}).copy()

pr_root_node(df_slice, "electricity")
# 0.35777126099706746 # L
# 0.6367226061204343 # H

##################
# operating cost #
##################

ok = df[df["total_operating_costs"].notnull()]

ok["petrol_vineyard"] = ok["petrol_vineyard"].replace({np.nan: 0})
ok["diesel_vineyard"] = ok["diesel_vineyard"].replace({np.nan: 0})
ok["water_used"] = ok["water_used"].replace({np.nan: 0})

ok["electricity"] = \
    ok["electricity_vineyard"].replace({np.nan: 0}).copy() +\
    ok["total_irrigation_electricity"].replace({np.nan: 0}).copy()

# we drop vineyards who used no water or electricity.
ok = ok.drop(ok[ok["water_used"]==0].index)
ok = ok.drop(ok[ok["electricity"]==0].index)

# the selection needs to be made first so we use a third dataframe!

op = ok[(((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])>0) # H
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])<0)  # L
    ) & 
    (
        ok["water_used"]>0 # H
        # ok["water_used"]<0 # L
    )& 
    (
        ok["electricity"]>0 # H
        # ok["water_used"]<0 # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# 0.6739130434782609 # H
# 0.32608695652173914 # L

op = ok[(
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])>0) # H
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])<0)  # L
    ) & 
    (
        ok["water_used"]>0 # H
        # ok["water_used"]<0 # L
    )& 
    (
        ok["electricity"]>0 # H
        # ok["water_used"]<0 # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# 0.5625 # H
# 0.4375 # L

op = ok[(
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])>0) # H
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])<0)  # L
    ) & 
    (
        ok["water_used"]>0 # H
        # ok["water_used"]<0 # L
    )& 
    (
        # ok["electricity"]>0 # H
        ok["electricity"]<0 # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# div 0.6739130434782609 # H
# div 0.32608695652173914 # L

op = ok[(
    (
        # ok["water_used"]>0 # H
        ok["water_used"]<0 # L
    ) & 
    (
        ok["electricity"]>0 # H
        # ok["electricity"]<0 # L
    ) & 
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])>0) # H
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])<0)  # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# div 0.7142857142857143 # H
# div 0.2857142857142857 # L


op = ok[(
    (
        # ok["water_used"]>0 # H
        ok["water_used"]<0 # L
    ) & 
    (
        ok["electricity"]>0 # H
        # ok["electricity"]<0 # L
    ) & 
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])>0) # H
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])<0)  # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# 0.6666666666666666 # H
# 0.33333333333333337 # L

op = ok[(
    (
        # ok["water_used"]>0 # H
        ok["water_used"]<0 # L
    ) & 
    (
        # ok["electricity"]>0 # H
        ok["electricity"]<0 # L
    ) & 
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])>0) # H
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])<0)  # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# 0.6310679611650486 # H
# 0.3689320388349514 # L


op = ok[(
    (
        # ok["water_used"]>0 # H
        ok["water_used"]<0 # L
    ) & 
    (
        # ok["electricity"]>0 # H
        ok["electricity"]<0 # L
    ) & 
        # ((ok["petrol_vineyard"] +
        # ok["diesel_vineyard"])>0) # H
        ((ok["petrol_vineyard"] +
        ok["diesel_vineyard"])<0)  # L
    )]

length = len(op)

len(op[
        op["total_operating_costs"]>0 # H
        # op["total_operating_costs"]<0 # L
])/length
# 0.48333333333333334 # H
# 0.5166666666666666 # L

##########
# Yield  #
##########

ok = df[
    (df["scope1"].notnull()) &
    (df["water_used"].notnull()) &
    (df["tonnes_grapes_harvested"].notnull())
]

op = ok[
    (
        ok["water_used"]>0 # H
        # ok["water_used"]<0 # L
    ) &
    (
        ok["scope1"]>0 # H
        # ok["scope1"]<0 # L
    )
]

length = len(op)

len(op[
    (
        op["tonnes_grapes_harvested"]>0 # H
        # op["tonnes_grapes_harvested"]<0 # L
    )
])/length
# 0.7067307692307693 # H
# 0.2932692307692308 # L

# Because this is the only combination present
# we use this distribution for all of the
# columns with high because it is a reasonable indicator.
# We then use the opposite for the column with both low.

#################
# Grape Revenue #
#################

ok = df[df["total_grape_revenue"].notnull()]
length = len(op)

op = ok[
    (ok["tonnes_grapes_harvested"]<0)
]
length = len(op)
len(op[
    (op["total_grape_revenue"]>0)
])/length
# 0.5190380761523046 # H
# 0.48096192384769537 # L

op = ok[
    (ok["tonnes_grapes_harvested"]>0)
]
length = len(op)
len(op[
    (op["total_grape_revenue"]>0)
])/length
# 0.830028328611898 # H
# 0.16997167138810199 # L
