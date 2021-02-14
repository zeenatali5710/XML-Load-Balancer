#!/usr/bin/env python
# coding: utf-8

#     XML load balancer                        Created by: Zeenat Ali                    Date : 08/02/2020

# In[4]:


# import packages
import xml.etree.ElementTree as ET
import xml.etree


# In[5]:


# Parse through the XML file and get root node
tree = ET.parse('xmlFile_Raw.xml')
root = tree.getroot()

# Get list of tags under root node
# for child in root:
#     print(child.tag)
print('Enter any key to continue..')
a = input()


# In[6]:


# Trial method 1 : XML to csv --> modify csv --> csv to XML
# with open('Params.csv', 'w', newline='') as myfile:                
#     for child in root:
#         if child.tag == "default-processes":
#             #print(child.tag)
#             for child1 in child:
#                 #ipmgr
#                 if child1.attrib['name'] == 'openfep':
# #                 print(child1.attrib['params'])
# #                 print(child1.attrib['params'].split())
#                     List = child1.attrib['params'].split()
#                     print(List)
#                     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#                     wr.writerow(List)

# #Fix the bug - rows missing (outputs only 29 out of 44)
# RangeList = [[44],[45],[46],[47]]
# # ,[44],[45],[46],[47],[44],[45],[46],[47],[44],[45],[46],[47], [44],[45],[46],[47],[44],[45],[46],[47],[44],[45],[46],[47], [44],[45],[46],[47], [44],[45],[46],[47]]           
# print(len(RangeList))
# count = 0
# with open('Params.csv', 'r') as read_obj, open('Params20.csv', 'w', newline='') as write_obj:
#     csv_reader = reader(read_obj)
#     print(csv_reader)
#     csv_writer = writer(write_obj)
#     for row1 in csv_reader:
#         for row in zip(csv_reader, RangeList):
#             print(row)
#             csv_writer.writerow(row)
#             count = count + 1
# print('count: ', count)
# # try:
# #     xmldict = xmltodict.parse('xmlFile_Raw')
# # except xmltodict.expat.ExpatError:
# #     print("that's right")


# In[7]:


# Trial method 2: Use pandas
# import pandas as pd
# df = pd.read_csv('Params20.csv', sep=',')
# def convert_row(row):
#     return """<params="%s">
#     <type>%s</type>
# </params>""" % (row.params, row.load)

# print('\n'.join(df.apply(convert_row, axis=1)))
# print(child1.text)
# child1.attrib['params']

# for child in root:
#     if child.tag == "default-processes":
#         print(child.tag)
#         for child1 in child:
#             if child1.attrib['name'] == 'openfep' and child1.attrib['params'] == '17 -s 44':
#                 child1.attrib['params'] = 'test'
#                 print(child1.attrib['params'])
#                 wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#                 wr.writerow(child1.attrib['params'])


# In[8]:


# Trial method 3 : parse through the list
# for repeat in range(100):
#     while(i<4):
#         load = ['44', '45', '46', '47']
#         print(load[i])
#         i = i + 1
#     i = 0
    
# i = 0
# load = ['44', '45', '46', '47']
# for item in range(100):
#     if(i == 4):
#         i = 0
#     print(load[i])
#     i = i+1


# In[9]:


# Trial method 4 (working) : Append XML and write into tree

# Enter load range and process name
print('Enter load range and process name:')
print('Enter start range')
startRange = input()
print('Enter end range')
endRange = input()
print('your start range is ' + startRange)
print('your end range is ' + endRange)

#Create load list
print('Creating load range list...')
loadList = []
loadItem = int(startRange)
while loadItem <  int(endRange) + 1:
    loadList.append(loadItem)
    loadItem = loadItem + 1
print('Your load list is : ')
print(loadList)

#Skip loads from the series
print('Enter items to skip separated by space')
skipElem = [ int(x) for x in input().split()] 
print('you skipped the following elements : ' )
print(skipElem)
loadList = [ele for ele in loadList if ele not in skipElem]
print('Your updated load list is : ')
print(loadList)

# Check if entered process exists
processList= []
for processes in root.findall('default-processes'):
    for process in processes.findall('process'):
        processList.append(process.attrib['name'])
        processList = list(dict.fromkeys(processList))
print('\n')
print('Available process are:')
print(processList)
print('Enter process name from above list')
processName = input()
print('your process name is : ' + processName)
while(processName not in processList):
    print('process does not exist !!')
    print('Enter process name')
    processName = input()
    print('your process name is : ' + processName)

# Modify XML
print('\n')
print('Modifying XML....')

#Load balance range index
i = 0

#Tag : default-processes
for processes in root.findall('default-processes'):
    
    # Tag : process
    for process in processes.findall('process'):
        
        # Tag : openfep --> input to be taken from user.
        if process.attrib['name'] == processName:
            item_name = process.get('name')
#             print(item_name)
            item_params = process.get('params')
#             print(item_params)
            if(item_name == processName):
                elem = item_params.split()
                if(i > len(loadList)-1):
                    i = 0
                    
                # Take new load : load[i]
                item_params = elem[0] + ' ' + elem[1] + ' ' + str(loadList[i])
                i = i + 1
                print(item_params)
                process.attrib['params'] = item_params
        
# Write to XML
tree.write('outputXml.xml')

print('Modifying XML completed. Check file : outputXml.xml')
print('Enter any key to exit..')
a = input()


# In[ ]:




