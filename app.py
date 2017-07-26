import json
import re
import pymssql
from collections import OrderedDict

with open('param.secret.json') as json_data:
    parms = json.load(json_data)

fieldmap = {}
props = {}
jsonoutput = {}

conn = pymssql.connect(parms['mssql_server'], parms['mssql_user'], parms['mssql_password'], parms['remedydb_name'])
cursor = conn.cursor()

# Get schemaId
cursor.execute("select schemaId from arschema where name='HPD:Help Desk'")
schemaid = cursor.fetchone()[0]

# Get fields
cursor.execute("select fieldId,fieldName from field where schemaId=%s and fieldname in ('Impact','Category') order by fieldName asc" % schemaid)
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

# Done with the connection
conn.close()

# Here, have some JSON
for field in fieldmap:
    jsonoutput[field] = fieldmap[field]

jsonoutput["config"] = {
        "remedyHostName":"",
   		"remedyUserName":"",
   		"remedyPassword":"",
		"remedyPort":"",
   		"tsiApiToken":"",
		"tsiEventEndpoint" : "https://api.truesight.bmc.com/v1/events",
		"queryStatusList":[0,1,5],
  		"startDateTime":"2012-01-01 00:00:00 UTC",
  		"endDateTime":"2017-07-24 00:00:00 UTC"
}
jsonoutput["eventDefinitions"] = {
    "properties": props,
    "title":"@SUMMARY",
    "fingerprintFields": ["IncidentNumber","createdAt"],
    "severity":"@SEVERITY",
    "status":"@STATUS",
    "createdAt":"@SUBMIT_DATE",
    "eventClass": "Incident",
		"source": {
			"name": "Remedy",
			"type": "Remedy",
			"ref": "Remedy"
		},
		"sender": {
			"name": "Remedy",
			"type": "Remedy",
			"ref": "Remedy"
		}
}

print(json.dumps(jsonoutput,indent=4))
# print(fieldmap)
# print(properties)

# fieldsjson = json.dumps(fieldmap, indent=4, sort_keys=True)
# propsjson = json.dumps(properties, indent=4, sort_keys=True)

#print("%s,%s" % (json.loads(propsjson),json.loads(fieldsjson)))
# print(fieldsjson)

# Write it to a file
# fo = open(parms['mapfile'],"w")
# fo.write(fieldsjson)
# fo.close()
#
fo = open(parms['propsfile'],"w")
fo.write(json.dumps(jsonoutput, indent=4))
fo.close()
