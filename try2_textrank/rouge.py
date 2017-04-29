from pyrouge import Rouge155
from pprint import pprint
import sys
import io

reload(sys)
sys.setdefaultencoding('utf8')


with open('article.txt', 'r') as fp:
	content = fp.readlines()

with open('out.txt', 'r') as fp:
	summary = fp.readlines()

rouge = Rouge155('/home/mahesh/Desktop/RELEASE-1.5.5')
score = rouge.score_summary(summary, content)
pprint(score)





