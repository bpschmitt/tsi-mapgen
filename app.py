import json
import re
import pymssql
from collections import defaultdict

with open('param.secret.json') as json_data:
    parms = json.load(json_data)

fieldmap = []

conn = pymssql.connect(parms['server'], parms['user'], parms['password'], "ARSystem")
cursor = conn.cursor()

# Get schemaId
cursor.execute("select schemaId from arschema where name='HPD:Help Desk'")
schemaid = cursor.fetchone()[0]

# Get fields
cursor.execute("select fieldId,fieldName from field where schemaId=%s order by fieldName" % schemaid)
fields = cursor.fetchall()

for row in fields:

    thisrow = {}
    # thisrow = {row[0]:row[1]}
    thisrow = {"id":row[0],
               "name": row[1]}


    cursor.execute("select enumId, value from field_enum_values where schemaId=%s and fieldId=%s" % (schemaid, row[0]))
    enums = cursor.fetchall()
    enumerations = {}

    field = str(row[1])
    if re.match("z[0-9][A-Z]",field):
        print("Skipping %s" % row[1])
    else:
        print("Enumerating %s" % row[1])
        for enum in enums:
            enumerations[enum[0]] = enum[1]

        thisrow['enums'] = enumerations

    fieldmap.append(thisrow)
    #fieldmap[row[0]]['test'] = 'test'
    # if len(enums > 0):
    #     for enum in enums:

print(json.dumps(fieldmap, indent=4, sort_keys=True))
conn.close()