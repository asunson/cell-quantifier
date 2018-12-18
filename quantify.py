# import necessary packages 
import numpy as np
import cv2
import os

"""
Define behavior for counting/removing additional cells
"""
def pickCells(event, x, y, flags, param):
    global numCells, numCells_copy, c_img, c_img_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # backup image and cell count before making changes
        c_img_copy = np.copy(c_img)
        numCells_copy = numCells
        
#         print("Adding Cell...")
        cv2.circle(c_img,(x,y), 6, (255,0,0), 1)
        numCells += 1

    if event == cv2.EVENT_RBUTTONDOWN:
        # backup image and cell count before making changes
        c_img_copy = np.copy(c_img)
        numCells_copy = numCells
    
#         print("Removing Cell...")
        # draw an x
        cv2.line(c_img, (x + 5, y + 5), (x - 5, y - 5), (0,0,255), 1)
        cv2.line(c_img, (x - 5, y + 5), (x + 5, y - 5), (0,0,255), 1)

        numCells -= 1

"""
Does nothing - feed to createTrackBar for onChange parameter
"""
def nothing(x): 
    pass

"""
Clear any existing window with name 'image' and attach mouse call back function 
and trackbars for threshold and area.  
"""
def remakeWindow(t, a, pickCells, name):
    cv2.destroyWindow(name)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(name, pickCells)
    cv2.createTrackbar("min Threshold", name, t, 100, nothing)
    cv2.createTrackbar("min Area", name, a, 200, nothing)

"""
Filter candidate cells by area (default 35 pixels). This value should be user defined based
on their prior knowledge of pixel -> real world measurement conversion. 
"""
def filterByArea(contours, min_area = 35):
    contours_area = [c for c in contours if cv2.contourArea(c) > min_area]
    return contours_area

"""
Discover cells with input threshold and minimum area
"""
def getContourImage(image, t, a):
    # remove background noise
    im_gauss = cv2.GaussianBlur(image, (3, 3), 0)
    
    ret, thresh = cv2.threshold(im_gauss, t, 255, 0)
    _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_area = filterByArea(contours, a)
    
    # initial number of cells is equal to number of contours discovered
    numCells = len(contours_area)
    numCells_copy = numCells # copy for undo purposes
    
    # draw contours on original image
    c_img = cv2.drawContours(cv2.cvtColor(image,cv2.COLOR_GRAY2RGB), 
                         contours_area, -1, (0, 255, 0), 1)
    c_img = cv2.resize(c_img, (0, 0), None, .9, .9)
    c_img_copy = np.copy(c_img) # copy for undo purposes
    
    return numCells, numCells_copy, c_img, c_img_copy

"""
Produces GUI to quantify cells from list of images. Returns cell count for each image and threshold used. 
Also saves a copy of each annotated/quantified image. 
"""
def quantifyCells(imgnames):
    global numCells, numCells_copy, c_img, c_img_copy
    
    images = [cv2.imread(img, cv2.IMREAD_GRAYSCALE) for img in imgnames]
    # collect list of image names without the path
    raw_imgnames = [s.split(os.sep)[-1] for s in imgnames]
    
    final_cell_counts = []
    thresholds = []
    
    for i in range(len(images)):
        image = images[i]    

        # initialize image to intial threshold and minimum area
        old_t = 40
        old_a = 35
        numCells, numCells_copy, c_img, c_img_copy = getContourImage(image, old_t, old_a)
        remakeWindow(old_t, old_a, pickCells, raw_imgnames[i])

        while(1):
            t = cv2.getTrackbarPos("min Threshold", raw_imgnames[i])
            a = cv2.getTrackbarPos("min Area", raw_imgnames[i])

            # if either trackbar position changes, update image and window with new values
            if t != old_t or a != old_a:
                numCells, numCells_copy, c_img, c_img_copy = getContourImage(image, t, a)
                # remakeWindow(t, a, pickCells)

            # update previous t and a
            old_t = t
            old_a = a

            # display image
            cv2.imshow(raw_imgnames[i], c_img)
            k = cv2.waitKey(200) & 0xFF
            if k == 13:
                # append number of cells to final list
                final_cell_counts.append(numCells)
                thresholds.append("Threshold " + str(t))

                # write final cell count onto image (could expand to a breakdown 
                # (additional/removed/original counts))
                cv2.putText(c_img, "Cell Count: " + str(numCells), (50,50), 
                            cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 0), 1)
                
                # find directory to save file in
                directory = os.path.join(imgnames[i][:-len(raw_imgnames[i])], "Cell Counts")

                # save annotated image
                cv2.imwrite(os.path.join(directory, raw_imgnames[i].split('.')[-2] + " cell count.jpg"), c_img)
                break

            # undo last change
            if k == ord('z'):
                c_img = np.copy(c_img_copy)
                numCells = numCells_copy

            # reset image and default values
            if k == ord('r'):
                cv2.setTrackbarPos("min Threshold", raw_imgnames[i], 40)
                cv2.setTrackbarPos("min Area", raw_imgnames[i], 35)
                numCells, numCells_copy, c_img, c_img_copy = getContourImage(image, t, a)
                
            # print values for debugging
            elif k == ord('a'):
                print("Current Threshold: ", t)
                print("Current min Area: ", a)
                print("Current Cell Count: ", numCells)

        cv2.destroyAllWindows()
        cv2.waitKey(1)
        print("Total number of Cells: ", numCells)
        
    return raw_imgnames, final_cell_counts, thresholds