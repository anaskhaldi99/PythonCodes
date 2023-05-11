from Tkinter import *
import ttk
import urllib2
from bs4 import BeautifulSoup
root = Tk()

class Dept(object): # objects of this will be created first
    def __init__(self,name,link):
        self.name = name
        self.link = link
        self.courses = {} # dictionary where key is course name and value is Course class object

class Course(object):
    def __init__(self,name,semester):
        self.name = name
        self.semester = semester

class GUI(object):
    def __init__(self):
        self.initGUI()
        self.undergraduate = {} # dictionary where key is department name, and value is Dept class object
    def initGUI(self):
        self.var1 = StringVar(root,value='off')
        self.var2 = StringVar(root,value='off')
        self.var3 = StringVar(root,value='off')
        self.lst_of_vars = [self.var1,self.var2,self.var3] # variables for check buttons
        frame1 = Frame(root,highlightbackground = 'red',highlightcolor = 'red',highlightthickness=4,bd=0) # red frame
        frame1.grid(sticky=NSEW,columnspan=2)
        frame2 = Frame(root) # frame for text widget and labels and treeview widget
        frame2.grid(row=1,column=0,sticky=NSEW)
        frame3 = Frame(root) # frame for including all the checkbuttons and the search button
        frame3.grid(row=1,column=1,sticky=NSEW)
        title_label = Label(frame1,text = 'WHAT MAJOR IS BEST FOR MY INTERESTS',bg='red',fg='white',font=('','18','bold'))
        title_label.grid(sticky=NSEW,columnspan=3,row=0,column=0,padx=4,pady=(4,0))

        url_label = Label(frame1,text='SEHIR\'s programs URL:',fg='red',font=('','12',''))
        url_label.grid(row=1,column=0,padx=30,sticky=W,pady=12)

        self.url_entry = Entry(frame1,width=60)
        self.url_entry.grid(row=1,column=1,padx=(0,20),columnspan=2)
        self.url_entry.insert(END,'https://www.sehir.edu.tr/en/academics/all-programs')

        space_canvas = Canvas(frame1,height=0,width=200)  # this canvas is created just to fill the empty space under 'SEHIR's program URL' label and provide and extra column for a better application
        space_canvas.grid(row=2,column=0,sticky=NSEW)

        self.colored_canvas = Canvas(frame1,width=70,height=25,bg='red')
        self.colored_canvas.grid(row=2,column=1,sticky=W,padx=(30,0),pady=(0,4))

        fetch_data_button = Button(frame1,fg='red',text='Fetch Data',width=14,height=1,command=self.fetch_data_button)
        fetch_data_button.grid(row=2,column=2,sticky=W,padx=(0,100),pady=(0,4))

        my_interests_label = Label(frame2,text='My Interests:',font=('','12','bold'))
        my_interests_label.grid(row=0,column=0,pady=12,padx=20,sticky=N)

        self.txt_widget = Text(frame2,width=18,height=6)
        self.txt_widget.grid(row=0,column=1,pady=2)

        ranking_measures_label = Label(frame2,text='Ranking measures:',font=('','12','bold'))
        ranking_measures_label.grid(row=0,column=2,sticky=N,padx=20,pady=12)

        self.txt_cb = Checkbutton(frame3,text='Text-based:',variable=self.var1,onvalue='on')
        self.curriculum_cb = Checkbutton(frame3,text='Curriculum-based:',variable=self.var2,onvalue='on')
        self.hub_score_cb = Checkbutton(frame3,text='Hub-score-based',variable=self.var3,onvalue='on')

        self.txt_cb.pack(anchor=W,pady=5)
        self.curriculum_cb.pack(anchor=W,pady=5)
        self.hub_score_cb.pack(anchor=W,pady=5)

        self.tv = ttk.Treeview(frame2,columns=('no','department name','score'),show='headings',height=8)
        self.tv.heading('no', text='No')
        self.tv.heading('department name', text='Department Name')  # specifying headings
        self.tv.heading('score', text='Score')
        self.tv.column('no', width=50)
        self.tv.column('department name', width=250)
        self.tv.column('score', width=50)
        self.tv.grid(row=1,columnspan=3,sticky=NSEW,padx=6,pady=(20,4))

        search_button  = Button(frame3,text='SEARCH',width=15,font=('','10 ','bold'),command=self.search_button)
        search_button.pack(pady=(100,0),anchor=W)

        # for column in range(10): # this code is for making the widgets 'flexible' as the window enlarges
        #     Grid.columnconfigure(frame2, column, weight=1)
        # for row in range(10):
        #     Grid.columnconfigure(frame2, row, weight=1)

    def fetch_data_button(self):
        try:
            self.colored_canvas.configure(bg='yellow') # changing the canvas color to yellow during the process
            self.colored_canvas.update()
            link = self.url_entry.get()
            set_of_depts = set() # set of lists as [URL,dept name]
            site = urllib2.urlopen(link)
            contents = site.read()
            soup = BeautifulSoup(contents,'html.parser')
            links = soup.find_all('a') # this gives you a list of ALL the programs in sehir university
            for link in links:
                try:
                    newlink = 'https://www.sehir.edu.tr'+link.get('href')
                    lst = [] # this will be a list of tuples where URLs are on [0] and department names are on [1]
                    mainlink = urllib2.urlopen(newlink)
                    contents = mainlink.read()
                    soup = BeautifulSoup(contents, 'html.parser')
                    interior_links = soup.find_all('a')
                    for link2 in interior_links:
                        try: # this was used to avoid any nonetype error
                            lst.append(('https://www.sehir.edu.tr'+link2.get('href'),link2.find('span').string))
                        except:pass
                    for i in lst: # i here is the tuple itself
                        if ('/law' in i[0] or '/islamic' in i[0] or 'department' in i[0]) and ('graduate' not in i[0] and 'erasmus' not in i[0].lower() and 'minor' not in i[0].lower() and 'major' not in i[0].lower() and 'curriculum' not in i[0].lower()):
                            set_of_depts.add(i)
                except:pass
            for url,dept in set_of_depts: # creating the
                self.undergraduate[url] = Dept(dept,url)
            for url in self.undergraduate: # url here is the link of the department where each department alone is then being opened to extract the curriculum and thus the courses and semesters information from it
                site = urllib2.urlopen(url)
                contents = site.read()
                soup = BeautifulSoup(contents,'html.parser')
                curriculum_links = soup.find_all('a',{'class':'static menu-item ms-core-listMenu-item ms-displayInline ms-navedit-linkNode'}) # this will return a list of links of this specified class
                try:
                    if '(in Turkish)' in self.undergraduate[url]: # this is just for filtering out the languages if a certain department had a certain or specific laguage
                        for link in curriculum_links:
                            if 'english/curriculum' in link.get('href'):
                                curriculum_links.remove(link)
                    elif '(in English)' in self.undergraduate[url]:
                        for link in curriculum_links:
                            if 'turkish/curriculum' in link.get('href'):
                                curriculum_links.remove(link)
                except:pass
                for link in curriculum_links: # running a loop in all departments curriculums to store course and semester data
                    if '/curriculum' in link.get('href'):
                        curriculum_link = 'https://www.sehir.edu.tr'+ link.get('href')
                        site = urllib2.urlopen(curriculum_link)
                        contents = site.read()
                        soup = BeautifulSoup(contents,'html.parser')
                        div_links = soup.find_all('div')
                        for link in div_links:
                            try:
                                if 'Semester' in link.get('id'): # this implies it is a course supposed to be stored in the data
                                    for i in link.find_all('a', {'href': '#'}): # i here is the 'a' tag in the html code
                                        self.undergraduate[url].courses[i.string] = Course(i.string,int(link.get('id').split('.')[0]))
                            except:
                                pass

            self.colored_canvas.configure(bg='green') # when the whole fetching process is finished
        except:pass

    def search_button(self):
        try:
            self.tv.delete(*self.tv.get_children()) # for clearing the treeview widget first
            results = self.get_matching_results()
            rankings = self.getscoredlist(results)
            x=1
            sorted_lst = sorted(rankings, key=rankings.get,reverse=True)  # this provides a list of decreasingly scored departments
            for dept in sorted_lst: # inserting the ranked results in the tv widget
                dept_name = self.undergraduate[dept].name
                score = rankings[dept]
                self.tv.insert('', END, values=(x, dept_name, round(score,2)))
                x+=1
        except:pass


    def normalizescores(self,scores,smallIsBetter=0): # this fucntion is borrowed from mysearchengine.py to normalize the scores
        vsmall = 0.00001 # Avoid division by zero errors
        if smallIsBetter:
            minscore=min(scores.values())
            minscore=max(minscore, vsmall)
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                         in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0:
                maxscore = vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def getscoredlist(self, results):
        # try:
        ranked = {}
        weights = []
        for i in range(3): # checking for the three check buttons
            if self.lst_of_vars[i].get() == 'on': # if it was checked
                if i == 0: # if it was the first cb
                    weights.append(self.text_based_search(results))
                elif i ==1: # second
                    weights.append(self.semester_based_search(results))
                elif i == 2: # third
                    weights.append(self.hubscore())
        if len(weights) == 1: # if there was only ONE check button clicked
            return weights[0]
        elif weights == []: # if the user wanted to search only without the ranking
            results = self.get_matching_results()
            set_of_depts = set()
            for word in results:
                for dept in results[word]:
                    set_of_depts.add(dept)
            for dept in set_of_depts:
                ranked[dept] = 1.0
            return ranked
        else: # if more metrics were clicked in the cb
            urls = weights[0].keys()
            summed_scores = [] # list
            lst = [] # lst of tuples as scores for each metric
            for dictionary in weights:
                lst.append(dictionary.values())
            to_be_summed = zip(*lst) # zipping the scores together for later summation (score of first dept + score of second dept + ..... )
            for scores in to_be_summed:
                summed_scores.append(sum(scores))
            for i in range(len(weights[0])):
                ranked[urls[i]] = summed_scores[i]
            return ranked
        # except:pass

    def get_matching_results(self):
        results = {}
        lst_of_words = self.txt_widget.get('1.0',END).split(',') # there will be a \n in the last word (to be stripped)
        for word in lst_of_words:
            results.setdefault(word.strip(),[])
            for dept_url in self.undergraduate:
                for course in self.undergraduate[dept_url].courses:
                    try:
                        if word.encode('utf8').strip().lower() in course.encode('utf8').strip().lower() and dept_url not in results[word.strip()]:
                            results[word.strip()] += [dept_url]
                    except:pass
        return results # returns a dictionary of keys as words, and a list of urls that this word appears in its courses

    def text_based_search(self,results):
        counts = {} # dictionary of dept as a key and number of word frequencies as a value
        for word in results:
            for dept in results[word]: # dept here is the url of the dept
                score = 0
                for course in self.undergraduate[dept].courses:
                    try:
                        if word.encode('utf8').strip().lower() in course.encode('utf8').strip().lower():
                            score += 1
                    except:pass
                if dept in counts:
                    counts[dept] += score
                else:
                    counts[dept] = score
        return self.normalizescores(counts,smallIsBetter=False)

    def semester_based_search(self,results):
        counts = {}  # dictionary of dept as a key and max number of semester as a value
        for word in results:
            for dept in results[word]:  # dept here is the url of the dept
                set_of_semesters = set()
                for course in self.undergraduate[dept].courses:
                    try:
                        if word.encode('utf8').strip().lower() in course.encode('utf8').strip().lower():
                            set_of_semesters.add(self.undergraduate[dept].courses[course].semester)
                    except:pass
                if dept in counts:
                    counts[dept] += max(set_of_semesters)  # summing the scores in case there were two or more queries
                else:
                    counts[dept] = max(set_of_semesters)
        return self.normalizescores(counts, smallIsBetter=False)

    def hubscore(self):
        lst = [] # this will include all depts which are resulted from the search items
        counts = {}
        dict = {} # this will be a dictionary where dept is a key, and a nested dict is its value containing compared depts as keys and their score as value (score is the number of shared courses)
        results = self.get_matching_results()
        set_of_depts = set()
        for word in results:
            for dept in results[word]:
                set_of_depts.add(dept)
        for dept in set_of_depts:
            lst.append(dept)
        for dept in set_of_depts:
            dict.setdefault(dept,{})
            for compared_dept in set_of_depts:
                if compared_dept != dept:
                    for course in self.undergraduate[compared_dept].courses:
                        courses = self.undergraduate[dept].courses.keys()
                        if course in courses:
                            dict[dept].setdefault(compared_dept, 0)
                            dict[dept][compared_dept] += 1

        for dept in dict: # to finalize our work and append the depts with their scores in the dictionary
            score = 0
            for compared_dept in dict[dept]:
                score += (len(dict[compared_dept])*dict[dept][compared_dept])
            score /= float(len(dict[dept]))
            counts[dept] = score
        return self.normalizescores(counts,smallIsBetter=False)







app = GUI()
root.mainloop()