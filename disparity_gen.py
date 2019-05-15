import numpy as np
import cv2
import time


def ssd(left, right):
    return -np.sum(np.square(left - right))


def sad(left, right):
    return -np.sum(np.absolute(left - right))


def ncc(left, right):
    avg_l = np.average(left)
    avg_r = np.average(right)
    top = np.sum((left - avg_l) * (right - avg_r))
    bottom = np.sqrt(np.sum(np.square(left - avg_l) * np.square(right - avg_r)))
    return top / bottom


def grab_window(img, col, row, size, scale):
    width = scale * size
    return img[row:row+size, col:col+width]


def disp(img_l, img_r, scan_size, scale):
    max_row = img_l.shape[0] - scan_size
    max_col = img_l.shape[1] - scan_size
    result = np.empty([img_l.shape[0], img_l.shape[1]])
    for row in range(0, max_row):
        print row
        for col in range(0, max_col):
            wl = grab_window(img_l, col, row, scan_size, 1)
            wr_width = scan_size * scale
            wr_large_x = col - (scan_size * (scale/2) - (scan_size/2))
            wr_large_y = row
            wr_large_x = np.amin([np.amax([wr_large_x, 0]), (img_r.shape[1] - wr_width)])
            wr_large_y = np.amin([np.amax([wr_large_y, 0]), (img_r.shape[0] - wr_width)])
            wr_large = grab_window(img_r, wr_large_x, wr_large_y, scan_size, scale)
            match_x = 1
            max_disp = -999999
            arr_width = (scale * scan_size) - scan_size + 1
            x_mid = (arr_width/2)
            for y in range(0, wr_large.shape[0] - scan_size + 1):
                for x in range(0, wr_large.shape[1] - scan_size + 1):
                    sub_win = grab_window(wr_large, x, y, scan_size, 1)
                    disp = ssd(wl, sub_win)
                    if disp > max_disp:
                        max_disp = disp
                        match_x = x
            x = x_mid - match_x
            result[row][col] = (255 /x_mid) * np.abs(x)
            # print col, match_x, x_mid - match_x, max_disp
    return result.astype(np.uint8)

if __name__ == "__main__":
    img_left = cv2.imread('pentagon_left.bmp')
    img_right = cv2.imread('pentagon_right.bmp')
    img_left = np.transpose(img_left, (2, 0, 1))
    print img_left.shape
    img_right = np.transpose(img_right, (2, 0, 1))
    start = time.time()
    img_dis = disp(img_left[0], img_right[0], 9, 3)
    end = time.time()
    print end - start
    cv2.imshow('gray', img_dis)
    cv2.imwrite('pen_ssd_9.png', img_dis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

