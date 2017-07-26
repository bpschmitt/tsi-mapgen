import json
import re
import pymssql

with open('param.secret.json') as json_data:
    parms = json.load(json_data)

fieldmap = {}
props = {}
properties = {}

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
    enumerations = {}

    cursor.execute("select enumId, value from field_enum_values where schemaId=%s and fieldId=%s" % (schemaid, row[0]))
    enums = cursor.fetchall()

    field = str(row[1])
    # Skipping all the junk fields and adding the enumerations
    if re.match("[zZ][0-9].*",field):
        print("Skipping %s" % row[1])
        continue
    elif re.match("z[G,D,P,T]",field):
        print("Skipping %s" % row[1])
        continue
    else:
        print("Enumerating %s" % row[1])
        for enum in enums:
            enumerations[enum[0]] = enum[1]

        thisrow['fieldId'] = row[0]
        thisrow['valueMap'] = enumerations
        fieldmap["@%s" % str(row[1]).upper().replace(" ","_")] = thisrow
        props[str(row[1]).replace(" ","_")] = "@%s" % str(row[1]).upper().replace(" ","_")
conn.close()

# Here, have some JSON
properties["properties"] = props

fieldsjson = json.dumps(fieldmap, indent=4, sort_keys=True)
propsjson = json.dumps(properties, indent=4, sort_keys=True)

#print("%s,%s" % (json.loads(propsjson),json.loads(fieldsjson)))
# print(fieldsjson)

# Write it to a file
fo = open(parms['mapfile'],"w")
fo.write(fieldsjson)
fo.close()

fo = open(parms['propsfile'],"w")
fo.write(propsjson)
fo.close()
