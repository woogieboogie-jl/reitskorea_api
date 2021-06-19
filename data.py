from reitskorea_api.krx.data import (KrxDelistingReader)
from reitskorea_api.naver.data import (NaverDailyReader)
from reitskorea_api.investing.data import (InvestingDailyReader)
from reitskorea_api._utils import (_convert_letter_to_num, _validate_dates)

import pandas as pd
from datetime import datetime, timedelta

def DataReader(symbol, exchange=None, start=None, end=None):
    '''
    read price data from various exchanges or data source
    * symbol: code or ticker
    * start, end: date time string
    * exchange: 'KRX'(default), 'KRX-DELISTING', 'NYSE', 'NASDAQ', 'AMEX', 'SSE', 'SZSE', 'HKEX', 'TSE', 'HOSE'
    '''
    start, end = _validate_dates(start, end)

    # KRX and Naver Finance
    if (symbol[:5].isdigit() and exchange==None) or \
       (symbol[:5].isdigit() and exchange and exchange.upper() in ['KRX', '한국거래소']):
        return NaverDailyReader(symbol, start, end, exchange).read()

    # KRX-DELISTING
    if (symbol[:5].isdigit() and exchange and exchange.upper() in ['KRX-DELISTING']):
        return KrxDelistingReader(symbol, start, end, exchange).read()

    # Investing
    reader = InvestingDailyReader
    df = reader(symbol, start, end, exchange).read()
    end = min([pd.to_datetime(end), datetime.today()])
    while len(df) and df.index[-1] < end: # issues/30
        more = reader(symbol, df.index[-1] + timedelta(1), end, exchange).read()
        if len(more) == 0:
            break
        df = df.append(more)
    return df   

