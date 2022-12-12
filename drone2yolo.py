import os
from PIL import Image

drone_texts_path = "Annotations"  # 原有 annotations的保存路径
drone_images_path = "Images"  # 图片的保存路径
yolo_txt_path = "yolo_lable"  #转换后图片txt的保存路径

drone_txts = os.listdir(drone_texts_path)



def drone2yolo(line):
    label = line[:-3].split(",")
    top_left  =  (int(label[0]),int(label[1])+int(label[3]))
    bot_right =  (top_left[0] + int(label[2]) , top_left[1]-int(label[3]))
    category = label[5]
    return top_left,bot_right,category

# 写入每一个文件 需要对坐标点进行归一化处理 x/w y/h
def write_yolo(img_path,file,top_left,bot_right,category):
    # os.makedirs("yolo_lable")
    # img = cv2.imread(img_path)
    # h,w,c = img.shape
    img = Image.open(img_path)
    w,h = img.size
    f = open(file,'a')
    f.write(category)
    f.write(" ")
    # 保留小数点后六位
    x_center = round((top_left[0] + 0.5*abs(top_left[0]-bot_right[0]))/w,6)
    y_center = round((top_left[1] - 0.5*abs(top_left[1]-bot_right[1]))/h,6)
    w_b =round( abs(top_left[0]-bot_right[0]) /w,6)
    h_b =round(abs(top_left[1]-bot_right[1]) /h,6)
    f.write(str(x_center))
    f.write(" ")
    f.write(str(y_center))
    f.write(" ")
    f.write(str(w_b))
    f.write(" ")
    f.write(str(h_b))

    f.write("\n")


# 写入文件
a = 0
try:
    for txt in drone_txts:
        for line in open(os.path.join(drone_texts_path,txt)).readlines():
            top_left, bot_right, category = drone2yolo(line)
            txt_path = os.path.join(yolo_txt_path,txt)

            img_path = os.path.join(drone_images_path,txt[:-3] + "jpg")
            write_yolo(img_path,txt_path,top_left,bot_right,category)
        print("正在写入第{:}个文件".format(a))
        a+=1
except:
    print("error")





