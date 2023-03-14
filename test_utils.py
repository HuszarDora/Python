import utils as u
import matplotlib.pyplot as plt


def test_get_portfolio_return():
    df_iei = u.get_etf_returns('IEI', 'simple', 'Adj Close')
    df_voo = u.get_etf_returns('VOO', 'simple', 'Adj Close')
    l_df = [df_iei, df_voo]
    d_weights = {'IEI': 0.1, 'VOO': 0.9}
    df_pf = u.get_portfolio_return(d_weights)
    df_pf.plot()
    df_pf.hist()
    plt.show()
# test_get_portfolio_return()

def test_calc_historical_var():
    d_weights = {'IEI': 0.1, 'VOO': 0.9}
    l_conf_levels = [0.01, 0.05]
    print(u.calc_historical_var(d_weights, l_conf_levels))
test_calc_historical_var()