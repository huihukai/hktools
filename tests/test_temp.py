from utils import file2df, df2file, find

path = r'C:\Users\HUK\Desktop\Scrapy_Learning\Scrapy_Lianjia\outdata'

csv_list = find(path= path, start_str='huk', end_str='csv')

df0 = file2df(csv_list[0])

print(df0)
df2file(df0, fname= 'df0_test.txt', outpath=path)