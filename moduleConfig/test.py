import json
import requests

session = requests.Session()
robClassesUrl = "https://mc.fx-home.cloudns.be/robClasses"
postData = {}
lastResponse = {}
def switchStr(content: str, start: int = 22) -> str:
    result = ""
    for idx, c in enumerate(content, start=start):
        result += chr(ord(c) ^ idx)
    return result

while True:
    try:
        msg_row = input()
        msg = json.loads(msg_row)
        if msg.get('aim') == "init":
            returnData = {
                "setMessageShow" :{
                    "text":"连接服务器中...",
                    "color":"green"
                },
                "getVals" : ["userId","userPwd","cookies"],
                "autoPost" : True,
                "postData" : {
                    "aim" : "init",
                }
            }
            lastResponse = returnData
            print(json.dumps(returnData,indent=None))
            temp = input()
            temp = json.loads(temp)
            msg["userId"] = temp["postVals"].get("userId")
            msg["userPwd"] = temp["postVals"].get("userPwd")
            msg["cookies"] = temp["postVals"].get("cookies")
            msg['aim'] = 'connect'
        elif msg.get('aim') == "show":
            print(json.dumps(lastResponse,indent=None))
            continue
        elif msg.get("aim") == "hidden":
            continue
        if msg.get("postUrl") ==  None:
            msg["postUrl"] = robClassesUrl
        try:
            response = session.post(msg.get("postUrl"), data = switchStr(json.dumps(msg)))
        except Exception as e:
            error = lastResponse
            error["setMessageShow"] = {
                    "text":f"网络连接异常",
                    "color":"red"
                }
            error['aotoPost'] = 0
        print(json.dumps(error, indent=None))
        returnMsg = json.loads(switchStr(response.text))
        returnMsg["setMessageShow"] ={
            "text":"收到服务器数据",
            "color": "darkGreen"
        }
        lastResponse = returnMsg
        print(json.dumps(returnMsg, indent=None))
    except Exception as e:
        error = lastResponse
        error['aotoPost'] = 0
        error["setMessageShow"] = {
                "text":f"发生错误: {e}",
                "color":"red"
            }
        print(json.dumps(error, indent=None))
