import os
import sys
import glob
import requests
from PIL import Image
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, 
	QToolTip, QAction, qApp, QDesktopWidget, QHBoxLayout, QVBoxLayout, QGridLayout, 
	QLabel, QInputDialog, QMessageBox, QFileDialog, QDialog, QProgressBar)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon

class Gui(QMainWindow):

	canceledown = pyqtSignal()

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		exitAction = QAction(QIcon('images/exit.png'), '나가기', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('나갈 수 있습니다.')
		exitAction.triggered.connect(qApp.quit)

		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)
		filemenu = menubar.addMenu('&파일')
		filemenu.addAction(exitAction)

		self.dialog = QDialog()
		self.bar = QProgressBar(self.dialog)

		self.setWindowTitle('네이버 웹툰 다운로더')
		self.statusBar().showMessage('준비')
		self.setWindowIcon(QIcon('images/dl.png'))
		self.resize(300, 500)
		self.center()
		self.text()
		self.show()

	def PB_dialogue(self):
		self.bar.setGeometry(10, 10, 200, 30)
		self.bar.setValue(0)
		self.bar.setAlignment(Qt.AlignCenter)
		self.bar.resetFormat()

		btn = QPushButton('취소하기', self.dialog)
		btn.move(70, 50)
		btn.clicked.connect(self.canceleddown)

		self.dialog.setWindowIcon(QIcon('images/dl.png'))
		self.dialog.setWindowTitle('진행률')
		self.dialog.setWindowModality(Qt.ApplicationModal)
		self.dialog.resize(220, 80)
		self.center()
		self.dialog.show()

	def canceleddown(self):
		self.canceledown.emit()

	def canceled(self):
		QMessageBox.question(self, '안내창', '취소되었습니다.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def diacanceled(self):
		self.dialog.reject()
		QMessageBox.question(self, '안내창', '취소되었습니다.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def Noned(self):
		QMessageBox.question(self, '안내창', '유효한 값을 입력해주세요.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def titleidDialogue(self):
		self.btn1.setEnabled(False)
		self.btn2.setEnabled(False)
		self.btn3.setEnabled(False)
		text, ok = QInputDialog.getInt(self, 'titleId 입력창', 'titleId를 입력해주세요:')

		if ok:
			if text == 0:
				self.Noned()
				return
			self.titleId = text
			self.StartnoDialogue()
		else:
			self.canceled()

	def StartnoDialogue(self):
		text, ok = QInputDialog.getInt(self, 'Starno 입력창', '시작 번호를 입력해주세요:')

		if ok:
			if text == 0:
				self.Noned()
				return
			self.startno = text
			self.EndnoDialogue()
		else:
			self.canceled()

	def EndnoDialogue(self):
		text, ok = QInputDialog.getInt(self, 'Endno 입력창', '끝 번호를 입력해주세요:')

		if ok:
			if text == 0:
				self.Noned()
				return
			self.endno = text
			self.FileDialogue()
		else:
			self.canceled()

	def FileDialogue(self):
		QMessageBox.question(self, '안내창', '다운로드 할 폴더를 지정해주세요.', QMessageBox.Yes)
		fname = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), './', QFileDialog.ShowDirsOnly)
		if len(fname) == 0:
			self.canceled()
		else:
			self.path = fname
			self.DownloadWebtoon()

	def DownloadWebtoon(self):
		thread = Downloader(self,self.startno,self.endno,self.titleId,self.path)
		thread.downdone.connect(self.downdone)
		thread.canceldone.connect(self.diacanceled)
		thread.bar.connect(self.barc)

		self.canceledown.connect(thread.cancel)
		self.PB_dialogue()
		thread.start()

	def barc(self,value):
		self.bar.setValue(value)

	def downdone(self):
		QMessageBox.question(self, '안내창', '다운로드가 완료되었습니다.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def Htmler(self):
		self.btn1.setEnabled(False)
		self.btn2.setEnabled(False)
		self.btn3.setEnabled(False)
		QMessageBox.question(self, '안내창', '웹툰 사진들이 있는 폴더를 지정해주세요.', QMessageBox.Yes)
		datapath = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), './', QFileDialog.ShowDirsOnly)
		if len(datapath) == 0:
			self.canceled()
		else:
			thread = Htmler(self,datapath)
			thread.htmlerdone.connect(self.htmlerdone)
			thread.start()

	def htmlerdone(self):
		QMessageBox.question(self, '안내창', '변환이 완료되었습니다.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def imageMerger(self):
		self.btn1.setEnabled(False)
		self.btn2.setEnabled(False)
		self.btn3.setEnabled(False)
		QMessageBox.question(self, '안내창', '웹툰 사진들이 있는 폴더를 지정해주세요.', QMessageBox.Yes)
		datapath = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), './', QFileDialog.ShowDirsOnly)
		if len(datapath) == 0:
			self.canceled()
		else:
			thread = Merger(self,datapath)
			thread.syntheticdone.connect(self.syntheticdone)
			thread.start()

	def syntheticdone(self):
		QMessageBox.question(self, '안내창', '사진 이어붙이기가 완료되었습니다.', QMessageBox.Yes)
		self.btn1.setEnabled(True)
		self.btn2.setEnabled(True)
		self.btn3.setEnabled(True)

	def text(self):
		widget = QWidget()
		layout = QGridLayout()

		self.l1 = QLabel('네이버 웹툰 다운로더'); self.l1.setStyleSheet("font-size: 35px;")
		self.btn1 = QPushButton('웹툰 다운로드 하기', self)
		self.btn2 = QPushButton('웹툰 사진 이어붙이기', self)
		self.btn3 = QPushButton('웹툰 사진 html로', self)
		self.btn1.clicked.connect(self.titleidDialogue)
		self.btn2.clicked.connect(self.imageMerger)
		self.btn3.clicked.connect(self.Htmler)

		layout.addWidget(self.l1,0,0)
		layout.addWidget(self.btn1,1,0)
		layout.addWidget(self.btn2,2,0)
		layout.addWidget(self.btn3,3,0)

		widget.setLayout(layout)
		self.setCentralWidget(widget)

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

