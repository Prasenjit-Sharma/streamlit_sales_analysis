import pandas as pd

GOOGLE_DRIVE_URL = "https://docs.google.com/spreadsheets/d/1xb7vPKFF2xMRm2tuIs_nXoofscmMR-7k/edit?usp=sharing&ouid" \
                   "=108088175004483400380&rtpof=true&sd=true "
OMC_MASTER_SHEET = "OMC_Master"
OMC_MS_SHEET = "OMC_MS"
OMC_HSD_SHEET = "OMC_HSD"

PRODUCT_MS = "MS"
PRODUCT_HSD = "HSD"


class ReadData:

    def __init__(self):
        self.omc_master = self.read_data_google_xlsx(url=GOOGLE_DRIVE_URL, sheet_name=OMC_MASTER_SHEET)
        self.omc_sales = self.create_sales_data()

    # Read XLSX from Google Drive
    def read_data_google_xlsx(self, url, sheet_name):
        url_for_pandas = url.replace("/edit?usp=sharing", "/export?format=xlsx")
        # print(url_for_pandas)
        df = pd.read_excel(url_for_pandas, engine='openpyxl', sheet_name=sheet_name)
        df = df.fillna(0)
        return df

    # Read CSV from Google Drive
    def read_data_google_csv(self, url):
        file_id = url.split('/')[-2]
        dwn_url = 'https://drive.google.com/uc?id=' + file_id
        df = pd.read_csv(dwn_url)
        return df

    # Clean Sales Data, transpose Date columns, get month, year and fiscal year
    def clean_sales_data(self, df, product):
        df["PRODUCT"] = product

        long_df = df.melt(id_vars=['CUST', 'DEALERNAME', 'PRODUCT'], var_name='Date', value_name='Volume')
        long_df["Date"] = pd.to_datetime(long_df['Date'])
        long_df["Month"] = long_df["Date"].dt.month_name().apply(lambda x: str(x)[:3])
        long_df["Year"] = long_df["Date"].dt.year.apply(lambda x: str(x)[2:])
        long_df["FiscalYear"] = pd.to_datetime(long_df['Date']).dt.to_period("Q-MAR").dt.qyear.apply(
            lambda x: str(x-1)[2:] + "-" + str(x)[2:])
        return long_df

    # Create the Sales Data by combining MS and HSD Sales
    def create_sales_data(self):
        omc_ms = self.read_data_google_xlsx(url=GOOGLE_DRIVE_URL, sheet_name=OMC_MS_SHEET)
        omc_ms = self.clean_sales_data(df=omc_ms, product=PRODUCT_MS)
        omc_hsd = self.read_data_google_xlsx(url=GOOGLE_DRIVE_URL, sheet_name=OMC_HSD_SHEET)
        omc_hsd = self.clean_sales_data(df=omc_hsd, product=PRODUCT_HSD)
        omc_sales = pd.concat([omc_ms, omc_hsd])
        return omc_sales
