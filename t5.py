import json
import os

#Three models: flan-t5-large, t5-large, bloom-560m

# This one is flan-t5-large
# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("t5-large")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-large")

# Load model directly
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-xl")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-xl")


path = os.getcwd()
## This document is generated by object detection model with bounding box
with open(path + '/processed_location_nodup.json', 'r') as f:
    concepts = json.load(f)

with open(path + '/fewshots.json', 'r') as f:
    fewshots = json.load(f)
    







# print(tokenizer.decode(outputs[0])[6:-4])
#This function reads the image id and labels for each image from json file
def location_reader(json_file):
    imageId = list()
    labels = list()
    for image in json_file:
        imageId.append(image[0]['image_id'])
        label = list()
        for object in image[1:]:
            label.append(object['labels'])
        labels.append(label)
    return imageId, labels



def generate_prompts(num_of_prompts, num_of_gtc):    
    
    
    
    if num_of_prompts == 0:
        return """We have following objects {0} in an image, \nA caption of this image could be:"""
    else:
        prompt = f"""Here are {num_of_prompts} examples of a sentence that uses objects in an image to generate the caption:"""
        for i in range(num_of_prompts):  
            fewshot_labels = fewshots[i]['labels']
            fewshot_captions = fewshots[i]['caption']
            l = [x['caption'] for x in fewshot_captions]
            l = l[:num_of_gtc]
            labels = ", ".join(fewshot_labels)
            label_prompts = f"We have following objects {labels} in an image, there are {num_of_gtc} possible captions for this image:"
            for num, cap in enumerate(l):
                l[num] = str(num+1) + '. ' + l[num]
            caption_prompts = '\t'+'\n\t'.join(l)
            prompt = prompt + '\n' + label_prompts + '\n' + caption_prompts

        prompt = prompt + '\n' + "Now, we have following objects {0} in an image, A caption of this image could be:"
        return prompt

imageId, labels = location_reader(concepts)


def finalprompt(concepts_name, p, g):
    concept = ', '.join(concepts_name)
    return generate_prompts(p, g).format(concept)
# print(labels[0])
# print(finalprompt(labels[0]))





# for i in trange(5):
#     objects_labels = labels[i]
#     input_ids = tokenizer(finalprompt(objects_labels), return_tensors="pt").input_ids
#     outputs = model.generate(input_ids, max_length=200)
#     results.append({
#         # 'id': catIds[0],
#         "image_id": imageId[i],
#         "caption": tokenizer.decode(outputs[0])[6:-4],
#     })


def output():
    combo = list()
    for i in range(2):
        a = list()
        a.append(i)
        a.append(1)
        combo.append(a)
    print(combo)
    for com in combo:
        results =[]
        for i in range(500):
            objects_labels = labels[i]
            input_ids = tokenizer(finalprompt(objects_labels, com[0], com[1]), return_tensors="pt").input_ids
            outputs = model.generate(input_ids, max_length=200)
            results.append({
                # 'id': catIds[0],
                "image_id": imageId[i],
                "caption": tokenizer.decode(outputs[0])[6:-4],
            })
        name = f"T5_results_nodup_{com[0]}shots_{com[1]}captions.json"
        with open(path + '/' + name, 'w') as f:
            data = json.dump(results, f, indent=2)
            
output()
# print(results)
# with open('one.json', 'w') as f:
#     data = json.dump(results, f, indent=2)
