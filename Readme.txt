组件识别模型Yolov5n
	功能：Img->Component分类及坐标
	数据集：（Part1）Vue+Python Python生成随机组件格式文本txt+数据集格式处理
			Vue读文本绘制到Canva截图
	              （Part2）MakeSense.ai手动标注图片
文字识别模型PaddleOcr
	功能：Img->文字坐标
	数据集：无，直接调用现有模型
颜色鉴别器 python/cv2库
	Python识别文字及背景像素颜色
功能整合
	Img->结构化文本
