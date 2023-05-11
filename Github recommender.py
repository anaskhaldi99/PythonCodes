from Tkinter import *
import ttk
from recommendations import *
import tkFileDialog
root = Tk()

class Repository:
    def __init__(self,ID,name,URL,language):
        self.ID = ID
        self.name = name
        self.URL = URL
        self.language = language

class Starred_data:
    def __init__(self,):
        self.prefs = {}  # key is the User's ID, value is a NESTED dictionary of repository class object as key, and ranking as value
        self.users_languages = {}  # dictionary where the key is the code language, and the value is a list of users' ids who have that language in their repositories
class GithubUser:
    def __init__(self,ID,username,URL):
        self.ID = ID
        self.username = username
        self.URL = URL

class GUI:
    def __init__(self):
        self.initGUI ()
        self.users_data = {} # key is the ID, value is the GithubUser class object
        self.users_data2 = {} # same as user_data dictionary, but with key as username not ID (this was used for sorting purposes)
        self.repository_data = {} # key is the repository ID, value is the Repository class object
    def initGUI(self):
        self.languages = ['None','TypeScript', 'Scala', 'Julia', 'Dart', 'Swift', 'TeX', 'python', 'C++', 'ruby', 'C', 'JavaScript', 'Java', 'JupyterNotebook', 'HTML', 'Go','-']  # list of all languages for the combobox
        self.evar = BooleanVar() # for Euclidean cb
        self.pvar = BooleanVar() # for pearson cb
        self.combovar = StringVar() # for combobox
        title_frame = Frame(root) # title frame only
        frame = Frame(root) # frame that will hold the uploading buttons
        frame2 = Frame(root) # frame that will hold everything else
        title_frame.pack(fill=X)
        frame.pack(fill=BOTH,expand=True)
        frame2.pack(fill=BOTH,expand=True,pady=(80,0))
        self.title_label = Label(title_frame,text='Github Project Recommender',bg='orange',fg='white',font=('','16','bold'))
        self.title_label.pack(fill=X)

        self.user_data_button = Button(frame,text='Upload User Data',width=15,height=2,command=self.user_data_button)
        self.user_data_button.grid(pady=(20,0),padx=(20,0),sticky=NSEW)

        self.rectangular_blank = Canvas(frame,bg='grey',width=300,height=2)
        self.rectangular_blank.grid(row=0,column=1,sticky=NSEW,pady=(20,0))

        self.repository_data_button = Button(frame,text='Upload Repository Data',width=20,height=2,command=self.repository_data_button)
        self.repository_data_button.grid(row=0,column=2,sticky=NSEW,pady=(20,0))

        self.rectangular_blank2 = Canvas(frame, bg='grey', width=300, height=2)
        self.rectangular_blank2.grid(row=0,column=3,sticky=NSEW,pady=(20,0))

        self.star_data_button = Button(frame,text='Upload Star Data',width=15,height=2,command=self.star_data_button)
        self.star_data_button.grid(row=0,column=4,sticky=NSEW,pady=(20,0),padx=(0,20))

        self.recommend_repository_label = Label(frame2,text='Recommend Repository For:')
        self.recommend_repository_label.grid(row=1,column=0,padx=(10,0),pady=(20,0),sticky=NSEW)

        self.users_tv = ttk.Treeview(frame2,columns=('username','Id'),show='headings') # the show option is to omit the first column which is useless in our case
        self.users_tv.heading('username',text='Username') # HEADINGS TAKE A PLACE in grid (ROW = 1)!!!
        self.users_tv.heading('Id',text='Id')
        self.users_tv.column('username',width=100) # ROW = 2 FOR COLUMNS!!!
        self.users_tv.column('Id',width=50)
        self.users_tv.grid(padx=(10,0),pady=(10,0))

        self.scroll1 = ttk.Scrollbar(frame2, orient='vertical', command=self.users_tv.yview)
        self.users_tv.configure(yscroll=self.scroll1.set) # applying the scroll bar to the treeview
        self.scroll1.grid(row=2, column=1,sticky=N+S+W)

        self.filter_label = Label(frame2,text='Filter by Programming language:')
        self.filter_label.grid(row=3,column=0,pady=10,padx=(5,0))

        self.combobox = ttk.Combobox(frame2,values=self.languages,textvariable=self.combovar,state='readonly') # readonly is for not allowing the users to alter the combobox
        self.combobox.grid(row=4,column=0)

        self.distance_algorithm_label = Label(frame2,text='Distance algorithm:')
        self.distance_algorithm_label.grid(row=5,column=0,pady=(10,0))

        self.pearson_checkbutton = Checkbutton(frame2,text='Pearson',variable=self.pvar)
        self.pearson_checkbutton.grid(row=6,column=0)

        self.euclidean_checkbutton = Checkbutton(frame2,text='Euclidean',variable=self.evar)
        self.euclidean_checkbutton.grid(row=7,column=0)

        self.number_of_recom_label = Label(frame2,text='Number of Recommendations:')
        self.number_of_recom_label.grid(row=8,column=0,sticky=W,pady=(0,50))

        self.number_entry = Entry(frame2,width=4)
        self.number_entry.grid(row=8,column=1,sticky=W,pady=(0,50))

        self.recommend_repository_button = Button(frame2,text='Recommend Repository',width=20,height=2,command=self.recommend_repository_button)
        self.recommend_repository_button.grid(row=2,column=3,padx=(30,0),pady=(100,0))

        self.recommend_github_button = Button(frame2,text='Recommend Github User',width=22,height=2,command=self.recommend_github_user_button)
        self.recommend_github_button.grid(row=2,column=3,padx=(30,0),pady=(180,0))

        self.recommendations_label = Label(frame2,text='Recommendations')
        self.recommendations_label.grid(row=0,column=4,padx=(200,0))

        self.recommendations_tv = ttk.Treeview(frame2,columns=('name','url','score'),show='headings')
        self.recommendations_tv.heading('name',text='Name')
        self.recommendations_tv.heading('url',text='URL') # specifying headings
        self.recommendations_tv.heading('score',text='Score')
        self.recommendations_tv.column('name',width=100)
        self.recommendations_tv.column('url',width=250)
        self.recommendations_tv.column('score',width=50)
        self.recommendations_tv.grid(row=1,column=4,padx=(200,20),rowspan=9,sticky=NS,pady=(0,20))

        # IN THE CASE OF THE SECOND TREEVIEW WIDGET, THERE IS NO NEED FOR USING A SCROLLBAR SINCE IT OCCUPIES A LARGE ENOUGH SPACE

        # self.scroll2 = ttk.Scrollbar(frame2,orient='vertical',command=self.recommendations_tv.yview)
        # self.recommendations_tv.configure(yscroll=self.scroll2.set)
        # self.scroll2.grid(row=1,column=5,sticky=N+S+W,padx=(0,20))


    def user_data_button(self):
        filename = tkFileDialog.askopenfilename(title="Please choose your file(Users data):", filetypes=(('text file','*.txt*'),('all files','*.*'))) # returns the file absolute path of the chosen file
        with open(filename) as usersfile: # opening the file for reading
            for user in usersfile.readlines():
                lst = user.split(',') # splitting the list into ID,username,and URL of the user respectively
                ID,username,URL = (lst[0],lst[1].lower(),lst[2][:-1])
                self.users_data[ID] = GithubUser(ID,username,URL) # creating the GithubUser instances and inserting them into a dictionary where the key is the user ID
                self.users_data2[username] = GithubUser(ID,username,URL)    # doing the same as above, but inserting them into a dictionary where the key is the username 
        lst_of_users = [] # list for sorting names
        for user in self.users_data2:
            lst_of_users.append(user)
        lst_of_users.sort()
        for user in lst_of_users: # inserting the users in alphabetical order
            self.users_tv.insert('',END,values=(user, self.users_data2[user].ID))

    def repository_data_button(self): # applying the logic (code) as in users txt file
        filename = tkFileDialog.askopenfilename(title='please choose your file (repository data):', filetypes= (('text file','*.txt*'),('all files','*.*')))
        with open(filename) as data:
            for repository in data.readlines():
                lst = repository.split(',')
                ID,name,URL,language = (lst[0],lst[1],lst[2],lst[3][:-1])
                self.repository_data[ID] = Repository(ID,name,URL,language)
            self.combovar.set('None')

    def star_data_button(self):
        filename = tkFileDialog.askopenfilename(title='please choose your file (star data):', filetypes= (('text file','*.txt*'),('all files','*.*')))
        with open(filename) as star:
            self.data = Starred_data() # creating an instance of Starred data class
            for text in star.readlines():
                modified_text = text.replace('\t',',').replace('\n','') # replace here is used to eliminate the tabs and newlines in the text
                lst_of_ids = modified_text.split(',') # splitting the text into a list of user ID as FIRST ITEM, and the rest of the items representing the repository IDS
                user_id = lst_of_ids[0]
                for id in lst_of_ids[1:]: # id here is the repository's id
                    self.data.prefs.setdefault(user_id,{}) # creating the nested dictionary for each user_id
                    self.data.prefs[user_id][self.repository_data[id]] = 5.0 #placing key as repository object and value as rating to the nested dictionary inside
            # this part is for filtering users according to their starred code languages
            for language in self.languages[1:]: # checking for each language separately excluding the '-'
                for user in self.data.prefs: # checking for each one of the users alone if they have starred repositories of this 'looped' language or not
                    for repository in self.data.prefs[user]:
                        if repository.language == language:
                            self.data.users_languages.setdefault(language,[])
                            self.data.users_languages[language] += [user] # adding all the users who have starred a repository including this language to a list which is the 'language' (key) value

    def recommend_repository_button(self):
        number = self.number_entry.get()
        language = self.combobox.get()
        euclidean_distance = self.evar.get()
        pearson_distance = self.pvar.get()
        selected = self.users_tv.selection()
        id = str(self.users_tv.item(selected)['values'][1]) # this gives the selected user id
        if language == 'None': # in the case of no filter for language
            if pearson_distance == True and euclidean_distance == False:  # in case of pearson measurement
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children()) # for clearing the whole treeview
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_pearson) # recommendations list of tuples where the first itme in the tuple is the ranking and the other is the object in this case
                    for i in range(int(number)): # here it will execute the code if there was an integer provided by the user in the number entry. Otherwise, it will just skip to the 'except' part
                        # THIS PART OF TRY AND EXCEPT WILL APPLY TO THE REMAININIG PART OF THE RECOMMENDATION BUTTONS CODE SO THAT THE NUMBER OF TOP MATCHES OR RECOMMENDATIONS PROVIDED BY THE USER IS CONSIDERED
                        repository_object = recommendations[i][1]
                        score = recommendations[i][0]
                        self.recommendations_tv.insert('', END,
                                                       values=(repository_object.name, repository_object.URL, score)) # inserting the matched or recommended items into the treeview
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_pearson)
                    for recommendation in recommendations:
                        repository_id = recommendation[1]
                        score = recommendation[0]
                        self.recommendations_tv.insert('', END, values=(
                        self.repository_data[repository_id].name, self.repository_data[repository_id].URL, score))
            elif euclidean_distance == True and pearson_distance == False: # in case of Euclidean measurement
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_distance)
                    for i in range(int(number)):
                        repository_object = recommendations[i][1]
                        score = recommendations[i][0]
                        self.recommendations_tv.insert('',END,values=(repository_object.name,repository_object.URL,score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_distance)
                    for recommendation in recommendations:
                        repository_object = recommendation[1]
                        score = recommendation[0]
                        self.recommendations_tv.insert('', END, values=(
                        repository_object.name, repository_object.URL, score))
            else: # this is used throughout the remaining code to prevent any error while running the code
                pass
        else: # if there was a language filter
            if pearson_distance == True and euclidean_distance == False: # in case of pearson measurement
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = [] # list where the FILTERED RESULTED are appended (for inserting them later in the treeview)
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_pearson)
                    for recommendation in recommendations:
                        if language == recommendation[1].language: # checking if the language in the combobox matches that of the repository in the loop
                            lst.append(recommendation)
                    for i in range(int(number)):
                        repository_object = lst[i][1] # acquiring the object from the filtered list this time and not the recommendations list
                        score = lst[i][0]
                        self.recommendations_tv.insert('', END,values=(repository_object.name, repository_object.URL, score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_pearson)
                    for recommendation in recommendations:
                        if language == recommendation[1].language:
                            lst.append(recommendation)
                    for recommendation in lst:
                        repository_object = recommendation[1]
                        score = recommendation[0]
                        self.recommendations_tv.insert('', END, values=(repository_object.name, repository_object.URL, score))
            elif euclidean_distance == True and pearson_distance == False: # in case of Euclidean measurement
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_distance)
                    for recommendation in recommendations:
                        if language == recommendation[1].language:
                            lst.append(recommendation)
                    for i in range(int(number)):
                        repository_object = lst[i][1]
                        score = lst[i][0]
                        self.recommendations_tv.insert('', END,values=(repository_object.name, repository_object.URL, score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    recommendations = getRecommendations(self.data.prefs, id, similarity=sim_distance)
                    for recommendation in recommendations:
                        if language == recommendation[1].language:
                            lst.append(recommendation)
                    for recommendation in lst:
                        repository_object = recommendation[1]
                        score = recommendation[0]
                        self.recommendations_tv.insert('', END, values=(repository_object.name, repository_object.URL, score))
            else:
                pass

    def recommend_github_user_button(self): # EXACTLY THE SAME 'CODING LOGIC' TO EVERYTHING IS APPLIED HERE WITH RELATIVE TO THE PREVIOUS BUTTON
        # EXCEPT THE FACT THAT HERE WE ARE USING THE topMatches FUNCTION AND NOT THE getRecommendations
        number = self.number_entry.get()
        language = self.combobox.get()
        euclidean_distance = self.evar.get()
        pearson_distance = self.pvar.get()
        selected = self.users_tv.selection()
        id = str(self.users_tv.item(selected)['values'][1])
        if language == 'None':
            if pearson_distance == True and euclidean_distance == False:
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    topmatches = topMatches(self.data.prefs,id,n=int(number),similarity=sim_pearson) # HERE IS THE ONLY DIFFERENCE !!
                    for match in topmatches:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    topmatches = topMatches(self.data.prefs, id,similarity=sim_pearson)
                    for match in topmatches:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
            elif euclidean_distance == True and pearson_distance == False:
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    topmatches = topMatches(self.data.prefs,id,n=int(number),similarity=sim_distance)
                    for match in topmatches:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    self.recommendations_tv.delete()
                    topmatches = topMatches(self.data.prefs, id,similarity=sim_distance)
                    for match in topmatches:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
            else:
                pass
        else: # in case of language filtering for the users
            if pearson_distance == True and euclidean_distance == False:
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    topmatches = topMatches(self.data.prefs,id,n=int(number),similarity=sim_pearson)
                    for match in topmatches:
                        user_id = match[1]
                        if user_id in self.data.users_languages[language]:
                            lst.append(match)
                    for i in range(int(number)):
                        username = self.users_data[lst[i][1]].username
                        url = self.users_data[lst[i][1]].URL
                        score = lst[i][0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    topmatches = topMatches(self.data.prefs, id,similarity=sim_pearson)
                    for match in topmatches:
                        user_id = match[1]
                        if user_id in self.data.users_languages[language]:
                            lst.append(match)
                    for match in lst:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('',END,values=(username,url,score))
            elif euclidean_distance == True and pearson_distance == False:
                try:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    topmatches = topMatches(self.data.prefs, id, n=int(number), similarity=sim_distance)
                    for match in topmatches:
                        user_id = match[1]
                        if user_id in self.data.users_languages[language]:
                            lst.append(match)
                    for i in range(int(number)):
                        username = self.users_data[lst[i][1]].username
                        url = self.users_data[lst[i][1]].URL
                        score = lst[i][0]
                        self.recommendations_tv.insert('', END, values=(username, url, score))
                except:
                    self.recommendations_tv.delete(*self.recommendations_tv.get_children())
                    lst = []
                    topmatches = topMatches(self.data.prefs, id, similarity=sim_distance)
                    for match in topmatches:
                        user_id = match[1]
                        if user_id in self.data.users_languages[language]:
                            lst.append(match)
                    for match in lst:
                        username = self.users_data[match[1]].username
                        url = self.users_data[match[1]].URL
                        score = match[0]
                        self.recommendations_tv.insert('', END, values=(username, url, score))
            else:
                pass

app = GUI()
root.mainloop()

