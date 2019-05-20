

# In[103]:

# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 21:15:00 2019

@author: hanzhicheng
"""
"""
some global parameters which later will be separated into another module
"""
"""
The timezone has not been handled!!! Assumed all within the same timezone
and so is the format
"""




import abc
import numpy as np
from datetime import datetime
def int_rate(t): return 0.5


class World(abc.ABC):
    pass


class Underlying(object):
    """
    We currently use prescribed drift and volatility for simplicity of the
    project. Implied volatility tools amongst others will be built at a
    later phase.

    We expect all time entries to be datetime form.
    """

    def __init__(self, spot_time, spot_price, dividend=0.0):
        self.time = spot_time
        self.price = spot_price
        self.drift = None  # get these later
        self.vol = lambda asset, t: 0.2
        self.div = dividend


class Option(object):

    def __init__(self, expiry_date, otype):
        self.otype = otype
        self.expiry = expiry_date

    def _attach_asset(self, strike_price, *underlyings):
        self.strike = strike_price
        self.int_rate = int_rate
        self.spot_price = []
        self.currency = []
        self._time = []
        self._vol = []  # TODO: This need to be modified when get data
        self._drift = []
        for underlying in underlyings:
            self.spot_price.append(underlying.price)
            self._time.append(underlying.time)
            self._vol.append(underlying.vol)
            self._drift.append(underlying.drift)
            self.div = underlying.div
        if len(self._time) == 1:
            self.time_to_maturity = (self.expiry - self._time[0]).days / 365
        else:
            raise ValueError('Undelyings have different spot times')

    def payoff(self, price):
        if self.otype == 'call':
            return np.clip(price - self.strike, 0, None).astype(float)
        elif self.otype == 'put':
            return np.clip(self.strike - price, 0, None).astype(float)
        else:
            raise ValueError('Incorrect option type')


class EurOption(Option):
    """
    we write this subclass just to make the structure clearer.
    AmeOption can be seen as EurOptio when dealing with pricing.
    """

    def __init__(self, otype, expiry_date):
        super().__init__(otype, expiry_date)


class AmeOption(Option):

    def __init__(self, otype, expiry_date):
        super().__init__(otype, expiry_date)


class BarOption(EurOption, AmeOption):  # Barrier options
    """
    Currently this class only consider call/put options with knock-out barriers.
    Further knock-in features will be built up in a later phase.
    """

    def __init__(self, otype, expiry, strike_price=10, barrier=[0, None], rebate=5):
        super().__init__(otype, expiry)
        self.rebate = rebate
        self.barrier = barrier

    @property
    def barrier(self):
        return self._barrier

    @barrier.setter
    def barrier(self, val):
        try:
            val = np.broadcast_to(np.asarray(val, dtype=float), (2,))
            self._barrier = np.where(
                [self.strike < val[0], self.strike > val[1]], [0, np.inf], val)
        except AttributeError:
            self._barrier = val
        except:
            raise ValueError("Wrong barrier input form")

    def _attach_asset(self, barrier, strike_price, *underlyings):
        super()._attach_asset(strike_price, *underlyings)
        self.barrier = barrier


# %%
