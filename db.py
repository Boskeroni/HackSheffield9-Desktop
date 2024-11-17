from firebase_admin import db
import firebase_admin

class DBHandler:
    def __init__(self):
        credObj = firebase_admin.credentials.Certificate("include/db_credentials.json")
        databaseURL = "https://hack-sheffield-project-default-rtdb.europe-west1.firebasedatabase.app/"
        default_app = firebase_admin.initialize_app(credObj, {'databaseURL':databaseURL})
        self.rootRef = db.reference("/")

    # Returns the password for a given email address. If email address does not exist (therefore the account does not exist), returns -1
    def checkPassword(self, emailAddress, password_trial):
        userRef = self.rootRef.child("Users")
        field = list(userRef.order_by_child("email_address").equal_to(emailAddress).get().values())
        if len(field) == 0:
            return False
        return (field[0]["password"] == password_trial)
    
    # Returns the userId for a given email address. If email address does not exist (therefore the account does not exist), returns -1
    def getUserId(self, emailAddress):
        userRef = self.rootRef.child("Users")
        field = list(userRef.order_by_child("email_address").equal_to(emailAddress).get().keys())
        if len(field) == 0:
            return -1
        else:
            return field[0]

    # Creates a Users record with the given email address and password, where it generates a unique userID
    def createUser(self, emailAddress, password):
        userRef = self.rootRef.child("Users")
        userRef.push().set({
            "email_address": emailAddress,
            "password": password,
            "available_plots": 0
        })

        default_height = 40
        default_width = 40
        empty_layout = "0" * default_height * default_width
        self.createLayout(emailAddress, empty_layout, default_height, default_width)
        
    # Returns a lists of every task for a given email address, if there are none then it will return an empty list
    def getTasks(self, emailAddress):
        userId = self.getUserId(emailAddress)

        taskRef = self.rootRef.child("Tasks")
        tasks = taskRef.order_by_child("user_id").equal_to(userId).get()

        new_local_tasks = []
        for task_ids in tasks.keys():
            new_local_tasks.append((tasks[task_ids]["task"], tasks[task_ids]["difficulty"], task_ids))

        return new_local_tasks

    # Creates a Tasks record with the given email address and task, where it generates a unique userID
    def createTask(self, task, emailAddress, difficulty):
        userId = self.getUserId(emailAddress)

        taskRef = self.rootRef.child("Tasks")
        new_task = taskRef.push()
        
        new_task.set({
            "task": task,
            "user_id": userId,
            "difficulty": difficulty
        })

        return new_task.key
    
    def deleteSpecificTask(self, taskId):
        taskRef= self.rootRef.child("Tasks")
        taskRef.child(taskId).delete()

    # Returns a layout for a given email address, if there are none then it will return an empty list
    def getLayout(self, emailAddress):
        userId = self.getUserId(emailAddress)

        layoutRef = self.rootRef.child("Layouts")
        field = list(layoutRef.order_by_child("user_id").equal_to(userId).get().values())

        if len(field) == 0:
            return -1
        else:
            return field[0]

    # Creates a Layouts record with the given email address and layout, where it generates a unique userID
    def createLayout(self, emailAddress, layout, height, width):
        userId = self.getUserId(emailAddress)

        layoutRef = self.rootRef.child("Layouts")
        layoutRef.push().set({
            "layout": layout,
            "user_id": userId,
            "height": height,
            "width": width
        })
    
    def updateLayout(self, emailAddress, newLayout):
        userId = self.getUserId(emailAddress)
        layoutRef = self.rootRef.child("Layouts")
        layouts_table = list(layoutRef.get().items())
        
        for key, value in layouts_table:
            if value["user_id"] == userId:
                layoutRef.child(key).update({"layout": newLayout})

    def updateAvailablePlots(self, emailAddress, newAvailablePlots):
        userId = self.getUserId(emailAddress)
        usersRef = self.rootRef.child("Users")
        usersRef.child(userId).update({"available_plots": newAvailablePlots})

    def getAvailablePlots(self, emailAddress):
        userRef = self.rootRef.child("Users")
        field = list(userRef.order_by_child("email_address").equal_to(emailAddress).get().values())
        if len(field) == 0:
            return -1
        return field[0]["available_plots"]
    
    def deleteTasks(self, emailAddress):
        userId = self.getUserId(emailAddress)

        taskRef = self.rootRef.child("Tasks")
        fields = list(taskRef.order_by_child("user_id").equal_to(userId).get().keys())

        for key in fields:
            taskRef.child(key).delete()