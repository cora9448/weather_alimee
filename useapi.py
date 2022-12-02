from collections import defaultdict
from flask import Flask, render_template, request, jsonify
import time
import requests
import json
import sys

app = Flask(__name__)
nowhour = time
print(nowhour.localtime().tm_hour)
url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
params = {
    "serviceKey": "f+gnsss0lS5+jxASdEuTLtxTV1rfH3fuTJdySCRfhLnnwx8HXL6f78uTADFXU8IrxsvQyNR72jArPbC7pHigSw==",
    "pageNo": "1",
    "numOfRows": "1000",
    "dataType": "json",
    "base_date": "20221202",
    "base_time": "0600",
    "nx": "59",
    "ny": "73"
}


def dayapi():
    response = requests.get(url, params=params)
    diction = json.loads(response.text)
    print(diction)
    url_response = diction.get("response")
    url_body = url_response.get("body")
    url_items = url_body.get("items")
    url_item = url_items.get("item")

    result = {}
    dic_result = {}

    for x in url_item:
        result = x
        dic_result.setdefault(result.get("category"), result.get("obsrValue"))

    # dic_result["REH"],dic_result["T1H"],dic_result["WSD"]
    retval = {'습도': dic_result["REH"],
              '기온': dic_result["T1H"], '풍속': dic_result["WSD"]}
    return retval


@app.route("/", methods=['GET', 'POST'])
def index():
    value = dayapi()
    return render_template('index.html', value=value)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')
