from app import db
from app import customers

db.reflect()
table = db.metadata.tables['customers']

columns = [column.name for column in table.columns]
print(columns)
