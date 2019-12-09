import pickle
import time

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

class Character():
    def __init__(self, name, description):
        self.name = name
        self.decription = description

directory = input("CharacterTree:\n[>> ")+'.cgt'


try:
    pickle_in = open(directory,"rb")
    firstQuestion = pickle.load(pickle_in)
    pickle_in.close()
except:
    print("Creating New Tree")
    time.sleep(0.7)
    trueCharacterName = input("Please input the name of 2 character's pressing Enter at the end of each. \n>>> ")
    falseCharacterName = input(">>> ")
    trueCharacterDescription = input("And now a description for each. \n>>> ")
    falseCharacterDescription = input(">>> ")
    msg = "Now please give a question you would reply yes to if thinking of "+trueCharacterName+" and no to if thinking of "+falseCharacterName+". \n[>> "
    question = input(msg)
    firstQuestion = Question(question,Character(trueCharacterName,trueCharacterDescription),Character(falseCharacterName,falseCharacterDescription),None)
    f= open(directory,"w+")
    f.close
    pickle_out = open(directory,"wb")
    pickle.dump(firstQuestion, pickle_out)
    pickle_out.close()  
    print("\n\n\n")
    

def game():
    firstQuestion.ask()
    pickle_out = open(directory,"wb")
    pickle.dump(firstQuestion, pickle_out)
    pickle_out.close()  
    print("\n\n\n")
    game()


game()
