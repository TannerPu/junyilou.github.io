#-*- coding:utf-8 -*-
import os, time, datetime, urllib2, sys, json

filename = ['nanjingeast', 'kunming', 'wangfujing', 'taikoolichengdu', 'riverside66tianjin',
			'parc66jinan', 'mixcqingdao', 'parccentral', 'holidayplazashenzhen', 'mixcnanning',
			'nanjingist', 'center66wuxi', 'mixczhengzhou', 'westlake', 'xiamenlifestylecenter',
			'thaihotplaza', 'olympia66dalian', 'zhongjiejoycity', 'jiefangbei', 'ifcmall', 'galaxymacau', 'taipei101']
cityname = ['上海', '昆明', '北京', '成都', '天津', '济南', '青岛', '广州', '深圳', '南宁', '南京', '无锡',
			'郑州', '杭州', '厦门', '福州', '大连', '沈阳', '重庆', '香港特别行政区', '澳门特别行政区', '台湾']
checksum = list(range(len(cityname)))
for c in range(0, len(cityname)): checksum[c] = 0

def home():
	wAns = ""; wCount = 0; nowDatetime = datetime.datetime.now(); rpath = os.path.expanduser('~') + "/Retail/"
	os.system("rm " + rpath + "*.json"); os.system("wget -t 0 -T 3 -P " + rpath + " --no-check-certificate -i " + rpath + "url.md"); os.system("clear")
	print nowDatetime.strftime("%Y-%m-%d %H:%M:%S") + " 的检查结果:"
	for i in range(0, len(filename)):
		r = open(rpath + filename[i] + ".json"); raw = r.read(); r.close(); rJson = json.loads(raw)["courses"]
		for lct in range(0, len(rJson)):
			tlans = rJson[lct]["talent"]
			if len(tlans) > 0:
				singleID = rJson[lct]["id"]
				fb = open(rpath + "Event.md"); fcb = fb.read(); fb.close(); nCheck = fcb.count(singleID)
				reload(sys); sys.setdefaultencoding('utf-8')
				pushAns = "Apple 在" + cityname[i] + "有新活动 " + rJson[lct]["shortName"]
				singleURL = rJson[lct]["image"]; print pushAns
				if nCheck == 0:
					os.system('curl -X POST -H "Content-Type: application/json" -d' + "'" + '{"value1":"' + pushAns
							   + '", "value2":"' + singleURL + '"}' + "' https://maker.ifttt.com/trigger/today/with/key/dJ4B3uIsxyedsXeQKk_D3x"); print
				# GitHub users please notice: IFTTT Key only uses for private.
				wAns = wAns + singleID + ", "; wCount += 1; checksum[i] += 1
	if wCount > 0:
		fc = open(rpath + "Event.md", "w")
		fc.write(wAns); fc.close()
	for j in range(0, 22):
		if checksum[j] == 0: print "Apple 在" + cityname[j] + "没有新活动"

while True:
	home(); os.system("rm " + os.path.expanduser('~') + "/Retail/*.json")
	os.system("cp /home/pi/junyilou.github.io/states.json /home/pi/Retail/") #与 Jobs_IFTTT.py 冲突
	print "今天的刷新检测已经完成，Python 将休眠 24 小时。"; time.sleep(3600*24)