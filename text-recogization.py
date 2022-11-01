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

#中点
def MidPoint(x0,y0,x1,y1):
    return (int((x1+x0)/2),int((y1+y0)/2))

#PaddleOcr文字识别
def MyOcr(input_img,output_img,text_file,K=0.8):
    ocr = PaddleOCR(use_angle_cls=True,use_gpu=False)
    f = open(text_file,'w+')
    img = cv2.imread(input_img)
    img_path = input_img
    result = ocr.ocr(img_path, cls=True)
    count = 0
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
        

        print(AVG_COLOR,color_light,light_count,color_dark,dark_count,color_text,line[1][0])
        f.write(str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+line[1][0]+' '+str(color_text)+'\n')

    cv2.imwrite(output_img,img)
    f.close()

#SIFT-KNN图像特征匹配
def PicMatch(input_img,template_img):
    #import cv2
    img2=cv2.imread(template_img)
    img1=cv2.imread(input_img)
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

    #去除错误匹配，0.5是系数，系数大小不同，匹配的结果页不同
    goodMatches=[]
    for m,n in matches:
        if m.distance<0.5*n.distance:
            goodMatches.append(m)
            x,y=kp1[m.queryIdx].pt
            print(dir(m))
            print(m.imgIdx)
            print(m.queryIdx)
            print(m.trainIdx)
            print(x,y)
            cv2.rectangle(img1,(int(x),int(y)),(int(x)+5,int(y)+5),(0,255,0),2)



    #获取某个点的坐标位置
    #index是获取匹配结果的中位数
    index=int(len(goodMatches)/2)
    #queryIdx是目标图像的描述符索引
    x,y=kp1[goodMatches[index].queryIdx].pt
    #将坐标位置勾画在2.png图片上，并显示
    #cv2.rectangle(img1,(int(x),int(y),int(x)+5,int(y)+5),(0,255,0),2)
    cv2.imshow('match',img1)
    cv2.waitKey()

#线条/文本框检测
def RectangleMatch(input_img):
    img = cv2.imread(input_img)
    W,H,D = img.shape
    #img = cv2.GaussianBlur(img,(3,3),sigmaX=0,sigmaY=0)
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
                    cv2.rectangle(img,MidPoint(x1_0,y1,x3_0,y3_0),MidPoint(x2_1,y2,x3_1+x2_1-x2_0,y3_1),(0,255,0),2)
                    Recflag = True
                    break
                if Compare2Point(x1_1,y1,x3_0,y3_0,OFF_SET) and Compare2Point(x2_1,y2,x3_1,y3_1,OFF_SET):
                    cv2.rectangle(img,MidPoint(x1_0,y1,x3_0-x1_1+x1_0,y3_0),MidPoint(x2_1,y2,x3_1,y3_1),(0,255,0),2)
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


    cv2.imshow('lines',img)
    cv2.waitKey()

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
RectangleMatch(input_img = 'example/pic8.jpg')

#AreaMatch
#AreaMatch(input_img = 'example/pic8.jpg')

