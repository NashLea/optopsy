[![Downloads](https://pepy.tech/badge/optopsy)](https://pepy.tech/project/optopsy)
[![Build Status](https://travis-ci.org/michaelchu/optopsy.svg?branch=master)](https://travis-ci.org/michaelchu/optopsy)

# Optopsy

Optopsy is a nimble backtesting libary for option strategies, it is designed to abstract away the complexities of backtesting large option chain datasets and allows you to focus on what matters, your trading strategy.

The library makes no assumptions on your data and is designed to compose well into your data analysis work. It uses Pandas extensively under the hood and takes Pandas dataframe objects as input and outputs. For example, instead of trying to be a full featured backtester or provide visualizations on your results, it allows the developers to build on top of the backtested results. 

*This library is currently in development, please use at your own risk*

## Usage

### Use Your Data
* Use data from any source, just provide a Pandas dataframe with the required columns when calling optopsy functions.

### Advanced Backtest Parameters:

* Optopsy allows you to mix and match different 'filters' to create an option strategy. Results will be returned as Pandas dataframes so that complex strategies can be composed upon.

**Entry rules:**
* Days to expiration
* Entry Days (Staggered trades)
* Absolute Delta
* Percentage out-of-the-money
* Contract size

**Exit rules:**
* Days to expiration
* Hold days
* Profit/Stop loss percent
* Spread delta
* Spread price

### Option strategy support
* Single Calls/Puts
* Vertical Spreads
* Iron Condors
* (Coming Soon) Iron Butterfly
* (Coming Soon) Covered Stock
* (Coming Soon) Combos (Synthetics/Collars)
* (Coming Soon) Diagonal Spreads
* (Coming Soon) Calendar Spreads
* (Coming Soon) Custom Spreads
* (Coming Soon) Strangles
* (Coming Soon) Straddles

### Dependencies
You will need Python 3.6.x and Pandas 0.23.1 or newer. It is recommended to install [Miniconda3](https://conda.io/miniconda.html). See [requirements.txt](https://github.com/michaelchu/optopsy/blob/master/requirements.txt) for full details.

### Installation
```
pip install optopsy
```

### Usage
Optopsy is best used with Jupyter notebooks, however, it is also possible to incorporate it into your python scripts:

The following example uses [Level 2 Historical CSV Data Sample](http://www.deltaneutral.com/files/Sample_SPX_20151001_to_20151030.csv) from historicaloptiondata.com.

```python

import os
from datetime import datetime
import pandas as pd
import optopsy as op

#     Optopsy is a lightweight library, it does not make any
#     assumptions on the format of your data. Therefore, 
#     you are free to store your data however you like. 
#
#     To use your data with this library, 
#     convert your data into a pandas DataFrame with
#     the following list of standard column names:
#
#     Column Name        Status
#     ---------------------------
#     option_symbol      Optional
#     underlying_symbol  Required
#     quote_date         Required
#     expiration         Required
#     strike             Required
#     option_type        Required
#     bid                Required
#     ask                Required
#     underlying_price   Required
#     implied_vol        Optional
#     delta              Required
#     gamma              Required
#     theta              Required
#     vega               Required
#     rho                Optional

def run_strategy():

    # grab our data created externally
    curr_file = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(curr_file, "data", "SPX_2014_2018.pkl")
    data = pd.read_pickle(file)

    # define the entry and exit filters to use for this strategy, full list of
    # filters will be listed in the documentation (WIP).
    filters = {
        # set the start and end dates for the backtest,
        # the dates are inclusive, and are python datetime objects.
        "start_date": datetime(2018, 1, 1),
        "end_date": datetime(2018, 12, 31),
        # filter values can be int, float, or tuple types
        # tuples are of the following format: (min, ideal, max)
        "entry_dte": (5, 7, 9),
        "leg1_delta": 0.50,
        "leg2_delta": 0.30,
        "contract_size": 1,
        "expr_type": "SPXW"
    }

    # strategy functions will return an optopsy dataframe
    # containing all the simulated trades
    spreads = op.long_call_spread(data, filters)
    spreads.stats()

if __name__ == "__main__":
    run_strategy()
```

#### Sample Backtest Results:

Results:
```
{
    'Initial Balance': 10000,
    'Ending Balance': 8560.0,
    'Total Profit': -1440.0,
    'Total Win Count': 0,
    'Total Win Percent': 0.0,
    'Total Loss Count': 2,
    'Total Loss Percent': 1.0,
    'Total Trades': 2
}
```

Trades:
```
          entry_date  exit_date expiration underlying_symbol  dte  ratio  contracts option_type  strike  entry_delta  entry_stk_price  exit_stk_price  entry_opt_price  exit_opt_price  entry_price  exit_price    cost
trade_num
0         2018-01-24 2018-01-31 2018-01-31              SPXW    7      1          1           c    2840         0.48          2837.60         2823.89             15.0           -0.00       1500.0        -0.0  1500.0
0         2018-01-24 2018-01-31 2018-01-31              SPXW    7     -1          1           c    2860         0.28          2837.60         2823.89             -6.4            0.05       -640.0         5.0  -635.0
1         2018-02-21 2018-02-28 2018-02-28              SPXW    7      1          1           c    2705         0.48          2701.39         2713.78             20.7           -5.80       2070.0      -580.0  1490.0
1         2018-02-21 2018-02-28 2018-02-28              SPXW    7     -1          1           c    2730         0.30          2701.39         2713.78             -9.2            0.05       -920.0         5.0  -915.0
...

Total Profit: -1440.0
```

**Full Documentation Coming Soon!**
