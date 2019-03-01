import datetime
import logging
import operator


required = {
    "underlying_symbol": "object",
    "quote_date": "datetime64[ns]",
    "expiration": "datetime64[ns]",
    "strike": "float64",
    "option_type": "object",
    "bid": "float64",
    "ask": "float64",
    "underlying_price": "float64",
    "delta": "float64",
}

required_filters = ["leg$_delta", "leg$_strike_pct"]

required_spread_filters = [
    "entry_spread_price",
    "entry_spread_delta",
    "entry_spread_yield",
]

param_dtypes = {
    "start_date": (datetime.date,),
    "end_date": (datetime.date,),
    "expr_type": (str, list),
    "contract_size": (int,),
    "entry_dte": (int, tuple),
    "entry_days": (int,),
    "leg1_delta": (int, float, tuple),
    "leg2_delta": (int, float, tuple),
    "leg3_delta": (int, float, tuple),
    "leg4_delta": (int, float, tuple),
    "leg1_strike_pct": (int, float, tuple),
    "leg2_strike_pct": (int, float, tuple),
    "leg3_strike_pct": (int, float, tuple),
    "leg4_strike_pct": (int, float, tuple),
    "entry_spread_price": (int, float, tuple),
    "entry_spread_delta": (int, float, tuple),
    "entry_spread_yield": (int, float, tuple),
    "exit_dte": (int,),
    "exit_hold_days": (int,),
    "exit_leg_1_delta": (int, float, tuple),
    "exit_leg_1_otm_pct": (int, float, tuple),
    "exit_profit_loss_pct": (int, float, tuple),
    "exit_spread_delta": (int, float, tuple),
    "exit_spread_price": (int, float, tuple),
    "exit_strike_diff_pct": (int, float, tuple),
}


def _values(params, param):
    return params[param][1] if isinstance(params[param], tuple) else params[param]


def _do_checks(data, params):
    if not all(col in list(required.keys()) for col in data.columns.values):
        raise ValueError("Required columns missing!")

    if data.dtypes.astype(str).to_dict() != required:
        raise ValueError("Incorrect datatypes detected!")

    if not all(
        [isinstance(param, type) for param in params.values() for type in param_dtypes]
    ):
        raise ValueError("Incorrect value type detected for a filter!")


def _do_required_filter_checks(deltas, strike_pct, params):
    if (set(deltas).issubset(params.keys())) == (
        set(strike_pct).issubset(params.keys())
    ):
        raise ValueError(
            "Must provide values for either leg_deltas or strike_pct parameters"
        )


def singles_checks(data, params):
    _do_checks(data, params)
    _do_required_filter_checks(["leg1_delta"], ["leg1_strike_pct"], params)


def _vertical_checks(params, op):
    deltas = ["leg1_delta", "leg2_delta"]
    strike_pct = ["leg1_strike_pct", "leg2_strike_pct"]
    _do_required_filter_checks(deltas, strike_pct, params)

    leg1_value = _values(params, "leg1_delta") or _values(params, "leg1_strike_pct")
    leg2_value = _values(params, "leg2_delta") or _values(params, "leg2_strike_pct")

    if op(leg1_value, leg2_value):
        raise ValueError("leg 1 strike price cannot be higher than leg 2 strike price")


def vertical_call_checks(data, params):
    _do_checks(data, params)
    _vertical_checks(params, operator.le)


def vertical_put_checks(data, params):
    _do_checks(data, params)
    _vertical_checks(params, operator.ge)


def _condor_checks(params):
    deltas = ["leg1_delta", "leg2_delta", "leg3_delta", "leg4_delta"]
    strike_pct = [
        "leg1_strike_pct",
        "leg2_strike_pct",
        "leg3_strike_pct",
        "leg4_strike_pct",
    ]
    _do_required_filter_checks(deltas, strike_pct, params)

    leg1_value = _values(params, "leg1_delta") or _values(params, "leg1_strike_pct")
    leg2_value = _values(params, "leg2_delta") or _values(params, "leg2_strike_pct")
    leg3_value = _values(params, "leg3_delta") or _values(params, "leg3_strike_pct")
    leg4_value = _values(params, "leg4_delta") or _values(params, "leg4_strike_pct")

    if leg1_value < leg2_value:
        raise ValueError("leg 1 strike price cannot be higher than leg 2 strike price")

    if leg2_value <= leg3_value:
        raise ValueError("leg 2 strike price cannot be higher than leg 3 strike price")

    if leg3_value > leg4_value:
        raise ValueError("leg 3 strike price cannot be higher than leg 4 strike price")


def iron_condor_checks(data, params):
    _do_checks(data, params)
    _condor_checks(params)


def iron_butterfly_checks(data, params):
    _do_checks(data, params)
    _condor_checks(params)
