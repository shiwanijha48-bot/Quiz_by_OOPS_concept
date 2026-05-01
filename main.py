import os

class Quiz: 

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__)) 
# stores project folder path, inialized in __init__, so that can access this path in class anywhere
#__file__ : special builtin variable in py, store name of path of curr py file
# abspath-> absolute path, gives the whole path. then removed the file name by dirname: which only gives the path.
#  stored that path in self.base_path 

# ----------------------------------------------------------------
    def registration(self):
        print("----------Registration---------")
        name = input("Enter your Name: ")
        enrollment_no = input("Enter your Enrollment Number: ")
        contact = input("Enter your Phone Number: ")  
        email = input("Enter your Email ID: ")
        password = input("Enter your Password: ")

        if enrollment_no.startswith("LN"):
            college = "LNCT University"
        elif enrollment_no.startswith("0103"):
            college = "LNCT"
        elif enrollment_no.startswith("0176"):
            college = "LNCTE"
        elif enrollment_no.startswith("0157"):
            college = "LNCTS"
        else:
            college = "not_known"
        print("College: ", college)

        if "CY" in enrollment_no:
            branch = "CyberSecurity"
        elif "AL" in enrollment_no:
            branch = "AIML"
        elif "AD" in enrollment_no:
            branch = "AIDS"
        elif "C" in enrollment_no:
            branch = "CSE"
        else:
            branch = "not_known"
        print("Branch: ", branch)

        with open("registration.txt", "a") as f:
            f.write(f"{name},{email},{contact},{enrollment_no},{password},{college},{branch}\n")

        with open("login.txt", "a") as f:
            f.write(f"{enrollment_no},{password}\n")

        print("-----Registration Successful-----")

# ----------------------------------------------------------------
    def login(self):
        print("-------Login-------")
        enrollment_no = input("Enter Enrollment Number: ")
        password = input("Enter your Password: ")

        if not os.path.exists("login.txt"):
            print("No users registered right now!")
            return None # file doesnt exist, so return. 
        # stop function immediately. or it will continue, try to open file & error aayega.

        with open("login.txt", "r") as f:
            for line in f:
                userEnroll, userPswd = line.strip().split(",") # strip removes extra space,/n new line. split- breaks str by"," here.
                if enrollment_no == userEnroll and password == userPswd:
                    print("----- Login Successful! ----- ")
                    return enrollment_no # after login successful, enroll_no back to main, so system knows who logged in. 
                    # passed to attempt_quiz(enroll), or profile(enroll) or others.

        print("------ Invalid Enrollment Number and Password -------")
        return None # if login fails, return none, cond false, menu wont open
        # without return, program may continue wrongly

