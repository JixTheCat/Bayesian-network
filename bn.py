import os 
from functools import partial
import torch
import numpy as np
import pandas as pd
import pyro
import pyro.distributions as dist
import seaborn as sns
import matplotlib.pyplot as plt

from torch import nn
from pyro.nn import PyroModule

assert issubclass(PyroModule[nn.Linear], nn.Linear)
assert issubclass(PyroModule[nn.Linear], PyroModule)

# The tutorial sure does some bad things.
# this is why you always define function first!
# 
# I feel like it is a massive weakness of python

from pyro.nn import PyroSample
from pyro.infer.autoguide import AutoDiagonalNormal

from pyro.infer import Predictive

def summary(samples):
    site_stats = {}
    for k, v in samples.items():
        site_stats[k] = {
            "mean": torch.mean(v, 0),
            "std": torch.std(v, 0),
            "5%": v.kthvalue(int(len(v) * 0.05), dim=0)[0],
            "95%": v.kthvalue(int(len(v) * 0.95), dim=0)[0],
        }
    return site_stats

class BayesianRegression(PyroModule):
    def __init__(self, in_features, out_features):
        super().__init__()
        self.linear = PyroModule[nn.Linear](in_features, out_features)
        self.linear.weight = PyroSample(dist.Normal(0., 1.).expand([out_features, in_features]).to_event(2))
        self.linear.bias = PyroSample(dist.Normal(0., 10.).expand([out_features]).to_event(1))

    def forward(self, x, y=None):
        sigma = pyro.sample("sigma", dist.Uniform(0., 10.))
        mean = self.linear(x).squeeze(-1)
        with pyro.plate("data", x.shape[0]):
            obs = pyro.sample("obs", dist.Normal(mean, sigma), obs=y)
        return mean

if __name__ == "__main__":
    # For CI testing
    smoke_test = ("CI" in os.environ)
    assert pyro.__version__.startswith("1.8.6")
    pyro.set_rng_seed(1)

    # set matplotlib settings
    # %matplotlib inline
    plt.style.use("default")

    df = pd.read_csv("df.csv") #, index_col=0)
    df.drop(1)
    df = df.drop(df.columns[0], axis=1)
    df = df.dropna()
    # area_harvested
    # scope1

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), sharey=True)
    sns.scatterplot(
        x=df["water_used"]
        ,y=df["tonnes_grapes_harvested"]
        ,ax=ax[0])
    ax[0].set(xlabel="Water",
            ylabel="Yield",
            title="My first baby model")
    sns.scatterplot(
        x=df["scope1"].apply(np.log)
        , y=df["tonnes_grapes_harvested"].apply(np.log)
        , ax=ax[1])
    ax[1].set(xlabel="Scope One Emissions",
            ylabel="Yield",
            title="My first baby")

    # Regression model
    linear_reg_model = PyroModule[nn.Linear](3, 1)

    # Define loss and optimize
    loss_fn = torch.nn.MSELoss(reduction='sum')
    optim = torch.optim.Adam(linear_reg_model.parameters(), lr=0.05)
    num_iterations = 1500 if not smoke_test else 2

    # Torch takes tensors as inputs.
    data = torch.tensor(df[["tonnes_grapes_harvested", "area_harvested", "water_used", "scope1"]].values,
                            dtype=torch.float)
    x_data  = data[:, 1:]
    y_data = data[:, 0]

    for j in range(num_iterations):
        y_pred = linear_reg_model(x_data).squeeze(-1)
        # calculate the mse loss
        loss = loss_fn(y_pred, y_data)
        # initialize gradients to zero
        optim.zero_grad()
        # backpropagate
        loss.backward()
        # take a gradient step
        optim.step()
        if (j + 1) % 50 == 0:
            print("[iteration %04d] loss: %.4f" % (j + 1, loss.item()))

    # Inspect learned parameters
    print("Learned parameters:")
    for name, param in linear_reg_model.named_parameters():
        print(name, param.data.numpy())


model = BayesianRegression(3, 1)
guide = AutoDiagonalNormal(model)

#  We use an evidence lower band
from pyro.infer import SVI, Trace_ELBO


adam = pyro.optim.Adam({"lr": 0.03})
svi = SVI(model, guide, adam, loss=Trace_ELBO())

pyro.clear_param_store()
for j in range(num_iterations):
    # calculate the loss and take a gradient step
    loss = svi.step(x_data, y_data)
    if j % 100 == 0:
        print("[iteration %04d] loss: %.4f" % (j + 1, loss / len(data)))

guide.requires_grad_(False)

for name, value in pyro.get_param_store().items():
    print(name, pyro.param(name))

guide.quantiles([0.25, 0.5, 0.75])

predictive = Predictive(model, guide=guide, num_samples=800,
                        return_sites=("linear.weight", "obs", "_RETURN"))
samples = predictive(x_data)
pred_summary = summary(samples)

