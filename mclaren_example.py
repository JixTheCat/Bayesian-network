import os
import torch
import torch.nn.functional as F
import pyro
import pyro.distributions as dist
import pyro.distributions.constraints as constraints

smoke_test = ('CI' in os.environ)
assert pyro.__version__.startswith('1.8.6')

def mclaren_vale():
    """This is an example model created using samplers."""
    # Each distribution is connected via an edge, which in this case is the linear relationship established prior through OLS.
    # These edges can be defined as any model.
    ha = pyro.sample("harvest area", dist.Normal(0, 1))
    wu = pyro.sample(
        "water used"
        , dist.Normal(
            ha*0.7708476 -
            8.846E-4
            , 0.6372)) # Note that the variance is the standard deviation in the residuals as we are linearly estimating the parameter. this is also equal to the RSE.
    so = pyro.sample(
        "scope one"
        , dist.Normal(
            ha*0.4688445 +
            wu*0.0187578 -
            7.394E-4
            , 0.8762))
    harvest = pyro.sample(
        "yield"
        , dist.Normal(
            ha* 0.7121393 +
            wu*0.0801902 +
            so*0.0657961 -
            9.848E-4
            , 0.5874) # Note that the variance is the standard deviation in the residuals as we are linearly estimating the parameter. this is also equal to the RSE.
            )
    return ha, wu, so, harvest

data = torch.ones(10)
graph = pyro.render_model(model, model_args=(data,))

graph.format = "png"
graph.render("file_name")

samples = {"yield": []
           , "area": []
           , "water use": []
           , "emissions": []}
for i in range(1000):
    ha, wu, so, harvest = model(i)
    samples["yield"].append(ha)
    samples["area"].append(wu)
    samples["water use"].append(so)
    samples["emissions"].append(harvest)
