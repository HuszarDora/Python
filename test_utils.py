import utils as u
import matplotlib.pyplot as plt

def test_get_portfolio_return():
    df_iei = u.get_etf_returns('IEI', 'simple', 'Adj Close')
    df_voo = u.get_etf_returns('VOO', 'simple', 'Adj Close')
    l_df = [df_iei, df_voo]
    d_weights = {'IEI': 0.6, 'VOO': 0.4}
    df_pf = u.get_portfolio_return(l_df, d_weights)
    df_pf.plot()
    plt.show()
test_get_portfolio_return()

