# from data import models
# from algo import pde
# %%
import numpy as np
import datetime
from opricer.data import models
from opricer.algo import pde
from opricer.tests.test_algo import AnalyticSolver
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from scipy.sparse import diags
from scipy.linalg import lu_solve, lu_factor


a = models.EurOption(datetime.datetime(2011, 1, 1), 'put')
b = models.Underlying(datetime.datetime(2010, 1, 1), 100)
c = models.AmeOption(datetime.datetime(2011, 1, 1), 'put')
d = models.BarOption(datetime.datetime(2011, 1, 1), 'put')
a._attach_asset(100, b)
c._attach_asset(100, b)
d._attach_asset([50, np.inf], 100, b)
solver = AnalyticSolver()
solver1 = pde.EurSolver()
solver2 = pde.AmeSolver()
solver3 = pde.BarSolver()
# print(solver3.get_price(d))
# print(solver3(c))
# print(c.__dict__)
fig = plt.figure(figsize=(15, 8))
ax = plt.axes()
price = solver(a)
ax.plot(solver.asset_samples, price, label='Analy')
ax.plot(solver.asset_samples, solver1(a), label='Sim')
ax.plot(solver.asset_samples, solver2(c), label='Ame')
ax.plot(solver.asset_samples, solver3(d), label='Bar')
ax.legend(loc='best')
cursor = Cursor(ax, useblit=True, linewidth=2)
plt.show()
plt.gcf()


# %%
# L = diags([solver3.L[50], 1], [-1, 0], shape=(48, 48)).A
# U = diags([solver3.H[50], solver3.C[1:-1, 50]], [0, 1], shape=(48, 48)).A

# # # L, H, C = solver3.L[50], solver3.H[50], solver3.C[1:-1, 50]
# # solver3._load_sim(c)
# # L1 = diags([solver3.L[50], 1], [-1, 0], shape=(48, 48)).A
# # U1 = diags([solver3.H[50], solver3.C[1:-1, 50]], [0, 1], shape=(48, 48)).A
# diag = diags([solver3.A[2:-1, 50], solver3.B[1:-1, 50], solver3.C[1:-2, 50]],
#              [-1, 0, 1], shape=(48, 48)).A

# %%
