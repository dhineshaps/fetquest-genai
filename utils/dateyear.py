from dateutil.relativedelta import relativedelta
import datetime

current_date = datetime.datetime.now().date()

print(current_date)

chk = current_date - relativedelta(years=5)
print(chk)
