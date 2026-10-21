import requests
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app=FastAPI()

api="https://open.bigmodel.cn/api/paas/v4/chat/completions"    #智谱的接口地址
with open("key.txt") as f:
    key=f.read().strip()    #从本地文件读key，不上传GitHub

class Ask(BaseModel):
    question:str

@app.get("/")
def home():
    return FileResponse("index.html")    #浏览器打开127.0.0.1:8000显示页面

@app.post("/ask")
def ask(a:Ask):
    df=pd.read_csv("csv_file/All_movies.csv")    #读文件电影数据
    top=df.sort_values("电影评分",ascending=False).head(10)    #取评分前10部
    ctx=top[["电影名称","电影评分","电影标签"]].to_string(index=False)    #拼成文本喂给模型
    prompt="下面是电影数据：\n"+ctx+"\n请根据这些数据回答："+a.question
    data={"model":"glm-4-flash","messages":[{"role":"user","content":prompt}]}
    r=requests.post(api,json=data,headers={"Authorization":"Bearer "+key})
    return {"answer":r.json()["choices"][0]["message"]["content"]}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
