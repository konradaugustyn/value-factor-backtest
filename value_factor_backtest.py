import pandas as pd
import matplotlib.pyplot as plt
import math


def main():
    df = pd.read_csv("Portfolios_Formed_on_BE-ME.csv", skiprows=23, nrows=1202, index_col=0)
    df.index = pd.to_datetime(df.index.astype(str), format="%Y%m")
    r_ls = (df["Hi 10"] - df["Lo 10"]) / 100

    # period 2018-2020
    y1820 = r_ls.loc["2018-01":"2020-12"]
    dd_y1820 = drawdown(y1820)
    plt.figure()
    dd_y1820.plot()
    plt.ylabel("drawdown")
    plt.title("value long-short drawdown, 2018-2020")
    plt.savefig("drawdown_2018-2020.png")

    # plot whole period
    dd = drawdown(r_ls)
    plt.figure()
    dd.plot()
    plt.ylabel("drawdown")
    plt.title("value long-short drawdown, whole period")
    plt.savefig("drawdown_whole_period.png")

    # summary
    print(f"{'Period':<28}{'Return':>10}{'Vol':>10}{'Sharpe':>10}{'Max DD':>10}")
    summary(r_ls, "whole sample")
    summary(r_ls.loc["1926-07":"2016-08"], "before (1926-2016)")
    summary(r_ls.loc["2016-09":"2026-08"], "last 10 years (2016-2026)")
    summary(y1820, "2018-2020")


def metrics(r):
    n = len(r)
    m_m_r = r.mean()
    m_std = r.std()
    ann_ret = (1 + r).prod() ** (12 / n) - 1
    ann_vol = m_std * math.sqrt(12)
    sharpe = (m_m_r * 12) / (m_std * math.sqrt(12))
    return ann_ret, ann_vol, sharpe


def drawdown(r):
    cur_wealth = (1 + r).cumprod()
    peak_wealth = cur_wealth.cummax()
    dd =  cur_wealth / peak_wealth - 1
    return dd


def summary(r, label):
    ann_ret, ann_vol, sharpe = metrics(r)
    dd = drawdown(r)
    mdd = dd.min()
    print(f"{label:<28}{ann_ret:>10.2%}{ann_vol:>10.2%}{sharpe:>10.2f}{mdd:>10.2%}")


if __name__ == "__main__":
    main()
