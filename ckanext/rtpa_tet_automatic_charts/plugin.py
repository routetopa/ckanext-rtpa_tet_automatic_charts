import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import urllib2
from pylons import config
from ckan.lib.base import BaseController
from ckan.common import json, response, request
import pandas as pd
import numpy as np
from pandas.io.json import json_normalize


class Rtpa_Tet_Automatic_ChartsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IResourceView, inherit=True)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IConfigurer

    



    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'rtpa_tet_automatic_charts')
    
    # IRoutes
    @staticmethod
    def after_map(m):
         m.connect('get_table_data', '/rtpa/{resource_id}/{field_id}',
            controller='ckanext.rtpa_tet_automatic_charts.plugin:TableApi', action='get_table_data')
         return m
         
         
         
    def getFields(self,context,data_dict):
		url=self.getResourceURL(context,data_dict)
		data=json.loads(urllib2.urlopen(url).read())
		Dataframe=pd.read_json(json.dumps(data['result']['records']))
		NumericColumns=(Dataframe.select_dtypes(exclude=['object','datetime']).columns)
		return NumericColumns
		
    def getResourceURL(self,context,data_dict):
		datasetId=(data_dict['resource']['id'])
		ckanurl=config.get('ckan.site_url', '')
		datadownloadurl=ckanurl+'/api/3/action/datastore_search?resource_id='+datasetId
		return datadownloadurl
    

    def getDataFrequency(self,context, data_dict):
		url=self.getResourceURL(context,data_dict)
		data=json.loads(urllib2.urlopen(url).read())
		Dataframe=pd.read_json(json.dumps(data['result']['records']))
		NumericDataframe=Dataframe.select_dtypes(exclude=['object'])
		DataforC3=[]
		for numericColumn in NumericDataframe:
			DataperColumnC3=[]
			tempcolumn=NumericDataframe[numericColumn]
			distribution=np.histogram(tempcolumn,11)
			valueFromValueToData=[]
			valueRanges=distribution[1].tolist()
			for i in range(0,11):
				valueFromValueToData.append(str(round(valueRanges[i]))+" to "+str(round(valueRanges[i+1])))
			DataperColumnC3.append([numericColumn,distribution[0].tolist(),valueFromValueToData])
			DataforC3.append(DataperColumnC3)
		return DataforC3


    def info(self):
		return { 
				'name': 'rtpa_tet_automatic_charts',
				'title': 'Charts',
				'icon': 'table',
				'default_title': 'Charts',
				}
				

    def view_template(self, context, data_dict):
		return "rtpa_tet_automatic_charts-view.html"
        
    def can_view(self, data_dict):
        return True
        
    def setup_template_variables(self, context, data_dict):
        datasetId=(data_dict['resource']['id'])
        numericColumns=self.getFields(context,data_dict)
        ckanurl=config.get('ckan.site_url', '')
        DataC3=self.getDataFrequency(context, data_dict)
        return{'dataforc3': json.dumps(DataC3),
               'dataset_id': datasetId,
               'resource_fields': numericColumns,
               'ckanurl': ckanurl}
        
        
class TableApi(BaseController):

    def get_table_data(self, resource_id ,field_id):
        response.content_type = 'application/json; charset=UTF-8'
	
        ckanurl=config.get('ckan.site_url', '')
        url = ckanurl +  "/api/action/datastore_search_sql?sql=" + urllib2.quote("SELECT \"" + field_id + "\" FROM \"" + resource_id + "\"")
        
        return self.column_summary(url, field_id)
        
    def column_summary(self,url, field_id):
		try:
			data=json.loads(urllib2.urlopen(url).read())
			temp_data = json_normalize(data["result"]["records"])
			fields = data["result"]["fields"] # type_unified TODO
			record_count = 0
			results = {
				"help": "http://google.com",
				"success": True,
				"result" : {
				"records" : [],
					"fields" : [
					{"id":"Name", "type" : "text"},
					{"id":"Range", "type" : "text"},
					{"id":"Frequency", "type" : "numeric"}
					],
				"total" : 0,
				"limit":99999,
				}
			}

			for f in fields:
				if f["id"] == field_id:
					break
			if f["type"] ==  "numeric":
				c = f["id"]
				temp_data[c] = pd.to_numeric(temp_data[c], errors='coerce')
				dist = np.histogram(temp_data[c],11)
				for i in range (0, 11):
					record = {
					"Name" : c,
					"Range" : str(round(dist[1][i]))+" to "+str(round(dist[1][i+1])),
					"Frequency" : int(dist[0][i])
					}
					results["result"]["records"].append(record)
					record_count += 1
			if f["type"] ==  "text":
				c = f["id"]
				counts = Counter(temp_data[c])
				for item in counts.most_common(10):
					value = item[0]
					if len(value) > 35:
						value = value[:35] + "..."
					record = {
					"Name" : c,
					"Value" : value,
					"Count" : item[1]
					}
					results["result"]["records"].append(record)
					record_count += 1 
				results["result"]["fields"] = [ {"id":"Name", "type" : "text"},
				{"id":"Value", "type" : "text"},
				{"id":"count", "type" : "numeric"}
				]               

			results["result"]["total"] = record_count
			json_response =  json.dumps(results)

			#response["Access-Control-Allow-Origin"] = "*"
			#print("Response")
			#print(response)

			return json_response

		except Exception as e:
			print("ERROR\n\n\n")
			print(e)
			return json.dumps({'success': False})

