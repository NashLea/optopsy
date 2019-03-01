#     Optopsy - Python Backtesting library for options trading strategies
#     Copyright (C) 2018  Michael Chu

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
from .enums import OptionType
from .backtest import create_spread
from .checks import (
    singles_checks,
    vertical_call_checks,
    vertical_put_checks,
    iron_condor_checks,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _process_legs(data, legs, params, check_func):
    check_func(data, params)
    #TODO: Remove mode parameter
    return create_spread(data, legs, params, "market")


def long_call(data, **params):
    legs = [(OptionType.CALL, 1)]
    return _process_legs(data, legs, params, singles_checks)


def short_call(data, **params):
    legs = [(OptionType.CALL, -1)]
    return _process_legs(data, legs, params, singles_checks)


def long_put(data, **params):
    legs = [(OptionType.PUT, 1)]
    return _process_legs(data, legs, params, singles_checks)


def short_put(data, **params):
    legs = [(OptionType.PUT, -1)]
    return _process_legs(data, legs, params, singles_checks)


def long_call_spread(data, **params):
    legs = [(OptionType.CALL, 1), (OptionType.CALL, -1)]
    return _process_legs(data, legs, params, vertical_call_checks)


def short_call_spread(data, **params):
    legs = [(OptionType.CALL, -1), (OptionType.CALL, 1)]
    return _process_legs(data, legs, params, vertical_call_checks)


def long_put_spread(data, **params):
    legs = [(OptionType.PUT, -1), (OptionType.PUT, 1)]
    return _process_legs(data, legs, params, vertical_put_checks)


def short_put_spread(data, **params):
    legs = [(OptionType.PUT, 1), (OptionType.PUT, -1)]
    return _process_legs(data, legs, params, vertical_put_checks)


def _iron_condor(data, legs, **params):
    spread = _process_legs(data, legs, params, iron_condor_checks)

    if spread is None:
        return None
    else:
        return (
            spread.assign(
                d_strike=lambda r: spread.duplicated(subset="strike", keep=False)
            )
            .groupby(spread.index)
            .filter(lambda r: (r.d_strike == False).all())
            .drop(columns="d_strike")
        )


def long_iron_condor(data, **params):
    legs = [
        (OptionType.PUT, 1),
        (OptionType.PUT, -1),
        (OptionType.CALL, -1),
        (OptionType.CALL, 1),
    ]
    return _iron_condor(data, legs, **params)


def short_iron_condor(data, **params):
    legs = [
        (OptionType.PUT, -1),
        (OptionType.PUT, 1),
        (OptionType.CALL, 1),
        (OptionType.CALL, -1),
    ]
    return _iron_condor(data, legs, **params)
