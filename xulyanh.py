import cv2 as cv
import numpy as np
import urllib.request

def read_image_from_url(url):
    req = urllib.request.urlopen(url)
    img_rw = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv.imdecode(img_rw, cv.IMREAD_COLOR)
    return img

def add_noise(img):
    mean = 0
    sigma = 50
    noisy = np.random.normal(mean, sigma, img.shape)
    new_img = np.clip(img + noisy, 0, 255).astype(np.uint8)
    return new_img

def add_muoi_tieu(img, ratio=0.02):
    nosy_img = img.copy()
    muoitieu= int(ratio*img.size)
    
    #cho muoi vao
    toado = [np.random.randint(0, i-1, muoitieu) for i in img.shape]
    nosy_img[ toado[0], toado[1]] = 255
    #cho tieu vao
    toado = [np.random.randint(0, i-1, muoitieu) for i in img.shape]
    nosy_img[ toado[0], toado[1]] = 0

    return nosy_img

if __name__ == "__main__":

    img = cv.imread("giaothong.jpg", cv.IMREAD_COLOR)
    img2 = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    clean_img = cv.medianBlur(img2,5)
    cv.imshow("clean_img", clean_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
       
    edge = cv.Canny(clean_img, 50, 150)
    cv.imshow("edge", edge)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    h,w = edge.shape
    mask = np.zeros_like(edge)
    polygon = np.array([
    [0, h],
    [w, h],
    [int(w*0.6), int(h*0.6)],
    [int(w*0.4), int(h*0.6)]
], dtype=np.int32)

    cv.fillPoly(mask, [polygon], 255)
    roi = cv.bitwise_and(edge, mask)
    cv.imshow("roi", roi)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    
   

    
    lines = cv.HoughLinesP(
        roi,
        rho=1.0,
        theta=np.pi / 180,
        threshold=100,
        minLineLength=100,
        maxLineGap=100
    )
    img_lines = clean_img.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv.line(img_lines, (x1, y1), (x2, y2), (0, 0, 255), 1)
    cv.imshow("img_lines", img_lines)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # print(w,h)
    # n_img = edge[w//2-100:w//2+100, h//2-100:h//2+100]
    # cv.imshow("n_img", n_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # cv.imshow("img", img2)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # # url = "https://raw.githubusercontent.com/udacity/CarND-LaneLines-P1/master/test_images/solidWhiteCurve.jpg"
    # # img = read_image_from_url(url)
    # img = cv.imread("giaothong.jpg")
    # cv.imshow("img", img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # clean_img = cv.medianBlur(img,5)
    # cv.imshow("clean_img", clean_img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # edge = cv.Canny(clean_img, 50, 150)
    # cv.imshow("edge", edge)
    # cv.waitKey(0)   
    # cv.destroyAllWindows()
    
   
    

    # url = "https://raw.githubusercontent.com/udacity/CarND-LaneLines-P1/master/test_images/solidWhiteCurve.jpg"
    # img = read_image_from_url(url)
    # n = add_noise(img)
    # cv.imshow("img", img)
    # cv.waitKey(0)
# cv.destroyAllWindows()
    
    # img2 = np.clip(img + n, 0, 255).astype(np.uint8)
    # cv.imshow("img2", img2)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    # img2 = add_noise(img)
    # cv.imshow("img2", img2)
    # cv.waitKey(0)   
    # cv.destroyAllWindows()
    
    # img3 = np.concatenate((img, img2), axis=1)
    # cv.imshow("img3", img3)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # img4 = add_muoi_tieu(img,0.01)
    # cv.imshow("img4", img4)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # anh_muoi_tieu = add_muoi_tieu(img, ratio=0.02)
    # img2 = anh_muoi_tieu.copy()
    # clean_img = cv.Blur(img2,(3,3)) #làm sạch ảnh
    # img3 = np.concatenate((anh_muoi_tieu, clean_img, img), axis=1)
    # cv.imshow("img3", img3)
    # cv.waitKey(0)
    # cv.destroyAllWindows() 
    
    
    # anh_muoi_tieu = add_muoi_tieu(img, ratio=0.02)
    # img2 = anh_muoi_tieu.copy()
    # clean_img = cv.medianBlur(img2,5) #làm sạch ảnh thứ 2
    # img3 = np.concatenate((anh_muoi_tieu, clean_img, img), axis=1)
    # cv.imshow("img3", img3)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    
    # ed1 = cv.Canny(anh_muoi_tieu, 50, 150)
    # ed2 = cv.Canny(clean_img, 50, 150) 
    # ed3 = cv.Canny(img, 50, 150)
    # img4 = np.concatenate((ed1, ed2, ed3), axis=1)
    # cv.imshow("img4", img4)
    # cv.waitKey(0)
    # cv.destroyAllWindows()