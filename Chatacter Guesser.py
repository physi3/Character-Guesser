import pickle

#Online Line Text Code Start
import mechanize
import re

url = "http://freetexthost.com/cquc2fsbdc"

br=mechanize.Browser()
response = br.open(url)
try:
    br.set_all_readonly(False)
except:
    pass

def edit(text,pas,url): # text you want to add/replace, admin password , url 
    response = br.open(url)
    try:
        br.set_all_readonly(False)
    except:
        pass
    br.select_form("editform")
    control = br.form.find_control("adminpass")
    control.value=pas
    response = br.submit()
    br.select_form("editform")
    control = br.form.find_control("text")
    control.value=text
    response = br.submit()

def read(url):
    response = br.open(url)
    txt=response.read()
    t1=re.findall(r'<div id="contentsinner">(.*?)<div style="clear: both;"><!-- --></div>',txt.decode('iso-8859-1'),re.DOTALL)
    t1=t1[0]
    t1=t1.strip()
    return t1

#Online Line Text Code End

class Main():
    def __init__(self):
        self.answerHistory = []
main = Main()

class Question():
    def __init__(self, question, trueCharacter, falseCharacter, parentQuestion):
        self.question = question
        self.trueCharacters = [trueCharacter]
        self.falseCharacters = [falseCharacter]
        self.parentQuestion = parentQuestion
    def addQuestion(self ,questionTrueBool ,question, newCharacter, characterTrueBool):
        if questionTrueBool:
            if characterTrueBool:
                self.trueQuestion = Question(question,newCharacter,self.trueCharacters[0],self)
            else:
                self.trueQuestion = Question(question,self.trueCharacters[0],newCharacter,self)
        else:
            if characterTrueBool:
                self.falseQuestion = Question(question,newCharacter,self.falseCharacters[0],self)
            else:
                self.falseQuestion = Question(question,self.falseCharacters[0],newCharacter,self)
        self.addCharacter(newCharacter, main.answerHistory[-1])
    def addCharacter(self, newCharacter, trueBool):
        if trueBool:
            self.trueCharacters.append(newCharacter)
        else:
            self.falseCharacters.append(newCharacter)
        if self.parentQuestion != None:
            main.answerHistory = main.answerHistory[:-1]
            self.parentQuestion.addCharacter(newCharacter,main.answerHistory[-1])
    def ask(self):
        ans = input(self.question+" (Y/N)\n>>> ").lower()
        main.answerHistory.append(ans == "y")
        if ans == "y":
            if hasattr(self, 'trueQuestion'):
                self.trueQuestion.ask()
            else:
                ans = input("Is it "+self.trueCharacters[0].name+"\n"+self.trueCharacters[0].decription+" (Y/N)\n>>> ")
                if ans.lower() == "y":
                    print("Great")
                else:
                    character = input("Ohh... In that case please tell me,\nWhat is the name of your character\n>>>")
                    characterDesc = input("And could you give me a brief description of this person\n>>>")
                    question = input("And could you give me question I can ask that sent them aside from "+self.trueCharacters[0].name+" (Try and make it as broad as possible)\n>>>")
                    ans = input("If I asked you that question and you were thinking of "+character+" would you say yes (Y/N)\n>>>")
                    self.addQuestion(main.answerHistory[-1],question,Character(character,characterDesc) , ans.lower() == "y")
        else:
            if hasattr(self, 'falseQuestion'):
                self.falseQuestion.ask()
            else:
                ans = input("Is it "+self.falseCharacters[0].name+"\n"+self.falseCharacters[0].decription+" (Y/N)\n>>> ")
                if ans.lower() == "y":
                    print("Great")
                else:
                    character = input("Ohh... In that case please tell me,\nWhat is the name of your character\n>>>")
                    characterDesc = input("And could you give me a brief description of this person\n>>>")
                    question = input("And could you give me question I can ask that sent them aside from "+self.falseCharacters[0].name+" (Try and make it as broad as possible)\n>>>")
                    ans = input("If I asked you that question and you were thinking of "+character+" would you say yes (Y/N)\n>>>")
                    self.addQuestion(main.answerHistory[-1],question,Character(character,characterDesc) , ans.lower() == "y")

def dump():
    pickle_out = open("firstQuestion.pickle","wb")
    pickle.dump(firstQuestion, pickle_out)
    pickle_out.close()
    pickle_out = open("firstQuestion.pickle","r")
    firstQuestionToDump = pickle.read()
    pickle_out.close()
    edit(firstQuestionToDump,"puffin",url)

def pickleUpdate():
    pickle_in = open("firstQuestion.pickle","w")
    pickle_in.write(read(url))
    pickle_in.close()   

class Character():
    def __init__(self, name, description):
        self.name = name
        self.decription = description

pickleUpdate()

pickle_in = open("firstQuestion.pickle","rb")
firstQuestion = pickle.load(pickle_in)
pickle_in.close()

def game():
    firstQuestion.ask()
    
    print("\n\n\n")
    game()


game()
