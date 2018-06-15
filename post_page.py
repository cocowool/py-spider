# 发送POST请求
import urllib
import urllib.parse
import urllib.request

url = 'https://exam.kaoshixing.com/exam/exam_start_ing_multi'
values = {'examTestList':'[{"test_id":"5b139d0336098f5bf3dea261","test_ans":"key1,","exam_results_id":"6212338","exam_info_id":"132128"}]', 'timeStamp':'1529050572750'}

data = urllib.parse.urlencode(values)
data = data.encode('ascii')
req = urllib.request.urlopen(url, data)
with urllib.request.urlopen(req) as response:
    result = response.read()
    print(result)