from preprocess import *
import os,cv2,sys
import numpy as np
from utils.ocr_func import *
from utils.unifyBlocks import *
from difflib import SequenceMatcher
import glob
import shutil
from date_picker import *
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import sys

def process(f):
    #try:
     # os.makedirs('preprocess')
      #os.makedirs('preprocess/start')
      #os.makedirs('preprocess/end')
    #except:
      #shutil.rmtree('preprocess')

    #  os.makedirs('preprocess')
    #for f in glob.glob('billout/*.png'):
    utils_ = os.path.join(os.path.dirname(__file__),"utils")

    input_image=cv2.imread(f)

    temp=np.zeros(input_image.shape,np.uint8)
    temp[:]=255
    y_val=[]
    pt=get_parts(f)# c code
    for i in range(0,len(pt)):
      y_val.append(pt[i][1])
    start_y=np.max(y_val)
    end_y=np.min(y_val)
    thresh=start_y-end_y
    m=0
    img=np.zeros(input_image.shape,np.uint8)
    img[:]=[255,255,255]
    for i in range(0,len(pt)):
         x=pt[i][0]
         y=pt[i][1]
         x1=pt[i][0] + pt[i][2]
         y1= pt[i][1] + pt[i][3]
         if y<thresh/3:
           im=input_image[y:y1,x:x1]
           #img[y:y1,x:x1]=im
           pre_name="top_process/"+str(y)+'.jpg'
           #print im.shape
           m=m+1
           cv2.imwrite(pre_name,im)
         else:
           im=input_image[y:y1,x:x1]

           pre_name="end_process/"+str(y)+'.jpg'
           m=m+1
           cv2.imwrite(pre_name,im)

         if y>thresh/2:
           im=input_image[y:y1,x:x1]
           img[y:y1,x:x1]=im
           pre_name="total_process/"+str(y)+str(m)+'.jpg'
           m=m+1
           cv2.imwrite(pre_name,im)

           #os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+".txt"+" -l engmain nobanner")

       #else:
        #    im=input_image[y:y1,x:x1]
        #    pre_name="preprocess/end/"+str(m)+'.jpg'
        #    print im.shape
        #    m=m+1
    cv2.imwrite("workingimages/corrected.jpg",img)


im_nam=sys.argv[1]
get_binary(im_nam)
image=cv2.imread(im_nam)
im=remove_noise('workingimages/0001.bin.png')
cv2.imwrite("oo.jpg",im)
process('oo.jpg')

os.system('ocropus-dewarp top_process/*.jpg')
os.system('ocropus-dewarp end_process/*.jpg')
os.system('ocropus-dewarp total_process/*.jpg')
for pre_name in glob.glob('top_process/*.png'):
   os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")
for pre_name in glob.glob('end_process/*.png'):
   os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")
for pre_name in glob.glob('total_process/*.png'):
   os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")


#import json
#data={'aam admi':{'1':'Aaam Admi Pakwaan, Jawahar Nagar,Kamla Nagar,Delhi 110007'},'haldiram':{'2':'Haldiram product pvt ltd,6,l block,OuterCircle,Connaught place'}}
#with open('data.json', 'w') as outfile:#
#    json.dump(data, outfile)
#os.system("./ocropus-rp -m en-default.pyrnn.gz end_process/*.jpg -n")

try:
  with open("data.json") as json_file:
   data = json.load(json_file)
except:
  print "Cannot open the data json"

index_=[]
mer_name=[]
bill=[]
total=[]
for i in range(0,len(data)):
    index_.append(data[str(i)])
    mer_name.append(data[str(i)]['name'])
    bill.append(data[str(i)]['bill'])
    total.append(data[str(i)]['total'])

details=[]
image_names=[]
for f in glob.glob('top_process/*.txt'):
    with open(f) as f_:
        content = f_.readlines()

        details.append(content)
down_details=[]
for f in sorted(glob.glob('end_process/*.txt')):
    with open(f) as f_:
        content = f_.readlines()
        image_names.append(f.split('.txt')[0])
        down_details.append(content)




dist=[]
max_=0

for i in range(0,len(details)):
    for j in range(0,len(data)):
        s=data[str(j)]['name']
        if max_<fuzz.partial_ratio(s,details[i]):
            max_=fuzz.partial_ratio(s,details[i])
            name_=s
            prob=fuzz.partial_ratio(s,details[i])
            bill=data[str(j)]['bill']
            total=data[str(j)]['total']


max_=0
for i in range(0,len(down_details)):
    if max_<fuzz.partial_ratio(bill,down_details[i]):
            max_=fuzz.partial_ratio(bill,down_details[i])
            bill_no=down_details[i]
            y=int(image_names[i].split('.')[0].split('/')[1])
            #cv2.imwrite("end_process/part.jpeg",image[y-100:y+100,0:image.shape[1]])
            cv2.imwrite("end_process/bill.jpeg",cv2.imread(image_names[i]))

max_=0
for i in range(0,len(down_details)):
    if max_<fuzz.partial_ratio('cash',down_details[i]):
            max_=fuzz.partial_ratio('cash',down_details[i])
            total_str=down_details[i]
            y=int(image_names[i].split('.')[0].split('/')[1])
            try:
                img=cv2.imread("workingimages/corrected.jpg")

                cv2.imwrite("total_process/part.jpeg",img[y-100:y+100,0:img.shape[1]])
                cv2.imwrite("total_process/p.jpeg",cv2.imread(image_names[i]))
            except:
                print "error"
for i in range (0,len(details)):
    print details[i]
#os.system('rm -rf end_process/*.jpeg')
print "********************************************************************"

#print name_,total_str,bill_no
os.system('rm -rf top_process/*.jpg top_process/*.png top_process/*.txt')
os.system('rm -rf end_process/*.jpg end_process/*.png end_process/*.txt')
os.system('rm -rf total_process/*.jpg total_process/*.png total_process/*.txt')
"""
for pre_name in glob.glob("end_process/*.jpeg"):
   os.system("tesseract "+pre_name+" "+pre_name.split('.jpeg')[0]+" -l engmain 1>/dev/null 2>&1")

total=[]
for f in glob.glob('end_process/*.txt'):
    with open(f) as f_:
      try:
          content=f_.readlines()
          #alp=re.sub('[^a-z,^A-Z,/,?,-,!,~,,,]','')
          if bool(re.match('[a-zA-Z]',content[0], re.IGNORECASE))==False:
              m=re.sub('[^0-9,.]','',content[0])
              total.append(float(m))
      except:
          continue
for i in range(0,len(name_.split(','))):
    print name_.split(',')[i].strip()
try:
   print "Bill no:",re.sub('[^0-9,.]','',bill_no[0])
   print "Total:",np.max(total)
except:
   print "no found"
"""
#os.system('rm -rf end_process/*.jpeg end_process/*.txt')
