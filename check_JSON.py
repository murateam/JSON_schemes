import os

import sys
import json
import jsonschema
from jsonschema import validate

"""
	This script checks all JSON files in folder /event with JSON schemes in folder /schema
	script creates the log file as result in root folder
"""

schemespath = os.getcwd() + "\\schema"
json_path = os.getcwd() + "\\event"


# get all schemes for JSON
schemes_dict = {}
for schema in os.listdir(schemespath):
	with open(os.path.join(schemespath, schema), 'r') as schema_file:
		schema_data = schema_file.read()
	schema_d = json.loads(schema_data)
	schemes_dict[schema] = schema_d

# get all JSON files 
json_dict = {}
for j in os.listdir(json_path):
	with open(os.path.join(json_path, j), 'r') as json_file:
		json_data = json_file.read()
	json_item = json.loads(json_data)
	json_dict[j] = json_item


#checks all JSON files with JSON schemes via validate method
with open("log.txt", 'w') as file_write:
	for json_name in json_dict:
		file_write.write("JSON file: ")
		file_write.write(json_name + '\n')
		print(json_name)
		for schema in schemes_dict:
			try:
				validate(json_dict[json_name], schemes_dict[schema])
				file_write.write('\t'+"JSON schema: " + schema + '\n')
				file_write.write('\t\t' + "result: " + "OK")

				print("OK")
			except jsonschema.exceptions.ValidationError as ve:
				file_write.write('\t' + "JSON schema: " + schema + '\n')
				file_write.write('\t\t'+"result: " + "ERROR" + '\n')
				file_write.write('\t\t\t' + "reasons:" + '\n')
				file_write.write('\t\t\t\t' + ve.message + '\n')
				file_write.write('\t\t\t\t' + "-----" + '\n')
				file_write.write('\t\t\t\t' + "for this schema required properties are:" + '\n' + '\t\t\t\t\t')
				for field in ve.validator_value:
					file_write.write(field+', ')
				file_write.write(' \n')
				file_write.write('\t\t\t' + " " + '\n')
				file_write.write('\t\t' + "For successfull result you need to add all required fields" + '\n')
				file_write.write('\t\t\t' + " " + '\n')

				print("\t", ve.message)
		file_write.write(' \n')