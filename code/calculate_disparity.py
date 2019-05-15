import cv2
import numpy as np


def convert_gray(img):
    return ((0.3 * img[2]) + (0.59 * img[1]) + (0.11 * img[0])).astype(np.uint8)


def map_value(img):
    print np.min(img)
    return (((img - np.min(img)) / (np.max(img) - np.min(img))) * 255).astype(np.uint8)


def metric_SAD(block_l, block_r):
    return np.sum(np.absolute(block_l - block_r))


def metric_SSD(block_l, block_r):
    return np.sum(np.square(block_l - block_r))


def compute_epipolarline(img_l, img_r, win_size):
    pad_size = win_size / 2
    img_left = np.pad(img_l, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    img_right = np.pad(img_r, ((pad_size, pad_size), (pad_size, pad_size)), 'constant',
                       constant_values=((0, 0), (0, 0)))
    result = np.empty([img_l.shape[0], img_l.shape[1]])
    for i in range(0, img_l.shape[0]):
        print i
        for j in range(0, img_l.shape[1]):
            filter = img_left[i:i + win_size, j:j + win_size]
            filter_result = np.empty(img_l.shape[1])
            for k in range(0, img_l.shape[1]):
                filter_result[k] = metric_SAD(filter, img_right[i:i+win_size, k:k+win_size])
            result[i][j] = ((255/ (i+1)) * np.absolute(j - np.argmin(filter_result))).astype(np.uint8)

    return result


def compute_with_range(img_l, img_r, win_size, range_size):
    pad_size = win_size / 2
    img_left = np.pad(img_l, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    img_right = np.pad(img_r, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    result = np.empty([img_l.shape[0], img_l.shape[1]])
    print img_left.shape, img_right.shape
    for i in range(0, img_l.shape[0]):
        print i
        for j in range(0, img_l.shape[1]):
            # print "j: ", j
            filter = img_left[i:i+win_size, j:j+win_size]
            start = np.amax([0, j-range_size])
            best_SSD = 99999999
            best_x = start
            end = np.amin([img_l.shape[1], j+range_size])
            # end = np.amin([img_l.shape[1], start+range_size*2])
            #
            # print "start: ", start
            # print "end: ", end
            # filter_result = np.empty(end-start)
            for k in range(start, end):
                SSD = metric_SSD(filter, img_right[i:i + win_size, k:k + win_size])
                if SSD < best_SSD:
                    best_SSD = SSD
                    best_x = k
            result[i][j] = np.absolute(j - best_x)
            # print j, best_x, j - best_x, best_SSD

    return map_value(result)

def compute_with_block(img_l, img_r, win_size, range_size):
    pad_size = win_size / 2
    img_left = np.pad(img_l, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    img_right = np.pad(img_r, ((pad_size, pad_size), (pad_size, pad_size)), 'constant', constant_values=((0, 0), (0, 0)))
    result = np.empty([img_l.shape[0], img_l.shape[1]])
    print img_left.shape, img_right.shape
    for i in range(0, img_l.shape[0]):
        print i
        for j in range(0, img_l.shape[1]):
            filter = img_left[i:i+win_size, j:j+win_size]
            start = np.amax([0, j-range_size])
            starty = np.amax([0, i - range_size])
            best_SSD = 99999
            best_x = start
            end = np.amin([img_l.shape[1], j+range_size])
            endy = np.amin([img_l.shape[0], i + range_size])
            # filter_result = np.empty(end-start)
            for l in range(0, endy - starty):
                for k in range(0, end - start):
                    SSD = metric_SSD(filter, img_right[l+starty:l+starty + win_size, k+start:k+start + win_size])
                    if SSD < best_SSD:
                        best_SSD = SSD
                        best_x = k + start
            result[i][j] = np.absolute(j - best_x)

    return map_value(result)

if __name__ == "__main__":

    img_left = cv2.imread('pentagon_left.bmp')
    img_right = cv2.imread('pentagon_right.bmp')
    img_left = np.transpose(img_left, (2, 0, 1))
    print img_left.shape
    img_right = np.transpose(img_right, (2, 0, 1))
    img_dis = compute_with_range(img_left[0], img_right[0], 7, 4)
    cv2.imshow('gray', img_dis)
    cv2.imwrite('pen_4.png', img_dis)
    cv2.waitKey(0)
    cv2.destroyAllWindows()