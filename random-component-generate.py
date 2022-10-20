# -*- coding: utf-8 -*-

from http.client import FORBIDDEN
from pickle import FRAME
import random
import os
import imagesize

zone = []
for i in range(122):
    zone.append(0)

def random_color():
    colors1 = '0123456789ABCDEF'
    num = "#"
    for i in range(6):
        num += random.choice(colors1)
    return num

def GBK():
    head = random.randint(0xb0,0xf7)
    body = random.randint(0xa1,0xfe)
    val = f'{head:x}{body:x}'
    str = bytes.fromhex(val).decode('gb2312',errors="ignore")
    return str

def Template_one(num = 100):
    result = []


    for i in range(num):
        #random zone
        zonesize = 100
        zx = random.randint(0,10)
        zy = random.randint(0,10)
        while (zone[zx*5+zy]>0):
            zx = random.randint(0,10)
            zy = random.randint(0,10)
            if (zone[zx*5+zy]==0):
                zone[zx*5+zy] = 1
                break

        temp_dict = dict()
        px = random.randint(0, zonesize/2)
        py = random.randint(0, zonesize/2)
        height = random.randint(20, min(zonesize-px-1,30))
        width = random.randint(height*2, max(zonesize-py-1,height*2))
        fontsize = random.randint(5, max(5,int(height*0.6)))
        temp_dict["content"] = ""
        #for i in range(max(int((width-height)/(fontsize*1.5)),1)):
        for i in range(1):
            temp_dict["content"] = temp_dict["content"] + GBK()
            if len(temp_dict["content"])>=5:
                break
        temp_dict["px"] = str(px+zx*150)  + "px"
        temp_dict["py"] = str(py+zy*150) + "px"
        temp_dict["width"] = str(width) + "px"
        temp_dict["height"] = str(height) + "px"
        temp_dict["fontsize"] = str(fontsize) + "px"
        temp_dict["fontcolor"] = random_color()

        result.append(str(temp_dict).replace('\'','"'))
    return result


def Template_two(num = 100):
    result = []


    for i in range(num):
        #random zone
        zonesize = 100
        zx = random.randint(0,10)
        zy = random.randint(0,10)
        while (zone[zx*5+zy]>0):
            zx = random.randint(0,10)
            zy = random.randint(0,10)
            if (zone[zx*5+zy]==0):
                zone[zx*5+zy] = 1
                break

        temp_dict = dict()
        px = random.randint(0, zonesize/2)
        py = random.randint(0, zonesize/2)
        height = random.randint(20, min(zonesize-px-1,30))
        width = random.randint(height*2, max(zonesize-py-1,height*2))
        fontsize = random.randint(5, max(5,int(height*0.6)))
        temp_dict["content"] = ""
        for i in range(max(int((width-height*2)/(fontsize*1.5)),1)):
            temp_dict["content"] = temp_dict["content"] + GBK()
            if len(temp_dict["content"])>=5:
                break
        temp_dict["px"] = str(px+zx*150)  + "px"
        temp_dict["py"] = str(py+zy*150) + "px"
        temp_dict["width"] = str(width) + "px"
        temp_dict["height"] = str(height) + "px"
        temp_dict["fontsize"] = str(fontsize) + "px"
        temp_dict["backgroundcolor"] = random_color()
        temp_dict["fontcolor"] = random_color()

        result.append(str(temp_dict).replace('\'','"'))
    return result



def generate_example(num=1000, root_path=None):
    for i in range(num):
        zone = []
        for j in range(122):
            zone.append(0)
        bottom_num = random.randint(1, 5)
        result_text = Template_one(bottom_num)
        bottom_num = random.randint(1, 5)
        result_button = Template_two(bottom_num)
        bottom_num = random.randint(1, 5)
        result_input = Template_one(bottom_num)
        bottom_num = random.randint(1, 5)
        result_datepicker = Template_one(bottom_num)
        bottom_num = random.randint(1, 5)
        result_select = Template_one(bottom_num)
        bottom_num = random.randint(1, 5)
        result_radio = Template_one(bottom_num)

        with open(os.path.join(root_path, "example%s.txt" % str(i)), "w", encoding="UTF-8") as fw:
            fw.write(str(len(result_text)) + "\n")
            for case in result_text:
                fw.write(str(case) + "\n")
            fw.write(str(len(result_button)) + "\n")
            for case in result_button:
                fw.write(str(case) + "\n")
            fw.write(str(len(result_input)) + "\n")
            for case in result_input:
                fw.write(str(case) + "\n")
            fw.write(str(len(result_datepicker)) + "\n")
            for case in result_datepicker:
                fw.write(str(case) + "\n")
            fw.write(str(len(result_select)) + "\n")
            for case in result_select:
                fw.write(str(case) + "\n")
            fw.write(str(len(result_radio)) + "\n")
            for case in result_radio:
                fw.write(str(case) + "\n")

#0: text
#1: button
#2: input
#3: radio
def convent2label(file_num,file_path,img_path,label_path):
    for i in range(file_num):
        W,H = imagesize.get(os.path.join(img_path, "test%s.png" % str(i)))
        with open(os.path.join(file_path, "example%s.txt" % str(i)), "r", encoding="UTF-8") as fr:
            class_num = -1
            result_list = []
            for line in fr:
                if len(line)<=2:
                    class_num = class_num + 1
                else:
                    if ((class_num == 3)or(class_num == 4)):
                        continue
                    line_dict = eval(line)
                    width = int(line_dict['width'].split('p')[0])
                    height = int(line_dict['height'].split('p')[0])
                    px = int(line_dict['px'].split('p')[0])
                    py = int(line_dict['py'].split('p')[0])
                    if (width+px>W/1.5):
                        width = int(W/1.5)-px
                    if (height+py>H/1.5):
                        height = int(H/1.5)-py
                    central_px = (px+width/2.0)/(W/1.5)
                    central_py = (py+height/2.0)/(H/1.5)
                    central_width = (width/2.0)/(W/1.5)
                    central_height = (height/2.0)/(H/1.5)
                    if (class_num == 5):
                        result_list.append(str(class_num-2)+' '+'%.6f'%central_px+' '+'%.6f'%central_py+' '+'%.6f'%central_width+' '+'%.6f'%central_height)
                    else:
                        result_list.append(str(class_num)+' '+'%.6f'%central_px+' '+'%.6f'%central_py+' '+'%.6f'%central_width+' '+'%.6f'%central_height)


        with open(os.path.join(label_path, "test%s.txt" % str(i)), "w", encoding="UTF-8") as fw:
            for result in result_list:
                fw.write(result+'\n')

#generate_example(root_path="antd-demo/public/file")
convent2label(1000,"antd-demo/public/file","dataset/webcomponent/images","dataset/webcomponent/labels")
print("successfully !!! ")