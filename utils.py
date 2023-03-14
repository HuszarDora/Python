import pandas as pd
import numpy as np
import os


def read_etf_file(etf):
    filename = os.path.join('input', etf + '.csv')
    df = pd.read_csv(filename, index_col=0)
    df.index = pd.to_datetime(df.index)
    return df


def get_etf_returns(etf_name,
    return_type='log', fieldname='Adj Close'):

    df = read_etf_file(etf_name)
    df = df[[fieldname]]

    df['shifted'] = df.shift(1)
    if return_type == 'log':
        df['return'] = np.log(df[fieldname]/df['shifted'])
    if return_type == 'simple':
        df['return'] = df[fieldname]/df['shifted']-1

    # restrict df to result col
    df = df[['return']]
    # rename column
    df.columns = [etf_name]

    return df


def get_total_return(etf, return_type='log'):
    return get_etf_returns(etf, return_type, 'Adj Close')


def get_dividend_return(etf, return_type='log'):
    # 1 calc total simple return from Adj Close and Close
    df_ret_from_adj = get_etf_returns(etf, 'simple', 'Adj Close')
    df_ret_from_close = get_etf_returns(etf, 'simple', 'Close')
    # 2 simple div = ret Adj Close simple - ret Close simple
    df_div = df_ret_from_adj - df_ret_from_close
    # 3 convert to log if log
    if return_type=='log':
        df_div = np.log(df_div + 1)
    return df_div


def get_price_return(etf, return_type='log'):
    df_total = get_total_return(etf, 'simple')
    df_div = get_dividend_return(etf, 'simple')
    df_price = df_total - df_div
    if return_type == 'log':
        df_price = np.log(df_price + 1)
    return df_price



def get_portfolio_return(d_weights):
    l_df = []
    for etf, value in d_weights.items():
        df_temp = get_total_return(etf, return_type='simple')
        l_df.append(df_temp)
    # step1: join dataframe by index
    df_joined = pd.concat(l_df, axis=1)
    df_joined.sort_index(inplace=True)
    # step2: drop na
    df_joined.dropna(inplace=True)
    # multiply by weights
    # df_weighted = df_joined.mul(d_weights, axis=1)
    df_weighted_return = df_joined * pd.Series(d_weights)
    # sum cross multiplied results
    s_portfolio_return = df_weighted_return.sum(axis=1)

    return pd.DataFrame(s_portfolio_return, columns=['pf'])

# def test_get_portfolio_return():
#     df_iei = get_etf_returns('IEI', 'simple', 'Adj Close')
#     df_voo = get_etf_returns('VOO', 'simple', 'Adj Close')
#     l_df = [df_iei, df_voo]
#     d_weights = {'IEI': 0.6, 'VOO': 0.4}
#     df_pf = get_portfolio_return(l_df, d_weights)
#     df_pf.plot()
#     plt.show()

    # - join returns
    # - (drop na)
    # - (step2 multiply by weights)
    # - sum across etfs
    # - give back result
    # df_result = None
    # for etf, weight in d_pf.items():
    #     if df_result is None:
    #         df_result = weight * get_total_return(etf, 'simple')
    #     else:
    #         df_result =
    #     df_result = df_result.add(df_result, df_ret)
    # return df_result

def calc_historical_var(d_weights, l_conf_levels):
    df_pf = get_portfolio_return(d_weights)
    return df_pf.quantile(l_conf_levels)




    pass

