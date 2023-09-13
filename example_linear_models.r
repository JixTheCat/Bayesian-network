
df <- read.csv("df.csv")

print(summary(lm(
    tonnes_grapes_harvested ~
    area_harvested + water_used + scope1
    , data = df)))

print(summary(lm(
    water_used ~
    area_harvested
    , data = df)))

print(summary(lm(
    scope1 ~
    area_harvested + water_used
    , data = df)))
