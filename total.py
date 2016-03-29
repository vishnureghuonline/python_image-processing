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
           img[y:y1,x:x1]=im
           #im= cv2.pyrUp(im)
           pre_name="bill_process/"+str(y)+'.jpg'
           m=m+1
           cv2.imwrite(pre_name,im)

         if y>thresh/2:
           im=input_image[y:y1,x:x1]
           #img[y:y1,x:x1]=im
           pre_name="total_process/"+str(y)+"_"+str(x)+'.jpg'
           m=m+1
           cv2.imwrite(pre_name,im)

    cv2.imwrite("workingimages/corrected.jpg",img)
class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])

with suppress_stdout_stderr():
    im_nam=sys.argv[1]
    get_binary(im_nam)
    image=cv2.imread(im_nam)
    im=remove_noise('workingimages/0001.bin.png')
    cv2.imwrite("oo.jpg",im)
    process('oo.jpg')

    os.system('ocropus-dewarp top_process/*.jpg')
    os.system('ocropus-dewarp bill_process/*.jpg')
    os.system('ocropus-dewarp total_process/*.jpg')

    for pre_name in glob.glob('top_process/*.png'):
       os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")
    for pre_name in glob.glob('bill_process/*.png'):
       os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain -psm 3 1>/dev/null 2>&1")
    for pre_name in glob.glob('total_process/*.png'):
       os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")

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

    det_txt=open("workingimages/total_details.txt",'w')
    total_details=[]
    image_names=[]
    total_img=[]
    total_prob=[]
    query='Cash'
    for f in glob.glob('total_process/*.txt'):
        with open(f) as f_:
            content = f_.readlines()
            nameofpart=f.split('.')[0]+'.dew.png'
            total_img.append(nameofpart)
            total_details.append(''.join(content))
            total_prob.append(fuzz.partial_ratio(query,''.join(content)))
            if len(content)!=0:
                det_txt.write(''.join(content))



    """
    det_txt=open("workingimages/total_details.txt",'w')
    bill_details=[]
    bill_names=[]
    bill_img=[]
    bill_prob=[]
    query='bill no'
    for f in glob.glob('bill_process/*.txt'):
        with open(f) as f_:
            content = f_.readlines()
            nameofpart=f.split('.')[0]+'.dew.png'
            bill_img.append(nameofpart)
            bill_details.append(''.join(content))
            bill_prob.append(fuzz.partial_ratio(query,''.join(content)))
            if len(content)!=0:
                det_txt.write(''.join(content))
    """


    input_image=cv2.imread("workingimages/corrected.jpg")
    xy=total_img[np.argmax(total_prob)].split('/')[1].split('.')[0].split('_')
    x=int(xy[1])
    y=int(xy[0])
    total_part=input_image[y-50:y+50,input_image.shape[1]/2:input_image.shape[1]]
    cv2.imwrite("total.jpg",total_part)
    #xy=bill_img[np.argmax(bill_prob)].split('/')[1].split('.')[0].split('_')
    #x=int(xy[1])
    #y=int(xy[0])
    #bill_part=bill_image[y-50:y+50,0:input_image.shape[1]]
    #total_img_name=total_img[np.argmax(total_prob)]

    #cv2.imshow("oo",cv2.imread(total_img[np.argmax(total_prob)]))
    #cv2.imshow("lll",total_part)

    #cv2.imshow("ooa",cv2.imread(bill_img[np.argmax(bill_prob)]))
    #cv2.imshow("lb",bill_part)
    #cv2.waitKey(0)
    det_txt.close()

    os.system('rm -rf top_process/*.jpg top_process/*.png top_process/*.txt')
    os.system('rm -rf bill_process/*.jpg bill_process/*.png bill_process/*.txt')
    os.system('rm -rf total_process/*.jpg total_process/*.png total_process/*.txt')
    pt=get_parts('total.jpg')

    main_=cv2.imread("total.jpg")
    for i in range(0,len(pt)):
         x=pt[i][0]
         y=pt[i][1]
         x1=pt[i][0] + pt[i][2]
         y1= pt[i][1] + pt[i][3]
         im=main_[y:y1,x:x1]
         cv2.imwrite("total_process/"+str(x)+str(y)+".jpg",im)
         pre_name="total_process/"+str(x)+str(y)+".jpg"
         #print pre_name
         os.system("tesseract "+pre_name+" "+pre_name.split('.jpg')[0]+" -l engmain 1>/dev/null 2>&1")

    total=[]
    for f in glob.glob('total_process/*.txt'):
        with open(f) as f_:
          try:
              content=f_.readlines()
              #alp=re.sub('[^a-z,^A-Z,/,?,-,!,~,,,]','')
              if bool(re.match('[a-zA-Z]',content[0], re.IGNORECASE))==False:
                  m=re.sub('[^0-9,.]','',content[0])
                  total.append(float(m))
          except:
              continue
    print "Total:",np.max(total)
