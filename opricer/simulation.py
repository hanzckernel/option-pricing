# from data import models
# from algo import pde
# %%
import numpy as np
import datetime
from opricer.model import models
from opricer.algo import pde, analytics, mc
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from scipy.sparse import diags
from scipy.linalg import lu_solve, lu_factor
# from opricer.teststaff import simulate
import pandas as pd

np.random.seed(123)
a = models.Underlying(datetime.datetime(2010, 1, 1), 100)
a1 = models.Underlying(datetime.datetime(2010, 1, 1), 200)
b = models.EurOption(datetime.datetime(2011, 1, 1), 'call')
b1 = models.AmeOption(datetime.datetime(2011, 1, 1), 'call')
c = models.BasketOption(datetime.datetime(2011, 1, 1), 'call')
d = models.BarOption(datetime.datetime(2011, 1, 1), 'put')
b._attach_asset(100, a)
b1._attach_asset(100, a1)
c._attach_asset(100, a, a1)
# d._attach_asset([30, np.inf], 100, a)
solver = analytics.AnalyticSolver(high_val=2, low_val=0)
price = solver(b)
# solver1 = pde.EurSolver()
solver2 = pde.AmeSolver(high_val=2, low_val=0)
# AMeprice = solver2()
Msolver = mc.EurMCSolver(path_no=60000, asset_no=10,
                         time_no=100, high_val=2, low_val=0)
solver4 = pde.BarSolver(high_val=2, low_val=0, asset_no=solver.asset_no)
Msolver2 = mc.BarMCSolver(high_val=2, low_val=0, asset_no=solver.asset_no)
Msolver3 = mc.BasketMCSolver(high_val=2, low_val=0, asset_no=solver.asset_no)
ABSolver = mc.BasketAmeSolver(high_val=2, low_val=0, asset_no=solver.asset_no)
ASolver = mc.AmeMCSolver(high_val=2, low_val=0, asset_no=solver.asset_no)


def plot(options, solvers, Msolvers, with_cursor=False):
    fig = plt.figure(figsize=(15, 8))
    ax = plt.axes()
    price = solver(b)
    MCprice = Msolver(b)
    ax.plot(solver.asset_samples, price, label='AnalyticSol')
    # for opt, sol in zip(options, solvers):
    #     ax.plot(solver.asset_samples, sol(opt)[0], label=type(
    #         sol).__name__ + type(opt).__name__)
    for opt, sol in zip(options, Msolvers):
        ax.plot(solver.asset_samples, sol(opt), label=type(
            sol).__name__ + type(opt).__name__)
    ax.legend(loc='best')
    if with_cursor:
        cursor = Cursor(ax, useblit=True, linewidth=2)
    plt.show()
    plt.gcf()


# plot([b1, c], [], [ASolver, ABSolver])
# print(solver.asset_samples.flatten(), price[:, 0])

solver(b).plot()
plt.show()
plt.gcf()
