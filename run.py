from flask import Flask, jsonify, url_for, render_template, request, redirect
from werkzeug.utils import secure_filename
import glob
from IPython.display import Image, display, clear_output
import math
import io
from operator import truediv
import os
import json
from PIL import Image
import torch


app = Flask(__name__)
lines = []
eee = ''
path = './data'

RESULT_FOLDER = os.path.join('static')
app.config['RESULT_FOLDER'] = RESULT_FOLDER
# finds the model inside your directory automatically - works only if there is one model
def find_model():
    for f in os.listdir():
      if f.endswith(".pt"):
        return f
    print("please place a model file in this directory!")
    

model_name = find_model()
model =torch.hub.load("WongKinYiu/yolov7", 'custom',model_name)
model.eval()
def get_prediction(img_bytes):
    change_dir(path+'/')
    img = Image.open(io.BytesIO(img_bytes))
    imgs = [img]  # batched list of images
# Inference
    results = model(imgs, size=640)  # includes NMS
    return results

def change_dir(path):
    os.chdir(path)
#병 추출 함수
def defini(imsibun):
    result = '0'
    if imsibun == 1:
        result = '고추탄저병'
    elif imsibun == 2:
        result = '정상'
    elif imsibun == 3:
        result = '고추흰가루병'
    elif imsibun == 4:
        result = '꽃노랑총채벌레'
    elif imsibun == 5:
        result = '담배가루이'
    elif imsibun == 6:
        result = '담배거세미나방'
    elif imsibun == 7:
        result = '담배나방'
    elif imsibun == 8:
        result = '도둑나방'
    elif imsibun == 9:
        result = '배추흰나비'
    elif imsibun == 10:
        result = '복숭아혹진딧물'
    else:
      result = '열대거세미나방'
    return result
#확률 추출 함수
def avgg(imsibun2):
    ee3 = 0
    df2 = 0
    for i in range(imsibun2):
        e3=lines[ee3][38:45] # 확률 슬라이싱
        de= float(e3) #확률 str->float로 변환
        df= round(de, 2) #소숫점 둘째자리까지 반올림
        ee3 += 1
        df2 += df
    return df2
#지정된 사진 경로 판별 및 변경
def filenum(imsibun3):
    if imsibun3 == 1:
        change_dir('C:/Users/user/Desktop/content/runs/detect/exp')
    else:
        a=str(imsibun3)
        imsii = 'exp'+a
        change_dir('C:/Users/user/Desktop/content/runs/detect/'+imsii)
#spring에서 받은 파일을 로컬 서버에 저장
@app.route('/fileUpload', methods=['GET','POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    eee = f.filename
    
  
  f.save('./data/'+ secure_filename(f.filename))
  #eee = 'C:/Users/user/Desktop/testing/data/'+secure_filename(f.filename)
  return redirect(url_for('go_a', name = eee))

@app.route('/research', methods=['GET','POST'])
def go_a():
    eeee = request.args.get('name')
    print(eeee)
    file = eeee
    img_bytes = file.read()
    results = get_prediction(img_bytes)
    results.save(save_dir='static')
    
    return redirect('http://localhost:8085/ASNJ/Mainpage.do')

@app.route('/sendresult ', methods=['GET','POST'])
def upload_file2():
  if request.method == 'POST':
    f = request.files['file']
  test = os.listdir() 
  test #배열화해서 변수에 삽입
  
  picname= os.path.splitext(test[0])[0]
  
  return redirect("http://localhost:8085/ASNJ/Mainpage.do")

@app.route('/training', methods=['GET','POST'])
def learning():
  
  return ee
  
# 아직 사용 안함(다시 spring으로 되돌리기)
# @app.route('/fileUpload2', methods=['GET','POST'])
# def dddd():
#   if request.method == 'POST':
#         f2 = request.files['file']
#   ill = 내부 html에서 딥러닝 결과를 json이든 세션이든 저장
#   return redirect("http://localhost:8085/ASNJ/Mainpage.do?pre=ill")
if __name__ == '__main__':
  app.run(host="0.0.0.0", port=5050, debug=True)