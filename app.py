import json
import re
import pymssql

with open('param.json') as json_data:
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

# Ok, now let's get the enum values
for row in fields:

    thisrow = {}

    cursor.execute("select enumId, value from field_enum_values where schemaId=%s and fieldId=%s" % (schemaid, row[0]))
    enums = cursor.fetchall()
    enumerations = {}

    field = str(row[1])
    # Skipping all the junk fields and adding the enumerations
    if re.match("[zZ][0-9][A-Z]",field):
        print("Skipping %s" % row[1])
    else:
        print("Enumerating %s" % row[1])
        for enum in enums:
            enumerations[enum[0]] = enum[1]

        thisrow['fieldId'] = row[0]
        thisrow['valueMap'] = enumerations
        fieldmap["@%s" % str(row[1]).upper().replace(" ","_")] = thisrow

conn.close()

# Here, have some JSON
print(json.dumps(fieldmap, indent=4, sort_keys=True))
