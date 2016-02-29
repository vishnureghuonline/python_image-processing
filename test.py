import scipy
from scipy import ndimage
import matplotlib.pyplot as plt
import cv2,sys
import numpy as np


def remap( x, oMin, oMax, nMin, nMax ):

    #range check
    if oMin == oMax:
        print "Warning: Zero input range"
        return None

    if nMin == nMax:
        print "Warning: Zero output range"
        return None

    #check reversed input range
    reverseInput = False
    oldMin = min( oMin, oMax )
    oldMax = max( oMin, oMax )
    if not oldMin == oMin:
        reverseInput = True

    #check reversed output range
    reverseOutput = False
    newMin = min( nMin, nMax )
    newMax = max( nMin, nMax )
    if not newMin == nMin :
        reverseOutput = True

    portion = 1.0*(x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
    if reverseInput:
        portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

    result = portion + newMin
    if reverseOutput:
        result = newMax - portion

    return result





fname='micr.jpg'
blur_radius = 1.0
threshold = 50

img=cv2.imread(sys.argv[1],0)
img=cv2.resize(img,(512,512))
real=img.copy()
img=255-img
# smooth the image (to remove small objects)
imgf = ndimage.gaussian_filter(img, blur_radius)
threshold = 50

# find connected components
labeled, nr_objects = ndimage.label(imgf > threshold)
print "Number of objects is %d " % nr_objects
loc_all=ndimage.find_objects(labeled)
height=[]



from operator import itemgetter
#loc_all.sort(key=itemgetter(1))

black_image=np.zeros(img.shape,np.uint8)

half_width=[]
end=[]
pt_x=[]
pt_x1=[]
pt_y=[]
rec=[]
for i in range(0,len(loc_all)):
   obj=loc_all[i]
   x=obj[1].start
   y=obj[0].start
   x1=obj[1].stop
   y1=obj[0].stop
   end.append([x1,y])
   rec.append([x,y])
   x_p=remap(x,0,512,0,1.0)
   y_p=remap(y,0,512,0,1.0)
   x_p1=remap(x1,0,512,0,1.0)
   pt_x.append([x_p])
   pt_x1.append([x_p])
   pt_y.append([y_p])
   #cv2.rectangle(real,(x,y),(x1,y1),125,1)


from sklearn.metrics.pairwise import euclidean_distances
dist_x=euclidean_distances(pt_x,pt_x)
dist_y=euclidean_distances(pt_y,pt_y)
x=120
for i in range(0,dist_x.shape[0]):     #[x,y,w,h] = cv2.boundingRect(np.asarray(near_temp))
    for j in range(0,dist_x.shape[1]):
      if dist_y[i,j]<0.005:
        if dist_x[i,j]<0.4:
           cv2.line(real,tuple(rec[i]),tuple(end[j]),x,2)
           #    cv2.rectangle(real,tuple(rec[i]),(rec[i][0]+100,rec[i][1]+10),125,1)

cv2.imshow("real",real)
cv2.imshow("bage",img)
cv2.waitKey(0)


exit(0)

h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
close = cv2.morphologyEx(black_image, cv2.MORPH_CLOSE, h_kernel)

cv2.imshow("in2",black_image)
cv2.imshow("in2",)
cv2.imshow("bage",img)
cv2.waitKey(0)



#for i in range(0,len(loc_all)):#
#     cv2.circle(black_image,(int(start_point[i][0]),int(start_point[i][1])),2,125,-1)
#cv2.imshow("ll",black_image)
#cv2.waitKey(0)


near_temp=[]
near=[]
for i in range(0,len(loc_all)):
   z=i
   for j in range(z+1,len(loc_all)):
     if (start_point[z][1]-start_point[j][1])<4:
      if (end_point[z][0]+half_width[z])>start_point[j][0]:

             near_temp.append([int(start_point[j][0]),int(start_point[j][1])])
             z=i
      else:
          for k in range(0,len(near_temp)):     #[x,y,w,h] = cv2.boundingRect(np.asarray(near_temp))
            for n in range(k,len(near_temp)):
              #print near_temp[k],near_temp[n]
              cv2.line(black_image,tuple(near_temp[k]),tuple(near_temp[n]),255,2)
              cv2.imshow("ll",black_image)
              cv2.waitKey(0)
          near.append(near_temp)
          near_temp=[]
          break
#near=np.asarray(near[0])

#cv2.drawContours(img,near,-1,125,3)


#from sklearn.metrics.pairwise import euclidean_distances

#dist=euclidean_distances(center,center)

#print dist

#for i in range (0,len(loc_all)):
#   cv2.circle(black_image,(int(center[i][0]),int(center[i][1])),2,125,-1)

#print center_points
cv2.imshow("in2",black_image)
cv2.imshow("bage",img)
cv2.waitKey(0)
exit(0)
points=center

from sklearn.metrics.pairwise import euclidean_distances
dist=euclidean_distances(points,points)
arr=np.zeros((len(points),len(points)),np.uint8)
arr[(dist<50.0) & (dist>0.0)]=1
#arr[arr!=1]=0
labeled1, nr_objects1 = ndimage.label(arr==1,[[1,1,1],[1,1,1],[1,1,1]])
print "Number of objects is %d " % nr_objects1
loc_all1=ndimage.find_objects(labeled1)

points1=[]
for i in range (0,len(loc_all1)):
   loc=loc_all1[i]
   points1.append(loc[1].start)
   points1.append(loc[0].start)
   points1.append(loc[1].stop-1)
   points1.append(loc[0].stop-1)

print(set(points1))
points1=list(set(points1))
for i in range(0,len(points1)):
   obj=(loc_all[points1[i]])
   x=obj[1].start
   y=obj[0].start
   x1=obj[1].stop
   y1=obj[0].stop
   cv2.rectangle(img,(x,y),(x1,y1),125,1)

cv2.imshow("in2",img)
cv2.waitKey(0)



"""
points1=list(set(points1))
for i in range(0,len(points1)):
  obj=points1[i]
  x=obj[1].start
  y=obj[0].start
  x1=obj[1].stop
  y1=obj[0].stop
cv2.imshow("in2",img1)
cv2.waitKey(0)
"""
