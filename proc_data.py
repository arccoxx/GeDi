import numpy as np
import csv
import random
import pandas as pd




def proc_and_binarize(dir, topics):
    fid = open(dir+ "/train.tsv")
    train= fid.read()
    train = train.split("\n")[:-1]

    fid = open(dir+ "/dev.tsv")
    test = fid.read()
    test = test.split("\n")[:-1]
    topics_pre = topics
    topics = []
    for t in topics_pre:
        topics.append(t.lower())
    print(topics)
    #topics = ['ARTS', 'BUSINESS', 'TRAVEL', 'POLITICS', 'EDUCATION',
       #'ENTERTAINMENT', 'GREEN', 'TECH', 'THE WORLDPOST', 'RELIGION',
       #'PARENTING', 'WOMEN', 'WELLNESS', 'HEALTHY LIVING', 'WORLD NEWS',
       #'BLACK VOICES', 'HOME & LIVING', 'FOOD & DRINK', 'PARENTS',
       #'DIVORCE', 'SCIENCE', 'QUEER VOICES', 'COMEDY', 'STYLE & BEAUTY',
       #'WEDDINGS', 'ARTS & CULTURE', 'IMPACT', 'CRIME', 'WEIRD NEWS',
       #'MEDIA', 'COLLEGE', 'TASTE', 'STYLE', 'MONEY', 'CULTURE & ARTS',
       #'SPORTS', 'WORLDPOST', 'FIFTY', 'GOOD NEWS', 'ENVIRONMENT',
       #'LATINO VOICES']

    true_test = []
    false_test = []

    true_train = []
    false_train = []

    range_arr = list(range(0,len(topics)))


    for i in range(0,len(test)):
        line = test[i].split('\t')
        label = line[0]


        if not(len(line) ==2):
            print("skipping " +str(i))
            continue

        if label[0] =="\"":
            label = label[1:-1]
        #label = int(label)-1
        text = line[1]
        if text[0] =="\"":
            text = text[1:-1]
        if text[0] == " ":
            text = text[1:]



        #choice_array = range_arr[:label]+range_arr[label+1:]
        choice_array = [topic for topic in topics if topic != label]
        ps_label = random.choice(choice_array)

        try:
            true_ex = line[0] + text
        except:
            print('label: ' + str(label) + ' text: ' + str(text) + ' ' + str(topics))
        false_ex = ps_label  + text
        true_test.append(true_ex)
        false_test.append(false_ex)

    for i in range(0,len(train)):
        line = train[i].split('\t')

        if not(len(line) ==2):
            print("skipping " +str(i))
            continue



        label = line[0]
        if label[0] =="\"":
            label = label[1:-1]
        
        text = line[1]
        if text[0] =="\"":
            text = text[1:-1]

        if text[0] == " ":
            text = text[1:]

        choice_array = [topic for topic in topics if topic != label]
        ps_label = random.choice(choice_array)

        true_ex = label +  text
        false_ex = ps_label +  text
        true_train.append(true_ex)
        false_train.append(false_ex)

    return true_train,false_train,true_test,false_test

def main():

    fid = open("data/train.csv")
    topics_frame = pd.read_csv('data/train.csv')
    topics = topics_frame[topics_frame.columns[0]].unique()

    text_train = fid.read()


    fid  = open("data/test.csv")
    text_test = fid.read()
    fid.close()


    csv.writer(open("data/train.tsv", 'w+'), delimiter='\t').writerows(csv.reader(open("data/train.csv")))
    csv.writer(open("data/dev.tsv", 'w+'), delimiter='\t').writerows(csv.reader(open("data/test.csv")))


    true_train, false_train, true_test, false_test = proc_and_binarize("data/", topics)
    random.shuffle(true_train)
    random.shuffle(false_train)
    random.shuffle(true_test)
    random.shuffle(false_test)


    false_lines = []
    true_lines = []
    for i in range(0,len(false_test)):
        false_lines.append(false_test[i] + "\t0" + "\n")
    for i in range(0,len(false_test)):
        true_lines.append(true_test[i] + "\t1" + "\n")

    test_lines = false_lines+true_lines
    random.shuffle(test_lines)

    false_lines = []
    true_lines = []
    for i in range(0,len(false_train)):
        false_lines.append(false_train[i] + "\t0" + "\n")
    for i in range(0,len(true_train)):
        true_lines.append(true_train[i] + "\t1" + "\n")

    train_lines = false_lines+true_lines
    random.shuffle(train_lines)

    train_split_all= "\n" + "".join(train_lines)
    test_split_all= "\n" + "".join(test_lines)


    fid = open("data/train.tsv",'w')
    fid.write(train_split_all)
    fid.close()

    fid = open("data/dev.tsv",'w')
    fid.write(test_split_all)
    fid.close()



main()