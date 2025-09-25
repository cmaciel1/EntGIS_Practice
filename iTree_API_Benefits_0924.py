import requests, arcpy, datetime
import xml.etree.ElementTree as et
from arcgis.gis import GIS
arcpy.env.overwriteOutput = True

g = GIS("https://www.arcgis.com", "cassidymaciel", "Bailey131!")

fs = g.content.get('31a0f046a8314d1fbbedfce269dab202')
print(fs.title)
url = fs.url+'/0'
print(url)

fields = ['TreeLocation_Long',
          'TreeLocation_Lat',
          'CountyName',
          'CityName',
          'SpeciesCode_Value',
          'DatePlanted',
          'Condition',
          'HouseVintage',
          'DirectionDegree',
          'DistanceMeter',
          'Heat',
          'Air_Conditioned',
          'EcoBen_RunoffAvoided',
          'EcoBen_RunoffAvoidedValue',
          'EcoBen_HydroIntercep',
          'EcoBen_CORemoved',
          'EcoBen_CORemovedValue',
          'EcoBen_NO2Removed',
          'EcoBen_NO2RemovedValue',
          'EcoBen_SO2Removed',
          'EcoBen_SO2RemovedValue',
          'EcoBen_O3Removed',
          'EcoBen_O3RemovedValue',
          'EcoBen_PM25Removed',
          'EcoBen_PM25RemovedValue',
          'EcoBen_CO2Sequest',
          'EcoBen_CO2SequestValue',
          'EcoBen_CO2Avoided',
          'EcoBen_CO2AvoidedValue',
          'EcoBen_ElectricityHeatValue',
          'EcoBen_ElectricityCoolValue',
          'CreationDate',
          'DBH_CM'
          
         ]
print("hello")
for i, value in enumerate(fields):
    print(f"Index: {i}, Value: {value}")    


print('Running feature class trees through API and calculating Eco Benefits...')
with arcpy.da.UpdateCursor(url, fields) as cursor:
        
    for row in cursor:        

        api_url = 'https://dtbe-api.daveyinstitute.com/v2/getGrowoutTreeBenefit'
        PARAMS = {'key':'272752b916654994a7e781cd037fc4ed',
                      'ProjectYears':'1',
                      'MortalityRate':'0.00',
                      'Longitude':row[0],
                      'Latitude':row[1],
                      'TreeAmount':'1',
                      'Species':row[4],
                      'TreeHeightMeter':'-1',
                      'TreeCrownWidthMeter':'-1',
                      'TreeCrownHeightMeter':'-1',
                      'Condition':row[6],
                      'CLE':'5',
                      'EnergyOnly':'0',
                      'HouseVintage':row[7],
                      'DirectionDegree':row[8],
                      'DistanceMeter':row[9],
                      'Heated':row[10],
                      'AirConditioned':row[11],
                      'DBHCentimeter':row[32]
                 }
        response = requests.get(url = api_url, params = PARAMS)
        print(response.url)

print('Running feature class trees through API and calculating Eco Benefits...')
with arcpy.da.UpdateCursor(url, fields) as cursor:
        
    for row in cursor:        

        api_url = 'https://dtbe-api.daveyinstitute.com/v2/getGrowoutTreeBenefit'
        PARAMS = {'key':'272752b916654994a7e781cd037fc4ed',
                      'ProjectYears':'1',
                      'MortalityRate':'0.00',
                      'Longitude':row[0],
                      'Latitude':row[1],
                      'TreeAmount':'1',
                      'Species':row[4],
                      'TreeHeightMeter':'-1',
                      'TreeCrownWidthMeter':'-1',
                      'TreeCrownHeightMeter':'-1',
                      'Condition':row[6],
                      'CLE':'5',
                      'EnergyOnly':'0',
                      'HouseVintage':row[7],
                      'DirectionDegree':row[8],
                      'DistanceMeter':row[9],
                      'Heated':row[10],
                      'AirConditioned':row[11],
                      'DBHCentimeter':row[32]
                 }
        
        response = requests.get(url = api_url, params = PARAMS)
        root = et.fromstring(response.content)
        if response.status_code == 200:
            print('Status Code = 200')

            for child in root.iter('*'):
                if child.tag == 'RunoffAvoided':
                    row[12] = child.text
                    cursor.updateRow(row)
                elif child.tag == 'RunoffAvoidedValue':
                    row[13] = child.text
                    cursor.updateRow(row)
                elif child.tag == 'Interception':
                    row[14] = child.text
                    cursor.updateRow(row)
                elif child.tag == 'KWhElectricityHeatClimateValue':
                    #row[31] = child.text
                    row[29] = child.text
                    cursor.updateRow(row)
                elif child.tag == 'KWhElectricityCoolClimateValue':
                    #row[31] = child.text
                    row[30] = child.text
                    cursor.updateRow(row)
           
            for child in root.find('.//AirQualityBenefit_PollRemoved'):
                if child.tag == 'CO':
                    row[15] = child.text
                    cursor.updateRow(row)
        
                elif child.tag == 'COValue':
                    row[16] = child.text
                    cursor.updateRow(row)
                        
                elif child.tag == 'NO2':
                    row[17] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'NO2Value':
                    row[18] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'SO2':
                    row[19] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'SO2Value':
                    row[20] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'O3':
                    row[21] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'O3Value':
                    row[22] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'PM25':
                    row[23] = child.text
                    cursor.updateRow(row)
                    
                elif child.tag == 'PM25Value':
                    row[24] = child.text
                    cursor.updateRow(row)
            
                        
                for child in root.find('.//CO2Benefit_Sequestered'):
        
                    if child.tag == 'CO2':
                        row[25] = child.text
                        cursor.updateRow(row)
        
                    elif child.tag == 'CO2Value':
                        row[26] = child.text
                        cursor.updateRow(row)
                        
                for child in root.find('.//CO2Benefit_Avoided'):
        
                    if child.tag == 'CO2':
                        row[27] = child.text
                        cursor.updateRow(row)
        
                    elif child.tag == 'CO2Value':
                        row[28] = child.text
                        cursor.updateRow(row)
                            
print('Done adding eco benefit values to the attribute table')