class Htmler(QThread):

	htmlerdone = pyqtSignal()

	def __init__(self,parent,datapath):
		super().__init__(parent)
		self.parent = parent
		self.datapath = datapath

	def run(self):
		files = glob.glob(self.datapath + '/*.png')
	
		gar = {}
		name_list = []
	
		for f in files:
			name = f.split('\\')[1]
			value = name.split('.')[0]
	
			if value in gar.keys():
				gar[value].append(name)
			else:
				gar[value] = [name]
	
			gar[value].sort()
	
		for n in gar:
			self.parent.statusBar().showMessage('%s.png 얻는중..' % n)
			name_list.append(n)
		del gar
	
		basename = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
	
		for i in name_list:
			f = open(self.datapath + '/' + i + '.html', 'w')
			self.parent.statusBar().showMessage('%s.html 출력중..' % i)
			self.WriteMain(f,basename,i,name_list)
			f.close()
		self.htmlerdone.emit()
		self.parent.statusBar().showMessage('준비')

	def W(self,O,M):
		O.write(M)

	def WH(self,O,name,list):
		self.W(O,'<p align=left style="float: left;">')
		backs = self.MakeItFour(str(int(name)-1))
		if backs in list:
			self.W(O,'<a href="%s.html">이전화</a>' % backs)
		else:
			self.W(O,'''<a href="void(0);" onclick="alert('최초화입니다.');return false;">이전화</a>''')
		self.W(O,'</p>\n<p align=right style="float: right;">\n')
		nexts = self.MakeItFour(str(int(name)+1))
		if nexts in list:
			self.W(O,'<a href="%s.html">다음화</a>' % nexts)
		else:
			self.W(O,'''<a href="void(0);" onclick="alert('마지막화입니다.');return false;">다음화</a>''')
		self.W(O,'</p>')
		self.W(O,'''</p>
	<p align=center>
	<select onchange="if(this.value) location.href=(this.value);">
	''')
		for names in list:
			if str(names) == str(name):
				self.W(O,'<option selected value="./%s">%s</option>' % (names+'.html',repr(int(names))+'화') + '\n')
			else:
				self.W(O,'<option value="./%s">%s</option>' % (names+'.html',repr(int(names))+'화') + '\n')
		self.W(O,'</select>\n</p>\n')

	def WriteMain(self,O,basename,name,list):
		self.W(O,'<html>\n<head>\n<title>%s - %d화</title>\n<style>' % (basename,int(name)))
		self.W(O,'''body { color: #000000; }
	a { color: #000000; }
	a:link { color: #000000; }
	a:hover { color: #000000; }
	a:visited { color:  #000000; }
	a {font-family: D2Coding; }
	img {border-color: gray;}
	select {
		background-color: white;
		border: 1px solid purple;
		border-radius: 10px;
		display: inline-block;
		font: inherit;
		line-height: 1.5em;
		padding: 0.5em 3.5em 0.5em 1em;
	
	margin: 0;
	-webkit-box-sizing: border-box;
	-moz-box-sizing: border-box;
	box-sizing: border-box;
	-webkit-appearance: none;
	-moz-appearance: none;
	
	
	background-image:
	linear-gradient(45deg, transparent 50%, gray 50%),
	linear-gradient(135deg, gray 50%, transparent 50%),
	radial-gradient(#ddd 70%, transparent 72%);
	background-position:
	calc(100% - 20px) calc(1em + 2px),
	calc(100% - 15px) calc(1em + 2px),
	calc(100% - .5em) .5em;
	background-size:
	5px 5px,
	5px 5px,
	1.5em 1.5em;
	background-repeat: no-repeat;
	}</style>
	<script>
	function aaa() {
	if ( document.getElementById('webim').style.cssText == "max-width: 100%;" ) {
		document.getElementById('webim').style="max-width: 3000;";
	} else {
		document.getElementById('webim').style="max-width: 100%;";
	}
	}
	</script>
	</head>
	<body style="margin:0;padding:0" bgcolor="White" onkeyup="asdf()">
	''')
	
		self.WH(O,name,list)
	
		self.W(O,'''<br>
	<p align=center>
	<a href="javascript:void(0);" onclick="aaa();">폰/컴</a>
	</p>
	''')
	
		self.W(O,'<p align=center>\n<img id="webim" src="./%s" style="max-width:2000;" border="0">\n' % (str(name) + '.png') + '</p>')
	
		self.WH(O,name,list)
	
		self.W(O,'''</body>
	</html>''')

	def MakeItFour(self,aaa):
		if len(aaa) == 1:
			aaa = '000' + aaa
		elif len(aaa) == 2:
			aaa = '00' + aaa
		elif len(aaa) == 3:
			aaa = '0' + aaa
		return aaa

