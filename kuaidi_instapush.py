# -*- coding:utf-8 -*-
import sys, json, urllib2, time, datetime, os, fileinput, signal
arg = signCheck = siging = 0; brew = 4; sm = ""; argv = list(range(15))

binvar = "" # Signal Part
def user1(a,b):
	global binvar; binvar += "0"
signal.signal(signal.SIGUSR1,user1)
def user2(a,b):
	global binvar; binvar += "1"
signal.signal(signal.SIGUSR2,user2)
def sig_start(a,b):
	global siging; siging = 1
	print 'Received Linux siganal, analyzing.'
	global binvar; binvar = ""
signal.signal(signal.SIGCONT,sig_start)
def sig_end(a,b): 
	sigans = int(binvar,2)
	print "Received new readid:", sigans
	global siging, arg; siging = 0
	arg += 1; argv[arg] = str(sigans)
signal.signal(signal.SIGTERM,sig_end)

def blanker(bid, notice):
	blanktime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print str(os.getpid()) + " " + blanktime + " Checked " + bid + " " + notice + ", ignore."
def pytry(tryurl):
	try:
		response = urllib2.urlopen(tryurl)
	except urllib2.URLError as err:
		if hasattr(err, 'reason') or hasattr(err, 'code'): return "False"
	else:
		return response.read()
def home(readid):
	exsc = False; es = ""
	if readid != "":
		idt = FileLocation + '/' + readid + ".txt"; exi = os.path.isfile(idt)
		if exi:
			for line in fileinput.input(idt):
				orgCounter = int(line)
			fileinput.close()
		else:
			createFile = open(idt, 'w')
			createFile.write("0")
			createFile.close()
			orgCounter = 0
		urla = "https://www.kuaidi100.com/autonumber/autoComNum?text=" + readid; trya = pytry(urla)
		if trya != "False":
			countp = trya.count("comCode")
		else:
			countp = 1
		if (countp - 1):
			comp = json.loads(urllib2.urlopen(urla).read())["auto"][0]["comCode"]
			urlb = "https://www.kuaidi100.com/query?type=" + comp + "&postid=" + readid; tryb = pytry(urlb)
			if tryb != "False":
				anst = tryb; ansj = json.loads(anst)
				today = datetime.datetime.now().strftime("%m月%d日")
				comtext = {'yuantong': '圆通', 'yunda': '韵达', 'shunfeng': '顺丰', 'shentong': '申通', 'zhongtong': '中通', 'jd': '京东'}
				if ansj["status"] == "200":
					erstat = 1
					maxnum = anst.count("location")
					if maxnum != orgCounter:
						result = ansj["data"]
						realComp = comtext.get(ansj["com"], "其他") + "快递"
						fTime = time.strftime("%m月%d日 %H:%M", time.strptime(result[0]["time"], "%Y-%m-%d %H:%M:%S"))
						reload(sys); sys.setdefaultencoding('utf-8')
						fContent = result[0]["context"].replace(" 【", "【").replace("】 ", "】")
						signCount = fContent.count("签收") + fContent.count("感谢")
						sendCount = fContent.count("派送") + fContent.count("派件") + fContent.count("准备")
						if signCount > 0 and sendCount < 1:
							es = "[签收] "
							exsc = maxnum
						fileRefresh = open(idt, 'w')
						fileRefresh.write(str(maxnum))
						fileRefresh.close()
						a='curl -X POST -H "x-instapush-appid: '; b='" -H "x-instapush-appsecret: '
						c='" -H "Content-Type: application/json" -d '; d="'"
						e='{"event":"kuaidi","trackers":{"rc":"'; f=realComp
						g='","ri":"'; h=readid; i='","ft":"'; j=fTime; k='","fc":"'
						l=fContent; m='"}'; n='}'; o="'"; p=' https://api.instapush.im/v1/post'
						finalOut = a+AppID+b+AppSecret+c+d+e+es+f+g+h+i+j+k+l+m+n+o+p
						os.system(finalOut); print
					else:
						blanker(readid, "has no update")
				else:
					blanker(readid, "returned code " + ansj["status"])
			else:
				blanker(readid, "has HTTP-Connect error")
		else:
			blanker(readid, "returned no auto-company")
	else:
		blanker("this package", "probably signed")
	return exsc
for m in sys.argv[1:]: arg += 1
AppID = sys.argv[1]
AppSecret = sys.argv[2]
TimeInterval = int(sys.argv[3])*60
if TimeInterval < 30: TimeInterval = 30
FileLocation = sys.argv[4]
for n in range (1,arg + 1):
	argv[n] = sys.argv[n]
print "Start with PID " + str(os.getpid()) + ". Time interval will be " + sys.argv[3] + " minutes."
while True:
	if not siging:
		for n in range(5, arg + 1):
			readid = argv[n]
			sm = sm + "[" + str(n-4) + "] " + readid + " "
			stat = home(readid)
			if stat:
				argv[n] = ""
				print "Checked " + str(readid) + " signed and emptied, " + str(stat) + " updates in total recorded."
				os.system("rm " + FileLocation + '/' + readid + ".txt")
				brew += 1
		time.sleep(TimeInterval)
	if brew == arg: break
nt = "============================================="
st = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print "\nSummary:\n" + nt + "\n" + "readid List: " + sm + "\n" + st + " All " + str(brew-4) + " packages signed, exit.\n" + nt