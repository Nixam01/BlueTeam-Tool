# TODO:
#  OFF.LOG.1 zrob mozliwosc wywołania operacji systemowej grep
#  na wskazanych plikach tekstowych. Argumentem przekazywanym do operacji
#  jest właściwe wyrażenie regularne.
#  OFF.LOG.2 zrob możliwość wywołania działania wyrażenia regularnego z modułu Python
#  re na wskazanych plikach tekstowych lub EVTX przetworzonych do formatu JSON/XML/inny tekstowy.
#  Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne.
#  pomocne linki:
#  https://appdividend.com/2021/05/03/python-grep/
#  https://stackoverflow.com/questions/1921894/grep-and-python
#  https://stackoverflow.com/questions/15026357/use-grep-on-file-in-python


#wstepny kod na ktorym beda bazowac dalsze prace
import re

file = open("data.txt", "w")

file.write("One Up\nTwo Friends\nThree Musketeers")
file.close()

pattern = "Friends"

file = open("data.txt", "r")

for word in file:
    if re.search(pattern, word):
        print(word)