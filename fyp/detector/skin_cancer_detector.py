import numpy as np
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from tensorflow import keras
from .gradcam import make_gradcam_heatmap,save_and_display_gradcam



model_path = '../final_model/main_model.h5'
vis_model_path = '../final_model/vis_model.h5'
def load():
    
    pass

def prediction(img_path:str):
    classes=['nv','mel','bkl', 'bcc', 'akiec', 'vasc', 'df']
    img_size = (299, 299)
    
    
    cmodel = tf.keras.models.load_model(model_path, compile=True)
    model = tf.keras.models.load_model(vis_model_path)


    preprocess_input = keras.applications.inception_resnet_v2.preprocess_input
    last_conv_layer_name = "conv_7b"


    #img_path = #"drive/MyDrive/Cancer Model/val_dir/vasc/ISIC_0026490.jpg"
    
    image = tf.keras.preprocessing.image.load_img(img_path)
    
    input_arr = keras.preprocessing.image.img_to_array(image, dtype='float32')
    input_arr = preprocess_input(input_arr)
    input_arr = tf.keras.preprocessing.image.smart_resize(input_arr, size=img_size)
    

    #print(input_arr.shape)
    acc= cmodel.predict(np.array([input_arr]))
    n = np.argmax(acc)
    #print(classes[n])
    #Image(img_path)


    print("Predicted:", classes[n])
    model.layers[-1].activation = None
    # Generate class activation heatmap
    input_arr = np.expand_dims(input_arr, axis=0)
    heatmap = make_gradcam_heatmap(input_arr, model, last_conv_layer_name)
    img_path = save_and_display_gradcam(img_path, heatmap,cam_path=img_path)

    fullform = {
        'akiec' : "Actinic keratoses and intraepithelial carcinoma / Bowen's disease",
        'bcc':'basal cell carcinoma' ,
        'bkl':'benign keratosis-like lesions' ,
        'df': 'dermatofibroma', 
        "mel" : "melanoma" ,
        "nv" : "melanocytic nevi",
        "vasc" : "vascular lesions"
        } 
    
    return { 
        'acc': np.ndarray.max(acc),
        'class': fullform[classes[n]],
        'vis_path': img_path
        }