mu = pred_summary["_RETURN"]
y = pred_summary["obs"]
predictions = pd.DataFrame({
    "area_harvested": x_data[:, 0],
    "water_used": x_data[:, 1],
    "scope1": x_data[:, 2],
    "mu_mean": mu["mean"],
    "mu_perc_5": mu["5%"],
    "mu_perc_95": mu["95%"],
    "y_mean": y["mean"],
    "y_perc_5": y["5%"],
    "y_perc_95": y["95%"],
    "yield": y_data,
})

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), sharey=True)
fig.suptitle("Regression line 90% CI", fontsize=16)
ax[0].plot(predictions["water_used"],
           predictions["mu_mean"])
ax[0].fill_between(predictions["water_used"],
                   predictions["mu_perc_5"],
                   predictions["mu_perc_95"],
                   alpha=0.5)
ax[0].plot(predictions["water_used"],
           predictions["yield"],
           "o")
ax[0].set(xlabel="water used",
          ylabel="yield",
          title="water vs yield")
idx = np.argsort(predictions["water_used"])
ax[1].plot(predictions["scope1"],
           predictions["mu_mean"])
ax[1].fill_between(predictions["scope1"],
                   predictions["mu_perc_5"],
                   predictions["mu_perc_95"],
                   alpha=0.5)
ax[1].plot(predictions["scope1"],
           predictions["yield"],
           "o")
ax[1].set(xlabel="scop1 emissions",
          ylabel="yield",
          title="emissions vs yield");

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12, 6), sharey=True)
fig.suptitle("Posterior predictive distribution with 90% CI", fontsize=16)
ax[0].plot(predictions["water_used"],
           predictions["y_mean"])
ax[0].fill_between(predictions["water_used"],
                   predictions["y_perc_5"],
                   predictions["y_perc_95"],
                   alpha=0.5)
ax[0].plot(predictions["water_used"],
           predictions["yield"],
           "o")
ax[0].set(xlabel="water_used",
          ylabel="yield",
          title="water and yield")
idx = np.argsort(predictions["water_used"])

ax[1].plot(predictions["scope1"],
           predictions["y_mean"])
ax[1].fill_between(predictions["scope1"],
                   predictions["y_perc_5"],
                   predictions["y_perc_95"],
                   alpha=0.5)
ax[1].plot(predictions["scope1"],
           predictions["yield"],
           "o")
ax[1].set(xlabel="scope1",
          ylabel="yield",
          title="yield vs scope1 emissions");

weight = samples["linear.weight"]
weight = weight.reshape(weight.shape[0], 3)
fig = plt.figure(figsize=(10, 6))
sns.distplot(weight, kde_kws={"label": "vineyards"},)
fig.suptitle("a figure");


plt.show()

#  we can use torch script to save our findings for easier precompiled models! This is done using c++ as well bonus.

# from pyro import poutine
# from pyro.poutine.util import prune_subsample_sites


# class Predict(torch.nn.Module):
#     def __init__(self, model, guide):
#         super().__init__()
#         self.model = model
#         self.guide = guide

#     def forward(self, *args, **kwargs):
#         samples = {}
#         guide_trace = poutine.trace(self.guide).get_trace(*args, **kwargs)
#         model_trace = poutine.trace(poutine.replay(self.model, guide_trace)).get_trace(*args, **kwargs)
#         for site in prune_subsample_sites(model_trace).stochastic_nodes:
#             samples[site] = model_trace.nodes[site]['value']
#         return tuple(v for _, v in sorted(samples.items()))

# predict_fn = Predict(model, guide)
# predict_module = torch.jit.trace_module(predict_fn, {"forward": (x_data,)}, check_trace=False)

# torch.jit.save(predict_module, '/tmp/reg_predict.pt')
# pred_loaded = torch.jit.load('/tmp/reg_predict.pt')
# pred_loaded(x_data)

# weight = []
# for _ in range(800):
#     # index = 1 corresponds to "linear.weight"
#     weight.append(pred_loaded(x_data)[1])
# weight = torch.stack(weight).detach()
# weight = weight.reshape(weight.shape[0], 3)
# gamma_within_africa = weight[:, 1] + weight[:, 2]
# gamma_outside_africa = weight[:, 1]
# fig = plt.figure(figsize=(10, 6))
# sns.distplot(gamma_within_africa, kde_kws={"label": "African nations"},)
# sns.distplot(gamma_outside_africa, kde_kws={"label": "Non-African nations"})
# fig.suptitle("Loaded TorchScript Module : log(GDP) vs. Terrain Ruggedness");

# # sprinkler.py
# import pylab as pl
# import pymc as mc
 
# G_obs = [1.]
# N = len(G_obs)
 
# R = mc.Bernoulli('R', .2, value=pl.ones(N))
 
# p_S = mc.Lambda('p_S', lambda R=R: pl.where(R, .01, .4),
#                 doc='Pr[S|R]')
# S = mc.Bernoulli('S', p_S, value=pl.ones(N))
 
# p_G = mc.Lambda('p_G', lambda S=S, R=R:
#                 pl.where(S, pl.where(R, .99, .9), pl.where(R, .8, 0.)),
#                 doc='Pr[G|S,R]')
# G = mc.Bernoulli('G', p_G, value=G_obs, observed=True)