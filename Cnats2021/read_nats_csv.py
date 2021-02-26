# -*- coding: utf-8 -*-
import csv
from scoutingreport import *
import operator
import pandas as pd


weight_classes = [
        "43",
        "47",
        "52",
        "57",
        "63",
        "69",
        "76",
        "84",
        "84+",
        "53",
        "59",
        "66",
        "74",
        "83",
        "93",
        "105",
        "120",
        "120+"
        ]

odd_names = {
        }

def get_lifter_names_from_csv(category = "Equipped"):
    lifters = {}
    for weight_class in weight_classes:
        lifters[weight_class] = []
    with open('cnat_2021.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
            if not (line_count == 0 or line_count == 1):
                if row[-5] == category:
                    name = row[4]
                    weight_class = row[-1]
                    if name not in lifters[weight_class]:
                        lifters[weight_class].append(name)
    return lifters

def get_lifter_data(lifters):
    lifters_totals = {}
    look_up_lifters = {}
    for weight_class in weight_classes:
        lifters_totals[weight_class] = []
        look_up_lifters[weight_class] = []
    for weight_class in weight_classes:
        for lifter in lifters[weight_class]:
            try:
                total = get_best_numbers(get_table_on_lifter(lifter))
                total["Name"] = lifter
                lifters_totals[weight_class].append(total)
            except NameError as e:
                if "Couldn't find lifter:" not in str(e):
                    raise e
                try:
                    print("Odd_name:\t" + lifter)
                    if lifter in odd_names.keys():
                        lifter = odd_names[lifter]
                        print("Actual_name:\t" + lifter)
                        total = get_best_numbers(get_table_on_lifter(lifter))
                        total["Name"] = lifter
                        lifters_totals[weight_class].append(total)
                    else:
                        look_up_lifters[weight_class].append(lifter)
                except NameError as e:
                    if "Couldn't find lifter:" not in str(e):
                        raise e
                    look_up_lifters[weight_class].append(lifter)
            print("Lifter:\t" + lifter + "\t\t\tWeight Class:\t" + weight_class)
    write_look_up_lifters(look_up_lifters)
    return lifters_totals

def write_look_up_lifters(look_up_lifters):
    file1 = open("look_up.txt","w")
    for weight_class, lifters in look_up_lifters.items():
        for lifter in lifters:
            file1.write(lifter + "\n")
    file1.close()

def sort_by(x, by="P-Total"):
    return 0 - x[by]

def sort_lifter_totals(lifters_totals):
    sorted_totals = []
    for weight_class in weight_classes:
        sorted_totals.append(sorted(lifters_totals[weight_class], key=sort_by))
    return sorted_totals

def export(sorted_lifters):
    for i in range(len(weight_classes)):
        df = pd.DataFrame(data=sorted_lifters[i],
                columns = [
                    "Name",
                    "P-Total", "H-Total", "Total",
                    "Squat", "Bench press", "Deadlift",
                    "BF-Squat", "BF-Bench press", "BF-Deadlift"],
                index = range(1,len(sorted_lifters[i]) + 1))
        df.to_excel(weight_classes[i] + '.xlsx')

export(sort_lifter_totals(get_lifter_data(get_lifter_names_from_csv())))
