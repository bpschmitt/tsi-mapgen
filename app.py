import json
import pymssql

with open('param.secret.json') as json_data:
    parms = json.load(json_data)

fieldmap = {}

conn = pymssql.connect(parms['server'], parms['user'], parms['password'], "ARSystem")
cursor = conn.cursor()

# Get schemaId
cursor.execute("select schemaId from arschema where name='HPD:Help Desk'")
schemaid = cursor.fetchone()[0]

# Get fields
cursor.execute("select fieldId,fieldName from field where schemaId=%s order by fieldName" % schemaid)
fields = cursor.fetchall()

for row in fields:
    fieldmap[row[0]] = row[1]

    cursor.execute("select enumId, value from field_enum_values where schemaId=%s and fieldId=%s" % (schemaid,row[0]))
    enums = cursor.fetchall()
    print(enums)
    # if len(enums > 0):
    #     for enum in enums:

print(json.dumps(fieldmap))


# cursor.execute("select enumId, value from field_enum_values where schemaId=1439 and fieldId=1000000162")
# # you must call commit() to persist your data if you don't set autocommit to True
# conn.commit()

# cursor.execute('SELECT * FROM persons WHERE salesrep=%s', 'John Doe')
# row = cursor.fetchone()
# while row:
#     print("ID=%d, Name=%s" % (row[0], row[1]))
#     row = cursor.fetchone()

conn.close()