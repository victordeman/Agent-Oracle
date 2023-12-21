file_path="../../dataset/sample_text.txt"
with open(file_path, 'r') as file:
    text = file.read()

# Split the text into paragraphs based on two newline characters
paragraphs = text.split('\n\n')
#conveert paragraphs to lower case
paragraphs=[i.lower() for i in paragraphs]
# Print the paragraphs
for i, paragraph in enumerate(paragraphs, 1):
    print(f"Paragraph {i}:\n{paragraph.strip()}\n")

entities=['sql','select','insert','delete','update','join']

#create a dictionary for each paragraph with key as paragraph number and value as list of entities
para_dict={}
for i, paragraph in enumerate(paragraphs, 1):
    para_dict[i]=[]
    for entity in entities:
        if entity in paragraph:
            para_dict[i].append(entity)

#create a json with 3 key value pairs, paragraph number, paragraph text and list of entities
para_json={}
for i, paragraph in enumerate(paragraphs, 1):
    para_json["paragraph_no_"+str(i)]={"text":paragraph,"entities":para_dict[i]}

#save the json to a file
import json
with open('paragraphs.json', 'w') as outfile:
    json.dump(para_json, outfile)