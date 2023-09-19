df = pd.read_feather("df.csv")

# We do the ones relating to cover crops differently!

len(df[
    (df["bare_soil"]/df["area_harvested"]>.5)
    ].index)/length
# 0.05204399934329338

len(df[
    (df["permanent_cover_crop_native"]/df["area_harvested"]>.5)
    ].index)/length
# 0.11361024462321458

len(df[
    (df["permanent_cover_crop_non_native"]/df["area_harvested"]>.5)
    ].index)/length
# 0.220325069775078

len(df[
    (df["permanent_cover_crop_volunteer_sward"]/df["area_harvested"]>.5)
    ].index)/length
# 0.4014119192250862

len(df[
    (df["annual_cover_crop"]>.5)
    ].index)/length
# 0.23033984567394516

##############
# First Water

len(df[
    (df["water_used"].div(df["area_harvested"])<df["water_used"].div(df["area_harvested"]).median()) & 
    (df["bare_soil"]>0.5)
    ].index)/length
# 0.04876046626169759

len(df[
    (df["water_used"].div(df["area_harvested"])<df["water_used"].div(df["area_harvested"]).median()) & 
    (df["permanent_cover_crop_native"]>0)
    ].index)/length
# 0.07437202429814481

len(df[
    (df["water_used"].div(df["area_harvested"])<df["water_used"].div(df["area_harvested"]).median()) & 
    (df["permanent_cover_crop_non_native"]>0)
    ].index)/length
# 0.16368412411755048

len(df[
    (df["water_used"].div(df["area_harvested"])<df["water_used"].div(df["area_harvested"]).median()) & 
    (df["permanent_cover_crop_volunteer_sward"]>0)
    ].index)/length
# 0.24150385815137088

len(df[
    (df["water_used"].div(df["area_harvested"])<df["water_used"].div(df["area_harvested"]).median()) & 
    (df["annual_cover_crop"]>.5)
    ].index)/length
# 0.11344606796913478


##############
# Lastly Fuel

len(df[
    ((df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | 
    (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())) & 
    (df["bare_soil"]>0.5)
    ].index)/length
# 0.08586439008373009

len(df[
    ((df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | 
    (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())) & 
    (df["permanent_cover_crop_native"]>0)
    ].index)/length
# 0.11459530454769332

len(df[
    ((df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | 
    (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())) & 
    (df["permanent_cover_crop_non_native"]>0)
    ].index)/length
# 0.20341487440485964

len(df[
    ((df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | 
    (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())) & 
    (df["permanent_cover_crop_volunteer_sward"]>0)
    ].index)/length
# 0.3350845509768511

len(df[
    ((df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | 
    (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())) & 
    (df["annual_cover_crop"]>.5)
    ].index)/length
# 0.15908717780331638

#####################
# We do electricity #
#####################

ok = df[(df["electricity_vineyard"]>0)]
ok[ok["electricity_vineyard"].div(ok["area_harvested"])<ok["electricity_vineyard"].div(ok["area_harvested"]).median()]
# 0.5
# This is the expected value due to using the median - however it could be different if the ratio of size to electricity is off.

##################
# operating cost #
##################

ok = df[df["total_operating_costs"]!=0]
length = len(ok)
ok = ok[
    (
        (ok["petrol_vineyard"].div(ok["area_harvested"])>ok["petrol_vineyard"].div(ok["area_harvested"]).median()) | # H
        (ok["diesel_vineyard"].div(ok["area_harvested"])>ok["diesel_vineyard"].div(ok["area_harvested"]).median())   # H
    )
]

len(ok[
    (ok["water_used"].div(ok["area_harvested"])>ok["water_used"].div(ok["area_harvested"]).median()) & # H
    (ok["total_operating_costs"]<ok["total_operating_costs"].median())
])/length
# 0.16060961313012895

len(ok[
    (ok["water_used"].div(ok["area_harvested"])<ok["water_used"].div(ok["area_harvested"]).median()) & # L
    (ok["total_operating_costs"]<ok["total_operating_costs"].median())
])/len(ok)
# 0.26480263157894735


ok = ok[
    (
        (ok["petrol_vineyard"].div(ok["area_harvested"])<ok["petrol_vineyard"].div(ok["area_harvested"]).median()) | # L
        (ok["diesel_vineyard"].div(ok["area_harvested"])<ok["diesel_vineyard"].div(ok["area_harvested"]).median())   # L
    )
]

len(ok[
    (ok["water_used"].div(ok["area_harvested"])>ok["water_used"].div(ok["area_harvested"]).median()) & # H
    (ok["total_operating_costs"]<ok["total_operating_costs"].median())
])/length
# 0.13130128956623682

len(ok[
    (ok["water_used"].div(ok["area_harvested"])<ok["water_used"].div(ok["area_harvested"]).median()) & # L
    (ok["total_operating_costs"]<ok["total_operating_costs"].median())
])/len(ok)
# 0.2670807453416149

##########
# Yield  #
##########
length = len(df)
ok = df[
    (
        (df["petrol_vineyard"].div(df["area_harvested"])<df["petrol_vineyard"].div(df["area_harvested"]).median()) | # L
        (df["diesel_vineyard"].div(df["area_harvested"])<df["diesel_vineyard"].div(df["area_harvested"]).median())   # L
    )
]


len(ok[
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) &
    (ok["water_used"].div(ok["area_harvested"])<ok["water_used"].div(ok["area_harvested"]).median()) # L
])/length
# 0.23575767525857824

len(ok[
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) &
    (ok["water_used"].div(ok["area_harvested"])>ok["water_used"].div(ok["area_harvested"]).median()) # H
])/length
# 0.12165490067312427

ok = df[
    (
        (df["petrol_vineyard"].div(df["area_harvested"])>df["petrol_vineyard"].div(df["area_harvested"]).median()) | # H
        (df["diesel_vineyard"].div(df["area_harvested"])>df["diesel_vineyard"].div(df["area_harvested"]).median())   # H
    )
]

len(ok[
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) &
    (ok["water_used"].div(ok["area_harvested"])<ok["water_used"].div(ok["area_harvested"]).median()) # L
])/length
# 0.2424889180758496

len(ok[
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) &
    (ok["water_used"].div(ok["area_harvested"])>ok["water_used"].div(ok["area_harvested"]).median()) # H
])/length
# 0.11377442127729437

##########
# Profit #
##########

ok = df[df["total_grape_revenue"]!=0]
length = len(ok)

len(ok[
    (ok["total_grape_revenue"].div(ok["area_harvested"])<ok["total_grape_revenue"].div(ok["area_harvested"]).median()) & # L
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])>ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) # H
])/length
# 0.02199967164669184

len(ok[
    (ok["total_grape_revenue"].div(ok["area_harvested"])<ok["total_grape_revenue"].div(ok["area_harvested"]).median()) & # L
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) # L
])/length
# 0.02199967164669184


len(ok[
    (ok["total_grape_revenue"].div(ok["area_harvested"])>ok["total_grape_revenue"].div(ok["area_harvested"]).median()) & # H
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])<ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) # L
])/length


len(ok[
    (ok["total_grape_revenue"].div(ok["area_harvested"])>ok["total_grape_revenue"].div(ok["area_harvested"]).median()) & #H
    (ok["tonnes_grapes_harvested"].div(ok["area_harvested"])>ok["tonnes_grapes_harvested"].div(ok["area_harvested"]).median()) # H
])/length

def second_layer(df: pd.DataFrame, first_col: str, second_col: str):
    length = len(df.index)
    return len(df[
        (df[first_col]<df[first_col].median()) & 
        (df[second_col]<df[second_col].median())
        ].index)/length