# ----------------------------------------------------------------
    def attempt_quiz(self, enrollment_no):
        print("------ Attempt Quiz ------")
        print("Choose your Test Subject: \n 1. Python\n 2. DSA\n 3. DBMS")

        try:
            choice3 = int(input("Choose Quiz: "))
        except:
            print("Invalid Input!")
            return # if dont return, program continue, crash later.exits func safely

        if choice3 == 1:
            filename = os.path.join(self.base_path, "python.txt")  # joins the basepath of folder,add filename
            quizName = "Python"
        elif choice3 == 2:
            filename = os.path.join(self.base_path, "dsa.txt")
            quizName = "DSA"
        elif choice3 == 3:
            filename = os.path.join(self.base_path, "dbms.txt")
            quizName = "DBMS"
        else:
            print("Invalid Choice!")
            return

        if not os.path.exists(filename):
            print("Quiz not found!")
            return # file doesnt exit, no return then will crash in with open(filename) line

        score = 0
        quesNo = 1

        with open(filename, "r") as file:
            for line in file: # line by line read, each question->line
                line = line.strip() # remove newline & spaces
                if not line: # empty line, skip karo
                    continue
                question, options, correctAnswer = line.split("|")
                print("\nQ",quesNo,":",question) # ques print 

                optionList = options.split(",") # options spliting into 1,2,3,4
                for i in range(len(optionList)): # len(optionlist) = 4
                    print(i + 1,")",optionList[i]) # i+1 = 0+1 = 1) option1

                try:
                    userChoice = int(input("Enter Option Number: "))
                except:
                    print("Invalid Input!")
                    quesNo += 1
                    continue

                if 1 <= userChoice <= len(optionList): # basically (1,4)
                    if optionList[userChoice - 1].strip().lower() == correctAnswer.strip().lower(): 
                        score += 1 # strip- remove space, lower- case insensitive to match the option & correct ans
                else:
                    print("Invalid option number!")

                quesNo += 1

        print("\nYour Score is:", score)

        with open("score.txt", "a") as f:
            f.write(f"{enrollment_no},{quizName},{score}\n")

    # ----------------------------------------------------------------
    def profile(self, enrollment_no):
        print("------- Profile -------")

        if not os.path.exists("registration.txt"): # if file doesnt exist, stop
            print("No User data found!") # show msg, and stop func safely
            return # return so that it may not try again to open file in "r" mode

        with open("registration.txt", "r") as f:
            for line in f:
                name, email, contact, enrollNo, pwd, college, branch = line.strip().split(",")

                if enrollNo == enrollment_no:
                    print(f"Name: {name}")
                    print(f"Email: {email}")
                    print(f"Contact: {contact}")
                    print(f"Enrollment: {enrollment_no}")
                    print(f"College: {college}")
                    print(f"Branch: {branch}")
                    print("-"*30)
                    return

        print("-------- User Profile not found -----")

    # ----------------------------------------------------------------
    def updateProfile(self, enrollment_no):
        print("-------- Update profile --------")

        if not os.path.exists("registration.txt"):
            print("User data not found!")
            return

        with open("registration.txt", "r") as f: # Store opened file obj in variable f
            lines = f.readlines() # reads entire file & return

        with open("registration.txt", "w") as f:
            for line in lines:
                name, email, contact, enrollNo, pwd, college, branch = line.strip().split(",")

                if enrollNo == enrollment_no:
                    print("Enter the info that you want to change or just skip it!")
                    name = input(f"Name ({name}): ").strip() or name # if ""- empty. in python it is false, result = old name
                    email = input(f"Email ({email}): ").strip() or email # strip to remove spaces, " "- treue, then value change, which is wrong
                    contact = input(f"Contact Number ({contact}): ").strip() or contact # new value or old value
                    f.write(f"{name},{email},{contact},{enrollNo},{pwd},{college},{branch}\n")
                else: # 
                    f.write(line) # it doesnt match, wrte back unchanged data of other users

        print("---------- Profile Updated Successfully! -----------")

    # ----------------------------------------------------------------
    def score(self, enrollment_no):
        print("------- Your Score ------")

        if not os.path.exists("score.txt"):
            print("No User Scores found!")
            return

        results = [] # store all matching quiz scores of that user

        with open("score.txt", "r") as f:
            for line in f:
                enrollNo, quizType, totalScore = line.strip().split(",")
                if enrollNo == enrollment_no:
                    results.append((quizType, totalScore)) # adds a tuple inside the list
        if results: # list not empty, list empty = false, non empty list = true
            for quizType, totalScore in results: # if true
                print(f"{quizType} Quiz: {totalScore} points secured!")
                print("-"*30)
        else:
            print("---------- No scores of user found! ------------")


    # ----------------------------------------------------------------
    def main(self):   
        while True: # infinite loop
            print("-" * 30)
            print("Choose an option:\n 1. Registration \n 2. Login \n 3. Exit ")
            print("-" * 30)

            try:
                choice1 = int(input("Enter your choice: ")) 
            except:
                print("Invalid choice!")
                continue # Input invalid → go back to menu → ask again

            if choice1 == 1:
                self.registration()
            elif choice1 == 2:
                enroll = self.login()
                if enroll: # check if login was successful
                    while True: # keep showing, until manually stop it or  until logout
                        print("\n 1. Attempt Quiz\n 2. Score \n 3. Profile \n 4. Update Profile \n 5. Logout")
                        try:
                            choice2 = int(input("Enter your choice: ")) 
                        except:
                            print("Invalid choice!")
                            continue

                        if choice2 == 1:
                            self.attempt_quiz(enroll)
                        elif choice2 == 2:
                            self.score(enroll)
                        elif choice2 == 3:
                            self.profile(enroll)
                        elif choice2 == 4:
                            self.updateProfile(enroll)
                        elif choice2 == 5:
                            print("Logging out----")
                            break # stop now
                        else:
                            print("Invalid Choice!")

            elif choice1 == 3:
                print("-"*30)
                print("Thank you for visiting!!!")
                print("-"*30)
                exit()
            else:
                print("Invalid choice!")

# obj = Quiz()
# obj.main()
if __name__ == "__main__": # when import this file in another py file, this obj will not auto-run.
    obj = Quiz()
    obj.main()
