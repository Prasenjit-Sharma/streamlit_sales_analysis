import pandas as pd


class DataAnalysis:

    @staticmethod
    def filter_data(df, **filters):
        filtered_df = df
        for key, value in filters.items():
            # print("{} is {}".format(key, value))
            filtered_df = filtered_df[filtered_df[key].isin(value)]
        return filtered_df

    @staticmethod
    def return_hist_fy(curr_fy):
        hist_fy = []
        for fy in curr_fy:
            hist_fy.append(str(int(fy[0:2]) - 1) + '-' + str(int(fy[3:5]) - 1))
        return hist_fy

    @staticmethod
    def calc_mkt_sh(df, fy):
        df = df.groupby('OMC').sum(numeric_only=True)
        # df = df.groupby('OMC').transform('sum')
        ind_vol = df['Volume'].sum()
        df[fy] = df['Volume'].apply(lambda x: int(x))
        df[f'{fy} Mkt Sh'] = df['Volume'].apply(lambda x: round(x / ind_vol * 100, 2))

        df.pop('CUST')
        df.pop('Volume')
        return df

    def sales_mkt_sh(self,**sales_filters):
        curr_omc_sales = self.filter_data(df=self.omc_sales, **sales_filters)
        hist_fy = DataAnalysis.return_hist_fy(curr_fy)
        return curr_omc_sales

    @staticmethod
    def omc_mkt_sh_dataframe(curr_omc_sales,hist_omc_sales,filtered_omc_master):
        curr_omc_sales_master = pd.merge(curr_omc_sales, filtered_omc_master[['CUST', 'OMC']], how='left', on='CUST')
        hist_omc_sales_master = pd.merge(hist_omc_sales, filtered_omc_master[['CUST', 'OMC']], how='left', on='CUST')

        omc_curr_mktsh = DataAnalysis.calc_mkt_sh(curr_omc_sales_master, 'Curr')
        omc_hist_mktsh = DataAnalysis.calc_mkt_sh(hist_omc_sales_master, 'Hist')

        mkt_sh = pd.merge(omc_curr_mktsh, omc_hist_mktsh, how='inner', on='OMC')
        mkt_sh['Growth%'] = round(mkt_sh['Curr'] / mkt_sh['Hist'] * 100 - 100, 2)
        mkt_sh['Mkt Sh Diff'] = mkt_sh['Curr Mkt Sh'] - mkt_sh['Hist Mkt Sh']
        cols = ['Curr', 'Hist', 'Growth%', 'Curr Mkt Sh', 'Hist Mkt Sh', 'Mkt Sh Diff']
        mkt_sh = mkt_sh[cols]
        return mkt_sh
