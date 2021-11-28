# -*- coding: utf-8 -*- 

import glob
import os

def W(O,M):
	O.write(M)

def MakeItFour(aaa):
	if len(aaa) == 1:
		aaa = '000' + aaa
	elif len(aaa) == 2:
		aaa = '00' + aaa
	elif len(aaa) == 3:
		aaa = '0' + aaa
	return aaa

def WH(O,name,list):
	W(O,'<p align=left style="float: left;">')
	backs = MakeItFour(str(int(name)-1))
	if backs in list:
		W(O,'<a href="%s.html">이전화</a>' % backs)
	else:
		W(O,'''<a href="void(0);" onclick="alert('최초화입니다.');return false;">이전화</a>''')
	W(O,'</p>\n<p align=right style="float: right;">\n')
	nexts = MakeItFour(str(int(name)+1))
	if nexts in list:
		W(O,'<a href="%s.html">다음화</a>' % nexts)
	else:
		W(O,'''<a href="void(0);" onclick="alert('마지막화입니다.');return false;">다음화</a>''')
	W(O,'</p>')
	W(O,'''</p>
<p align=center>
<select onchange="if(this.value) location.href=(this.value);">
''')
	for names in list:
		if str(names) == str(name):
			W(O,'<option selected value="./%s">%s</option>' % (names+'.html',repr(int(names))+'화') + '\n')
		else:
			W(O,'<option value="./%s">%s</option>' % (names+'.html',repr(int(names))+'화') + '\n')
	W(O,'</select>\n</p>\n')

def WriteMain(O,basename,name,list):
	W(O,'<html>\n<head>\n<title>%s - %d화</title>\n<style>' % (basename,int(name)))
	W(O,'''body { color: #000000; }
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

	WH(O,name,list)

	W(O,'''<br>
<p align=center>
<a href="javascript:void(0);" onclick="aaa();">폰/컴</a>
</p>
''')

	##########################################################################
																			#
	W(O,'<p align=center>\n<img id="webim" src="./%s" style="max-width:2000;" border="0">\n' % (str(name) + '.png') + '</p>')
																			#
	##########################################################################

	WH(O,name,list)

	W(O,'''</body>
</html>''')

if __name__ == '__main__' :

	print('[Htmler] Start Htmler!')

	print('[Htmler] Get png files..')

	target_dir = './'
	files = glob.glob(target_dir + '*.png')

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
		print('[Htmler] Get %s.png' % n)
		name_list.append(n)
	del gar

	basename = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

	for i in name_list:
		f = open(i + '.html', 'w')
		WriteMain(f,basename,i,name_list)
		f.close()
		print('[Htmler] Made %s.html' % i)

	print('[Htmler] Complete making htmls')