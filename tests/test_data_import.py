import os
import optopsy as op
import optopsy.checks as checks
import pandas as pd
import pytest


def test_missing_columns():
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    with pytest.raises(ValueError) as err:
        op.long_call(df, filters={"leg1_delta": 0.50})
        assert str(err.value) == "Required columns missing!"


def test_incorrect_datatypes():
    df = pd.DataFrame(
        [[1, "date", "123", 123, "call", 1, 1.2, "123", 1]],
        columns=[key for key in list(checks.required.keys())],
    )
    with pytest.raises(ValueError) as err:
        op.long_call(df, filters={"leg1_delta": 0.50})
        assert str(err.value) == "Incorrect datatypes detected!"