class Merger(QThread):

	syntheticdone = pyqtSignal()

	def __init__(self,parent,datapath):
		super().__init__(parent)
		self.parent = parent
		self.datapath = datapath

	def combineImage1(self,full_width,full_height,image_key,image_list,index,will_del_list):
		canvas = Image.new('RGB', (full_width, full_height), 'white')
		output_height = 0
		
		for im in image_list:
			width, height = im.size
			canvas.paste(im, (0, output_height))
			output_height += height

		self.parent.statusBar().showMessage(image_key+'-'+str(index)+'.jpg 출력중..')
		canvas.save(self.datapath+'/'+image_key+'-'+str(index)+'.jpg')
		for i in will_del_list:
			os.remove(i)

	def combineImage2(self,full_width,full_height,image_key,image_list,index,will_del_list):
		canvas = Image.new('RGB', (full_width, full_height), 'white')
		output_height = 0
		
		for im in image_list:
			width, height = im.size
			canvas.paste(im, (0, output_height))
			output_height += height
		
		self.parent.statusBar().showMessage(image_key+'.png 출력중..')
		canvas.save(self.datapath+'/'+image_key+'.png')
		for i in will_del_list:
			os.remove(i)

	def ConvertImage(self,image_key,image_value):
		for i in image_value:
			im = Image.open(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')
	
		self.parent.statusBar().showMessage(image_key+'.png 출력중..')
		im.save(self.datapath+'/'+image_key+'.png')
		os.remove(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')

	def listImage1(self,image_key,image_value):
		full_width, full_height,index = 0, 0, 1
		image_list = []
		will_del_list = []

		for i in image_value:
			if len(str(i)) == 1:
				im = Image.open(self.datapath+'/'+image_key+'-'+'00'+str(i)+'.jpg')
				will_del_list.append(self.datapath+'/'+image_key+'-'+'00'+str(i)+'.jpg')
			elif len(str(i)) == 2:
				im = Image.open(self.datapath+'/'+image_key+'-'+'0'+str(i)+'.jpg')
				will_del_list.append(self.datapath+'/'+image_key+'-'+'0'+str(i)+'.jpg')
			elif len(str(i)) == 3:
				im = Image.open(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')
				will_del_list.append(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')
			width, height = im.size
	
			if full_height+height > 65535:
				self.combineImage1(full_width,full_height,image_key,image_list,index,[])
				index = index + 1
				image_list = []
				full_width, full_height = 0, 0
			
			image_list.append(im)
			full_width = max(full_width, width)
			full_height += height
	
		self.combineImage1(full_width,full_height,image_key,image_list,index,will_del_list)

	def listImage2(self,image_key,image_value):
		full_width, full_height,index = 0, 0, 1
		image_list = []
		will_del_list = []
		
		if len(image_value) != 1:
			for i in image_value:
				im = Image.open(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')
				will_del_list.append(self.datapath+'/'+image_key+'-'+str(i)+'.jpg')
				width, height = im.size
			
				if full_height+height > 1000000:
					self.combineImage2(full_width,full_height,image_key,image_list,index,[])
					index = index + 1
					image_list = []
					full_width, full_height = 0, 0
				
				image_list.append(im)
				full_width = max(full_width, width)
				full_height += height
			
			self.combineImage2(full_width,full_height,image_key,image_list,index,will_del_list)


	def run(self):
		files = glob.glob(self.datapath + '/*.jpg')

		name_list = {} 
		for f in files:
			name = f.split('\\')[1]
			key = name.split('-')[0]
			value = name.split('-')[1].split('.')[0]
	
			if key in name_list.keys():
				name_list[key].append(int(value))
			else:
				name_list[key] = [int(value)]
	
			name_list[key].sort()
		
		for key,value in name_list.items():
			self.listImage1(key,value)

		self.parent.statusBar().showMessage('1/3 단계 완료.')
		self.IM2()

	def IM2(self):
		files = glob.glob(self.datapath + '/*.jpg')

		name_list = {} 
		for f in files:
			name = f.split('\\')[1]
			key = name.split('-')[0]
			value = name.split('-')[1].split('.')[0]
	
			if key in name_list.keys():
				name_list[key].append(int(value))
			else:
				name_list[key] = [int(value)]
	
			name_list[key].sort()
		
		for key,value in name_list.items():
			self.listImage2(key,value)

		self.parent.statusBar().showMessage('2/3 단계 완료.')
		self.IM3()

	def IM3(self):
		files = glob.glob(self.datapath + '/*.jpg')

		name_list = {} 

		for f in files:
			name = f.split('\\')[1]
			key = name.split('-')[0]
			value = name.split('-')[1].split('.')[0]

			if key in name_list.keys():
				name_list[key].append(int(value))
			else:
				name_list[key] = [int(value)]

			name_list[key].sort()
		
		for key,value in name_list.items():
			if len(value) == 1:
				self.ConvertImage(key,value)
		self.parent.statusBar().showMessage('3/3 단계 완료.')
		self.parent.statusBar().showMessage('준비')
		self.syntheticdone.emit()

class Downloader(QThread):

	downdone = pyqtSignal()
	canceldone = pyqtSignal()
	bar = pyqtSignal(int)

	def __init__(self,parent,startno,endno,titleId,path):
		super().__init__(parent)
		self.parent = parent
		self.startno = startno
		self.endno = endno
		self.titleId = titleId
		self.path = path
		self.canceled = False

	def run(self):
		pb = 1
		total = int(self.endno) - int(self.startno)
		i = int(self.startno)
		downloaded = []
		while i <= int(self.endno):
			if self.canceled == False:
				url = 'https://comic.naver.com/webtoon/detail.nhn?titleId='+self.titleId+'&no='+str(i)
				response = requests.get(url, allow_redirects=False)
				if response != '<Response [302]>':
					soup = BeautifulSoup(response.text, 'html.parser')
					content = soup.select('div.section_cont > div.view_area > div.wt_viewer > img')
					z = 1
					for x in content:
						if self.canceled == True:
							self.canceldownload(downloaded)
							return
						else:
							img_url = x['src']
							headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
							r = requests.get(img_url, headers = headers)
							self.parent.statusBar().showMessage(self.MakeItFour(i)+'-'+self.MakeItThree(z)+'.jpg 다운로드중..')
							open(self.path+'/'+self.MakeItFour(i)+'-'+self.MakeItThree(z)+'.jpg', 'wb').write(r.content)
							downloaded.append(self.path+'/'+self.MakeItFour(i)+'-'+self.MakeItThree(z)+'.jpg')
							z = z+1
				elif self.canceled == True:
					self.canceldownload(downloaded)
					return
				pbper = (pb * 100) / total
				self.bar.emit(round(pbper))
				pb += 1
				i += 1
			else:
				self.canceldownload(downloaded)
				return
		self.parent.statusBar().showMessage('다운로드 완료.')
		self.parent.statusBar().showMessage('준비')
		self.downdone.emit()

	def canceldownload(self,value):
		self.parent.statusBar().showMessage('취소중..')
		for x in value:
			os.remove(x)
		self.parent.statusBar().showMessage('준비')
		self.canceldone.emit()

	def cancel(self):
		self.canceled = True

	def MakeItFour(self,aaa):
		if len(str(aaa)) == 1:
			aaa = '000' + str(aaa)
		elif len(str(aaa)) == 2:
			aaa = '00' + str(aaa)
		elif len(str(aaa)) == 3:
			aaa = '0' + str(aaa)
		return str(aaa)

	def MakeItThree(self,aaa):
		if len(str(aaa)) == 1:
			aaa = '00' + str(aaa)
		elif len(str(aaa)) == 2:
			aaa = '0' + str(aaa)
		return str(aaa)

if __name__ == '__main__':

	try:
		os.chdir(sys._MEIPASS)
		print(sys._MEIPASS)
	except:
		os.chdir(os.getcwd())

	app = QApplication(sys.argv)
	ex = Gui()
	sys.exit(app.exec_())