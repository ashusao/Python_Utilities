r"""Image normalization utils."""

import cv2
import numpy as np

def Normalized_Value_Histogram_Equalization(amp):
  amp_255 = ((amp/amp.max())*255).astype(np.uint8)
  equalized_image = cv2.equalizeHist(amp_255)
  return equalized_image

def Clahe_normalization(amp):
  amp_255 = ((amp/amp.max())*255).astype(np.uint8)
  clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  equalized_image = clahe.apply(amp_255)
  return equalized_image

def Zero_Max_Normalization(amp):
  amp_255 = ((amp/amp.max())*255).astype(np.uint8)
  return amp_255

def Original_Value_Histogram_Equalization(amp):
  hist,  = np.histogram(amp.flatten(),int(amp.max())+1)
  cdf = hist.cumsum()
  cdf_m = np.ma.masked_equalized_imageal(cdf,0)
  cdf_m = (cdf_m - cdf_m.min())*(int(amp.max()))/(cdf_m.max()-cdf_m.min())
  cdf = np.ma.filled(cdf_m,0)
  equalized_image = cdf[(amp).astype(int)]
  equalized_image = ((equalized_image/amp.max())*255).astype(np.uint8)
  return equalized_image

# Positive Global Standardization, from the book "Deep Learning for Computer Vision Image Classification, Object Detection, and Face Recognition in Python" MACHINE LEARNING MASTERY, the blog "How to Manually Scale Image Pixel Data for Deep Learning"
# 2.56 : Z(2.56)-Z(-2.56) = 0.99 => theoretically: if the distribution of the data is a normal distribution 99% of the values are between -2.56 and 2.56
def Clipped_Mean_Std_Normalization(amp, clip_at = 2.56):
  mean = amp.mean()
  std = amp.std()
  standardized_amp = (amp-mean)/std
  clipped_standardized_amp = np.clip(standardized_amp,-clip_at,clip_at)
  normalized_amp = ((clipped_standardized_amp+clip_at)*255/(2*clip_at)).astype(np.uint8)
  return normalized_amp

# use full image value range  
def Asymmetric_clipped_Mean_Std_Normalization(amp, clip_at = 2.56):
  mean = amp.mean()
  std = amp.std()
  standardized_amp = (amp-mean)/std
  clipped_standardized_amp = np.clip(standardized_amp,-clip_at,clip_at)
  min_val = clipped_standardized_amp.min()
  max_val = clipped_standardized_amp.max()
  normalized_amp = ((clipped_standardized_amp-min_val)*255/(max_val-min_val)).astype(np.uint8)
  return normalized_amp

# idea from: https://medium.com/@TheDataGyan/day-8-data-transformation-skewness-normalization-and-much-more-4c144d370e55
def Cube_root_Transformation(amp, clip_at = 2.56, use_asymmetric = True):
  amp = np.cbrt(amp-amp.min())
  if use_asymmetric:
    normalized_amp = Asymmetric_clipped_Mean_Std_Normalization(amp, clip_at)
  else:
    normalized_amp = Clipped_Mean_Std_Normalization(amp, clip_at)
  return normalized_amp

def Square_root_Transformation(amp, clip_at = 2.56, use_asymmetric = True):
  amp = np.sqrt(amp-amp.min())
  if use_asymmetric:
    normalized_amp = Asymmetric_clipped_Mean_Std_Normalization(amp, clip_at)
  else:
    normalized_amp = Clipped_Mean_Std_Normalization(amp, clip_at)
  return normalized_amp

def Log_Transformation(amp, clip_at = 2.56, use_asymmetric = True):
  amp_m = np.ma.log(amp-amp.min())
  amp = np.ma.filled(amp_m,0)
  if use_asymmetric:
    normalized_amp = Asymmetric_clipped_Mean_Std_Normalization(amp, clip_at)
  else:
    normalized_amp = Clipped_Mean_Std_Normalization(amp, clip_at)
  return normalized_amp