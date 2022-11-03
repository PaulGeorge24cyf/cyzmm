#coding=<UTF-8>
from paddleocr import PaddleOCR, draw_ocr
import os
import cv2
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`

#色彩距离
def Dis_Color(a,b):
    return abs(a[0]-b[0])*abs(a[0]-b[0])+abs(a[1]-b[1])*abs(a[1]-b[1])+abs(a[2]-b[2])*abs(a[2]-b[2])

#像素点位置比较
def Compare2Point(x0,y0,x1,y1,offset):
    return ((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))<offset*offset

#矩形内部判定（点）
def PointInRec(p,r_p1,r_p2):
    if (p[0]<min(r_p1[0],r_p2[0]))or(p[0]>max(r_p1[0],r_p2[0])):
        return False
    if (p[1]<min(r_p1[1],r_p2[1]))or(p[1]>max(r_p1[1],r_p2[1])):
        return False
    return True

#矩形内部判断（矩形）
def RecInRec(p1,p2,r_p1,r_p2):
    OFFSET = 5
    if (p1[0]<min(r_p1[0],r_p2[0])-OFFSET)or(p1[0]>max(r_p1[0],r_p2[0])+OFFSET):
        return False
    if (p1[1]<min(r_p1[1],r_p2[1])-OFFSET)or(p1[1]>max(r_p1[1],r_p2[1])+OFFSET):
        return False
    if (p2[0]<min(r_p1[0],r_p2[0])-OFFSET)or(p2[0]>max(r_p1[0],r_p2[0])+OFFSET):
        return False
    if (p2[1]<min(r_p1[1],r_p2[1])-OFFSET)or(p2[1]>max(r_p1[1],r_p2[1])+OFFSET):
        return False
    return True

#中点
def MidPoint(x0,y0,x1,y1):
    return (int((x1+x0)/2),int((y1+y0)/2))

#颜色转换字符串
def Color2Str(color):
    B,G,R = int(color[0]),int(color[1]),int(color[2])
    str = "#"
    dic_hex = '0123456789ABCDEF'
    str = str + dic_hex[round((B-B%16)/16)] + dic_hex[B%16]
    str = str + dic_hex[round((G-G%16)/16)] + dic_hex[G%16]
    str = str + dic_hex[round((R-R%16)/16)] + dic_hex[R%16]
    return str

#PaddleOcr文字识别
def MyOcr(input_img,img_path,K=0.8):
    ocr = PaddleOCR(use_angle_cls=True,use_gpu=False)
    #f = open(text_file,'w+')
    #img = cv2.imread(input_img)
    #img_path = input_img
    img = input_img.copy()
    result = ocr.ocr(img_path, cls=True)
    count = 0
    ocr_result = []
    for line in result:
        #筛选可信度高的结果,K
        if line[1][1]<K:
            continue
        x1 = int(min(line[0][0][0],line[0][1][0],line[0][2][0],line[0][3][0]))
        y1 = int(min(line[0][0][1],line[0][1][1],line[0][2][1],line[0][3][1]))
        x2 = int(max(line[0][0][0],line[0][1][0],line[0][2][0],line[0][3][0]))
        y2 = int(max(line[0][0][1],line[0][1][1],line[0][2][1],line[0][3][1]))
        #边界设置
        border = int(min(x2-x1,y2-y1)/8+1)
        xb1 = x1 + border
        xb2 = x2 - border
        yb1 = y1 + border
        yb2 = y2 - border
        #设置同颜色分辨距离
        COLOR_SAME = 9000
        AVG_COLOR = [0,0,0]
        color_light = [0,0,0]
        color_dark = [0,0,0]
        color_text = [0,0,0]
        color_bg = [0,0,0]
        light_count = 0
        dark_count = 0
        for x in range(xb1,xb2+1):
            for y in range(yb1,yb2+1):
                px = img[y,x]
                for i in range(3):
                    AVG_COLOR[i] = AVG_COLOR[i] + px[i]
        for i in range(3):
            AVG_COLOR[i] = AVG_COLOR[i]/(x2-x1+1)/(y2-y1+1)
        AVG_DST = Dis_Color(AVG_COLOR, [0,0,0])
        for x in range(x1,x2+1):
            for y in range(y1,y2+1):
                px = img[y,x]
                if Dis_Color(px, AVG_COLOR) < COLOR_SAME:
                    continue
                if Dis_Color(px, [0,0,0]) > AVG_DST:
                    for i in range(3):
                        color_light[i] = color_light[i] + px[i]
                    light_count = light_count + 1
                else:
                    for i in range(3):
                        color_dark[i] = color_dark[i] + px[i]
                    dark_count = dark_count + 1  
        #获取文字与背景颜色
        if (light_count==0):
            color_light = AVG_COLOR
            light_count = 1
        if (dark_count==0):
            color_dark = AVG_COLOR
            dark_count = 1         
        for i in range(3):
            color_dark[i] = color_dark[i]/dark_count
            color_light[i] = color_light[i]/light_count    
        if (((dark_count==1) and (light_count*2 < (x2-x1)*(y2-y1))) or ((dark_count>light_count))):
            color_text = color_light
            color_bg = color_dark
            if light_count==1:
                for x in range(xb1,xb2+1):
                    for y in range(yb1,yb2+1): 
                        px = img[y,x]
                        if Dis_Color(px, AVG_COLOR) < COLOR_SAME:
                            img[y,x] = color_dark
            else:
                for x in range(xb1,xb2+1):
                    for y in range(yb1,yb2+1): 
                        px = img[y,x]
                        if Dis_Color(px, [0,0,0]) > AVG_DST:
                            img[y,x] = color_dark
        else:
            color_text = color_dark
            color_bg = color_light
            if dark_count==1:
                for x in range(xb1,xb2+1):
                    for y in range(yb1,yb2+1): 
                        px = img[y,x]
                        if Dis_Color(px, AVG_COLOR) < COLOR_SAME:
                            img[y,x] = color_light
            else:
                for x in range(xb1,xb2+1):
                    for y in range(yb1,yb2+1): 
                        px = img[y,x]
                        if Dis_Color(px, [0,0,0]) < AVG_DST:
                            img[y,x] = color_light             
        
        ocr_result.append((x1,y1,x2,y2,line[1][0],Color2Str(color_bg),Color2Str(color_text)))
        #print(AVG_COLOR,color_light,light_count,color_dark,dark_count,color_text,line[1][0])
        #f.write(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+line[1][0]+' '+str(color_text)+'\n')

    #cv2.imwrite(output_img,img)
    #f.close()
    return ocr_result

#SIFT-KNN图像特征匹配
def PicMatch(img,template_img):
    img2=cv2.imread(template_img)
    img1=img
    #使用SIFT算法获取图像特征的关键点和描述符
    sift=cv2.xfeatures2d.SIFT_create()
    kp1,des1=sift.detectAndCompute(img1,None)
    kp2,des2=sift.detectAndCompute(img2,None)

    #定义FLANN匹配器
    indexParams=dict(algorithm=0,trees=10)
    searchParams=dict(checks=50)
    flann=cv2.FlannBasedMatcher(indexParams,searchParams)
    #使用KNN算法实现图像匹配，并对匹配结果排序
    matches=flann.knnMatch(des1,des2,k=2)
    matches=sorted(matches,key=lambda x:x[0].distance)

    #去除错误匹配，0.5是系数，系数大小不同，匹配的结果也不同
    goodMatches=[]
    for m,n in matches:
        if m.distance<0.5*n.distance:
            goodMatches.append(m)
            x,y=kp1[m.queryIdx].pt
            #print(dir(m))
            #print(m.imgIdx)
            #print(m.queryIdx)
            #print(m.trainIdx)
            #print(x,y)
            #cv2.rectangle(img1,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)



    #获取某个点的坐标位置
    #index是获取匹配结果的中位数
    index = int(len(goodMatches)/2)
    #queryIdx是目标图像的描述符索引
    #x , y = kp1[goodMatches[index].queryIdx].pt
    result = []
    for i in range(index):
        x,y = kp1[goodMatches[i].queryIdx].pt
        result.append((x,y))
    return result
    #将坐标位置勾画在2.png图片上，并显示
    #cv2.rectangle(img1,(int(x),int(y),int(x)+5,int(y)+5),(0,255,0),2)
    #cv2.imshow('match',img1)
    #cv2.waitKey()

#线条/文本框检测
def RectangleMatch(img):
    #img = cv2.imread(input_img)
    W,H,D = img.shape
    img_g = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    MIN_H = 20
    MAX_H = 50
    MIN_W = W/20
    MAX_W = W/2
    OFF_SET = 5
    OFF_SET_BTN = 10

    fld = cv2.ximgproc.createFastLineDetector()
    dlines = fld.detect(img_g)
    xlines = []
    ylines = []
    for dline in dlines:
        x0 = int(round(dline[0][0]))
        y0 = int(round(dline[0][1]))
        x1 = int(round(dline[0][2]))
        y1 = int(round(dline[0][3]))
        if (abs(y0-y1)<OFF_SET):
            #宽度限制
            #cv2.line(img,(x0,y0),(x1,y1),(255,0,0),1,cv2.LINE_AA)
            if (abs(x1-x0)<MIN_W)or(abs(x1-x0)>MAX_W):
                continue
            xlines.append(dline)
            #cv2.line(img,(x0,y0),(x1,y1),(0,255,0),1,cv2.LINE_AA)
        else:
            #高度限制
            if (abs(y1-y0)<MIN_H)or(abs(y1-y0)>MAX_H):
                continue
            ylines.append(dline)
            #cv2.line(img,(x0,y0),(x1,y1),(0,255,0),1,cv2.LINE_AA)
    #Search4Rec
    result = []
    for line1 in xlines:
        y1 = int(round((line1[0][1]+line1[0][3])/2))
        x1_0 = int(round(line1[0][0]))
        x1_1 = int(round(line1[0][2]))
        for line2 in xlines:
            y2 = int(round((line2[0][1]+line2[0][3])/2))
            if (y1>y2):
                continue
            if (abs(y2-y1)<MIN_H)or(abs(y2-y1)>MAX_H):
                continue
            x2_0 = int(round(line2[0][0]))
            x2_1 = int(round(line2[0][2]))
            #cv2.line(img,(x1_0,y1),(x1_1,y1),(0,0,255),1,cv2.LINE_AA)
            #cv2.line(img,(x2_0,y2),(x2_1,y2),(0,0,255),1,cv2.LINE_AA)
            if (abs(x2_0-x1_0)>OFF_SET)or(abs(x2_1-x1_1)>OFF_SET):
                continue
            Recflag = False
            for line3 in ylines:
                x3_0 = int(round(line3[0][0]))
                y3_0 = int(round(line3[0][1]))
                x3_1 = int(round(line3[0][2]))
                y3_1 = int(round(line3[0][3]))
                if Compare2Point(x1_0,y1,x3_0,y3_0,OFF_SET) and Compare2Point(x2_0,y2,x3_1,y3_1,OFF_SET):
                    #cv2.rectangle(img,MidPoint(x1_0,y1,x3_0,y3_0),MidPoint(x2_1,y2,x3_1+x2_1-x2_0,y3_1),(0,255,0),2)
                    result.append((MidPoint(x1_0,y1,x3_0,y3_0),MidPoint(x2_1,y2,x3_1+x2_1-x2_0,y3_1)))
                    Recflag = True
                    break
                if Compare2Point(x1_1,y1,x3_0,y3_0,OFF_SET) and Compare2Point(x2_1,y2,x3_1,y3_1,OFF_SET):
                    #cv2.rectangle(img,MidPoint(x1_0,y1,x3_0-x1_1+x1_0,y3_0),MidPoint(x2_1,y2,x3_1,y3_1),(0,255,0),2)
                    result.append((MidPoint(x1_0,y1,x3_0-x1_1+x1_0,y3_0),MidPoint(x2_1,y2,x3_1,y3_1)))
                    Recflag = True
                    break
            if Recflag:
                break
            '''else:
                AVG_COLOR = [0,0,0]
                for x in range(max(x1_0,x2_0),min(x1_1,x2_1)):
                    for y in range(y1,y2):
                        px = img[y,x]
                        for i in range(3):
                            AVG_COLOR[i] = AVG_COLOR[i] + px[i]
                for i in range(3):
                    AVG_COLOR[i] = AVG_COLOR[i]/(min(x1_1,x2_1)-max(x1_0,x2_0)+1)/(y2-y1+1)
 

                AVG_DST = Dis_Color(AVG_COLOR, [0,0,0])
                if (AVG_DST > Dis_Color(AVG_COLOR, [255,255,255])):
                    cv2.rectangle(img,(max(x1_0,x2_0),y1),(min(x1_1,x2_1),y2),(0,0,255),2)
                    break
            '''

    #cv2.imshow('lines',img)
    #cv2.waitKey()
    return result

#BTN区域匹配
def AreaMatch(input_img):
    img = cv2.imread(input_img)
    W,H,D = img.shape
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    ret,thresh = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    print(contours[0])
    ret = cv2.drawContours(img,contours[0],0,(0,255,0),2)

    cv2.imshow('area',ret)
    cv2.waitKey()

#Ocr+区域二值判定图像文字颜色及清除
#MyOcr(input_img = 'example.jpg',output_img = 'example_no_word.jpg',text_file = 'example_result.txt',K=0.5)
#KNN图像匹配
#PicMatch(input_img = 'example.jpg',template_img = 'example_dp.jpg')
#PicMatch(input_img = 'example/pic3.jpg',template_img = 'example_sl.jpg')
#PicMatch(input_img = 'example/pic3.jpg',template_img = 'example_sl_d.jpg')
#PicMatch(input_img = 'example/pic1.jpg',template_img = 'example_rd_y.jpg')

#RectangleMatch
#RectangleMatch(input_img = 'example/pic8.jpg')

#AreaMatch
#AreaMatch(input_img = 'example/pic8.jpg')

#结果点重合处理
def Point2Result(points):
    result = []
    for pt in points:
        x,y = pt[0],pt[1]
        existFlag = False
        for pt_r in result:
            xr,yr,count = pt_r[0],pt_r[1],pt_r[2]
            if Compare2Point(x,y,xr,yr,10):
                existFlag = True
                pt_r = ((pt_r[0]*pt_r[2]+x)/(pt_r[2]+1),(pt_r[1]*pt_r[2]+x)/(pt_r[2]+1),pt_r[2]+1)
                break
        if not existFlag:
            result.append((x,y,1))
    return result

#矩形重合处理
def Rec2Result(recs):
    result = []
    for rec in recs:
        existFlag = False
        for recr in result:
            if Compare2Point((rec[0][0]+rec[1][0])/2,(rec[0][1]+rec[1][1])/2,(recr[0][0]+recr[1][0])/2,(recr[0][1]+recr[1][1])/2,5):
                existFlag = True
                break
        if not existFlag:
            result.append(rec)
    #print(len(recs),len(result))
    return result

#输出到文件
def Output2File(output_path,ocr_result,rec_result,rd_result,rd_y_result,sl_result,sl_d_result,dp_result):
    rd_result.extend(rd_y_result)
    sl_result.extend(sl_d_result)
    output = open(output_path,'w',encoding='utf-8')
    #关系/类型判定,转换为标准输出格式
    button_dic = ['提交','确认','取消','上一步','下一步','查询','导出','导出EXCEL','导出TXT']
    text_output = []
    button_output = []
    input_output = []
    datepicker_output = []
    select_output = []
    radio_output = []
    for datepicker in dp_result:
        dic = {"type":"DatePicker","content":"","px":"600px","py":"600px","width":"100px","height":"100px","fontsize":"20px","fontcolor":"#000000"}
        #固定大小
        SIZE = 50
        dic['width'] = str(SIZE)+"px"
        dic['height'] = str(SIZE)+"px"
        dic['px'] = str(int(round(datepicker[0]))-SIZE/2)+"px"
        dic['py'] = str(int(round(datepicker[1]))-SIZE/2)+"px"
        datepicker_output.append(dic)
    for text in ocr_result:
        inputFlag = False
        if text[4] in button_dic:
            dic = {"type":"Button","content":"MyButton","px":"300px","py":"300px","width":"100px","height":"100px","fontsize":"20px","backgroundcolor":"#0000FF","fontcolor":"#FF0000"}
            dic['content'] = text[4]
            size = int(round(text[3]-text[1]-2))
            dic['fontsize'] = str(size)+"px"
            dic['px'] = str(int(round(text[0]))-size)+"px"
            dic['py'] = str(int(round(text[1]))-size*2)+"px"
            dic['width'] = str(int(round(text[2]-text[0]))+size*4)+"px"
            dic['height'] = str(int(round(text[3]-text[1]))+size*2)+"px"
            dic['backgroundcolor'] = text[5]
            dic['fontcolor'] = text[6]   
            button_output.append(dic)
            continue
        #判断文本是否为文本框中
        for rec in rec_result:
            if RecInRec((int(text[0]),int(text[1])),(int(text[2]),int(text[3])),rec[0],rec[1]):
                inputFlag = True
                dic = {"type":"Input","content":"MyInput","px":"700px","py":"700px","width":"100px","height":"30px","fontsize":"25px","fontcolor":"#FF0000"}
                dic['content'] = text[4]
                dic['px'] = str(int(min(round(rec[0][0]),round(rec[1][0]))))+"px"
                dic['py'] = str(int(min(round(rec[0][1]),round(rec[1][1]))))+"px"
                dic['width'] = str(int(round(abs(rec[1][0]-rec[0][0]))))+"px"
                dic['height'] = str(int(round(abs(rec[1][1]-rec[0][1]))))+"px"
                dic['fontsize'] = str(int(round(abs(rec[1][1]-rec[0][1])))-5)+"px"
                dic['fontcolor'] = text[6]
                selectFlag = False
                for select in sl_result:
                    if PointInRec(select,rec[0],rec[1]):
                        selectFlag = True
                        dic['type'] = "Select"
                        select_output.append(dic)
                        break
                if selectFlag:
                    break
                input_output.append(dic)
        if inputFlag:
            continue
        #判断文本是否为Radio选项
        radioFlag = False
        dic = {"type":"Text","content":"MyRadio","px":"950px","py":"700px","width":"100px","height":"30px","fontsize":"15px","fontcolor":"#FF0000"}
        dic['content'] = text[4]
        dic['px'] = str(int(round(text[0])))+"px"
        dic['py'] = str(int(round(text[1])))+"px"
        dic['width'] = str(int(round(text[2]-text[0])))+"px"
        dic['height'] = str(int(round(text[3]-text[1])))+"px"
        dic['fontsize'] = str(min(15,int(round(text[3]-text[1]))-2,int(round(text[2]-text[0])/(len(text[4])+2))))+"px"
        dic['fontcolor'] = text[6]      
        for radio in rd_result:
            if PointInRec(radio,(int(text[0])-10,int(text[1])),(int(text[2])-10,int(text[3]))):
                radioFlag = True
                dic['type'] = "Radio"
                dic['px'] = str(int(round(text[0]))-10)+"px"
                dic['width'] = str(int(round(text[2]-text[0]))+10)+"px"
                radio_output.append(dic)
                break
        if not radioFlag:
            text_output.append(dic)
    for rec in rec_result:
        textFlag = False
        for text in ocr_result:
            if RecInRec((int(text[0]),int(text[1])),(int(text[2]),int(text[3])),rec[0],rec[1]):
                textFlag = True
                break
        if not textFlag:
            dic = {"type":"Input","content":"MyInput","px":"700px","py":"700px","width":"100px","height":"30px","fontsize":"25px","fontcolor":"#FF0000"}
            dic['content'] = ""
            dic['px'] = str(int(min(round(rec[0][0]),round(rec[1][0]))))+"px"
            dic['py'] = str(int(min(round(rec[0][1]),round(rec[1][1]))))+"px"
            dic['width'] = str(int(round(abs(rec[1][0]-rec[0][0]))))+"px"
            dic['height'] = str(int(round(abs(rec[1][1]-rec[0][1]))))+"px"
            dic['fontsize'] = str(int(round(abs(rec[1][1]-rec[0][1])))-5)+"px"
            dic['fontcolor'] = "#000000"
            selectFlag = False
            for select in sl_result:
                if PointInRec(select,rec[0],rec[1]):
                    selectFlag = True
                    dic['type'] = "Select"
                    select_output.append(dic)
                    break
            if selectFlag:
                continue
            input_output.append(dic)
    #print(len(input_output),len(rec_result))

    #OUTPUT TEXT/BUTTON/INPUT/DATEPICKER/SELECT/RADIO
    output.write(str(len(text_output)))
    output.write('\n')
    for text in text_output:
        output.write(str(text))
        output.write('\n')
    output.write(str(len(button_output)))
    output.write('\n')
    for button in button_output:
        output.write(str(button))
        output.write('\n')
    output.write(str(len(input_output)))
    output.write('\n')
    for input in input_output:
        output.write(str(input))
        output.write('\n')
    output.write(str(len(datepicker_output)))
    output.write('\n')
    for datepicker in datepicker_output:
        output.write(str(datepicker))
        output.write('\n')
    output.write(str(len(select_output)))
    output.write('\n')
    for select in select_output:
        output.write(str(select))
        output.write('\n')
    output.write(str(len(radio_output)))
    output.write('\n')
    for radio in radio_output:
        output.write(str(radio))
        output.write('\n')
    output.close()

#主过程
def Start(output_path,input_img):
    img = cv2.imread(input_img)
    #DatePicker图标识别
    dp_points = PicMatch(img = img,template_img = 'example_dp.jpg')
    #Select图标识别
    sl_points = PicMatch(img = img,template_img = 'example_sl.jpg')
    sl_d_points = PicMatch(img = img,template_img = 'example_sl_d.jpg')
    #Radio图标识别
    rd_y_points = PicMatch(img = img,template_img = 'example_rd_y.jpg')
    rd_points = PicMatch(img = img,template_img = 'example_rd.jpg')
    rd_points.extend(PicMatch(img = img,template_img = 'example_rd2.jpg'))
    #矩形识别
    recs = RectangleMatch(img = img)
    #Ocr文字识别
    ocr_result = MyOcr(input_img = img,img_path = input_img,K=0.5)
    #可视化展示
    dp_result = Point2Result(dp_points)
    for pt in dp_result:
        x,y = pt[0],pt[1]
        cv2.rectangle(img,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)
    sl_result = Point2Result(sl_points)
    for pt in sl_result:
        x,y = pt[0],pt[1]
        cv2.rectangle(img,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2) 
    sl_d_result = Point2Result(sl_d_points)   
    for pt in sl_d_result:
        x,y = pt[0],pt[1]
        cv2.rectangle(img,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)
    rd_y_result = Point2Result(rd_y_points)   
    for pt in rd_y_result:
        x,y = pt[0],pt[1]
        cv2.rectangle(img,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)
    rd_result = Point2Result(rd_points)
    for pt in rd_result:
        x,y = pt[0],pt[1]
        cv2.rectangle(img,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)
    rec_result = Rec2Result(recs)
    for rec in rec_result:
        cv2.rectangle(img,rec[0],rec[1],(0,0,255),2)
    for text in ocr_result:
        cv2.rectangle(img,(int(text[0]),int(text[1])),(int(text[2]),int(text[3])),(255,0,0),2)
    #输出到文件
    Output2File(output_path,ocr_result,rec_result,rd_result,rd_y_result,sl_result,sl_d_result,dp_result)
    #画图展示
    cv2.imshow('Result',img)
    cv2.waitKey()

def CodeGenerate(input_path,output_path):
    output = open(output_path,'w',encoding='utf-8')
    #代码头部
    output.write('import \'./App.css\';\n')
    output.write('import \'antd/dist/antd.min.css\'\n')
    output.write('import { Button,Input,Select,Radio,DatePicker } from \'antd\';\n')
    output.write('function App() {\n')
    output.write('  return (\n')
    output.write('    <div className="App">\n')
    #填充组件H5代码
    input_f = open(input_path,'r',encoding='utf-8')
    for line in input_f.readlines():
        component = eval(line)
        if type(component)==type(1):
            continue
        if component['type']=='Text':
            outstr = '      <div style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}>'
            outstr = outstr + component['content'] + '</div>\n'
            output.write(outstr)
        if component['type']=='Button':
            outstr = '      <Button style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'backgroundColor:' + '\'' + component['backgroundcolor'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}>'
            outstr = outstr + component['content'] + '</Button>\n'
            output.write(outstr)
        if component['type']=='Input':
            outstr = '      <Input style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}'
            outstr = outstr + ' placeholder=' + '"' + component['content'] + '"' + '/>\n'
            output.write(outstr)
        if component['type']=='Select':
            outstr = '      <Select style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}'
            outstr = outstr + ' placeholder="' + component['content'] + '"/>\n'
            output.write(outstr)    
        if component['type']=='DatePicker':
            outstr = '      <DatePicker bordered={false} style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}/>\n'
            #outstr = outstr + '</DatePicker>\n'
            output.write(outstr)
        if component['type']=='Radio':
            outstr = '      <Radio style={{position:\'absolute\','
            outstr = outstr + 'left:' + '\'' + component['px'] + '\'' + ','
            outstr = outstr + 'top:' + '\'' + component['py'] + '\'' + ','
            outstr = outstr + 'width:' + '\'' + component['width'] + '\'' + ','
            outstr = outstr + 'height:' + '\'' + component['height'] + '\'' + ','
            outstr = outstr + 'fontSize:' + '\'' + component['fontsize'] + '\'' + ','
            outstr = outstr + 'color:' + '\'' + component['fontcolor'] + '\'' + '}}>'
            outstr = outstr + component['content'] + '</Radio>\n'
            output.write(outstr)
    #代码尾部
    output.write('    </div>\n')
    output.write('  );\n')
    output.write('}\n')
    output.write('export default App;')
    output.close()


Start(output_path = 'MyOutput.txt',input_img = 'example/pic1.jpg')

CodeGenerate(input_path = 'MyOutput.txt',output_path = 'react-ant-demo/src/App.js')