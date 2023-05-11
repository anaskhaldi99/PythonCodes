from Tkinter import *
from bs4 import BeautifulSoup
import urllib2
import docclass
root = Tk()

class Course(object):
    def __init__(self,code,name):
        self.code = code
        self.name = name

class Classified_courses(object):
    def __init__(self):
        self.categories = {} # key as category, value as list of courses in that category (for analysis part)
class GUI(object):
    def __init__(self):
        self.initGUI()
        self.courses = {} # keys are course codes, values are Course class objects
        # self.courses_dict = {} # keys as course codes having a value of 1


    def initGUI(self):
        frame1 = Frame(root)
        frame1.grid(sticky=NSEW)
        frame2 = Frame(root)
        frame2.grid(row=1,column=0,sticky=NSEW)
        self.frame3 = Frame(root)
        self.frame3.grid(row=2,column=0,sticky=NSEW)
        frame4 = Frame(root)
        frame4.grid(row=3,column=0,pady=20,sticky=NSEW)

        title_label = Label(frame1, text='COURSE PROGRAM ESTIMATOR', bg='light green', fg='black',font=('', '18', 'bold'))
        title_label.grid(sticky=NSEW,columnspan=2)

        training_data_label = Label(frame1,text='Training Data:',font=('','12',''))
        training_data_label.grid(row=1,column=0,pady=8,padx=(60,0))

        self.entry = Entry(frame1,width=80)
        self.entry.grid(row=1,column=1,pady=8,padx=(0,15))
        self.entry.insert(END, 'https://www.sehir.edu.tr/tr/duyurular/2017-2018-Akademik-Yili-Ders-Programi')

        self.colored_canvas = Canvas(frame2, width=70, height=20, bg='red')
        self.colored_canvas.grid(padx=(250,0),pady=(0,10))

        self.train_button = Button(frame2,text='Fetch and Train',height=1,width=14,command=self.fetch_and_train_button)
        self.train_button.grid(row=0,column=1,padx=(70,0),pady=(0,10))

        self.individual_courses_label = Label(self.frame3,text='Individual Courses:',font=('','11','bold'))
        self.individual_courses_label.grid(padx=(65,0),sticky=W)

        self.courses_lstbx_sb = Scrollbar(self.frame3)
        self.courses_lstbx_sb.grid(row=1,column=1,sticky=NS,rowspan=3)

        self.courses_lstbx = Listbox(self.frame3,selectmode='single',width=32,height=8,yscrollcommand=self.courses_lstbx_sb)
        self.courses_lstbx.bind('<<ListboxSelect>>',self.onclick) # binding the listbox selection to a function
        self.courses_lstbx_sb.configure(command=self.courses_lstbx.yview)
        self.courses_lstbx.grid(row=1,column=0,padx=(65,0),rowspan=3)

        top3_estimates_label = Label(self.frame3,text='Top 3 Estimates:',font=('','11','bold'))
        top3_estimates_label.grid(row=0,column=2)

        self.canvas1 = Canvas(self.frame3,width=200,height=40)
        self.canvas1.grid(row=1,column=2,padx=(85,0))

        self.canvas2 = Canvas(self.frame3,width=200,height=40)
        self.canvas2.grid(row=2,column=2,padx=(85,0))

        self.canvas3 = Canvas(self.frame3,width=200,height=40)
        self.canvas3.grid(row=3,column=2,padx=(85,0))

        analysis_label = Label(frame4,text='Accuracy Analysis \n Based on Programs:',font=('','10','bold'))
        analysis_label.grid(padx=(65,0),pady=(35,0))

        self.programs_lstbx_sb = Scrollbar(frame4)
        self.programs_lstbx_sb.grid(row=1,column=2,sticky=NS,pady=12)

        self.programs_lstbx = Listbox(frame4,width=23,height=9,yscrollcommand=self.programs_lstbx_sb,selectmode='single')
        self.programs_lstbx.bind('<<ListboxSelect>>',self.onclick2)
        self.programs_lstbx_sb.configure(command=self.programs_lstbx.yview)
        self.programs_lstbx.grid(row=1,column=0,padx=(65,0),pady=12,sticky=NSEW)

        self.txt_widget_sb = Scrollbar(frame4)
        self.txt_widget_sb.grid(row=0,column=4,sticky=NS,rowspan=2)

        self.txt_widget = Text(frame4,width=40,height=15,yscrollcommand=self.txt_widget_sb)
        self.txt_widget_sb.configure(command=self.txt_widget.yview)
        self.txt_widget.grid(row=0,column=3,rowspan=2,padx=(65,0),sticky=NSEW)

    def fetch_and_train_button(self):
        # calling out methods in precedence order
        self.fetching()
        self.training()
        courses = self.courses.keys() # lst of all courses
        courses.sort() # alpha order
        for course in courses: # appending the courses into the first lstbx
            self.courses_lstbx.insert(END,course+' ('+self.courses[course].name+')')
        cats = self.categorized.categories.keys() # lst of categories
        cats.sort() # alpha order
        for category in cats: # inserting into the second lstbx
            self.programs_lstbx.insert(END,category)

    def fetching(self):
        link = self.entry.get()
        self.colored_canvas.configure(bg='yellow')  # changing the canvas color to yellow during the process
        self.colored_canvas.update()
        site = urllib2.urlopen(link)
        contents = site.read()
        soup = BeautifulSoup(contents, 'html.parser')
        lst_of_course_codes = []
        lst_of_course_names = []
        x = 0 # variable used to filter out just the courses ONLY from the rest even columns
        for i in soup.find_all('td',{'class':'ms-rteTableEvenCol-13'}):
            if x%3 == 0 and x!=0: # this filter is applied just to extract the course codes only
                lst_of_course_codes.append(i.string) # appending the course code
            x += 1
        n = 0 # variable used to extract the course names ONLY from the rest odd columns
        for i in soup.find_all('td',{'class':'ms-rteTableOddCol-13'}):
            if n%3 == 0 and n!=0: # this filter is applied just to extract the course names only
                lst_of_course_names.append(i.string)
            n += 1
        for i in range(len(lst_of_course_codes)): # adding all the fetched UNIQUE courses into the courses dictionary for further usages
            try:
                splitted = [lst_of_course_codes[i].split()[0]] + [lst_of_course_codes[i].split()[1]]
                course_code = ' '.join(splitted)
                if course_code not in self.courses:
                    course_name = lst_of_course_names[i].split('(')[0]
                    self.courses[course_code] = Course(course_code,course_name)
                else:pass
            except:pass
        self.categorized = Classified_courses() # creating the Classified_courses instance
        for course in self.courses:
            cat = course.split()[0]
            self.categorized.categories.setdefault(cat,[])
            self.categorized.categories[cat].append(course)
        self.colored_canvas.configure(bg='green')

    def training(self): # training function
        self.classified = docclass.naivebayes(docclass.getwords) # creating the classifier class object
        for course in self.courses:
            for cat in self.categorized.categories:
                if course in self.categorized.categories[cat]:
                    self.classified.train(self.courses[course].name,cat) # training the program name with its belonging category

    def classify(self,course): # function used for returning a dict of categories and their probabilities for a certain course (name)
        d = {}
        for cat in self.classified.categories():
            prob = self.classified.prob(course, cat)
            d[cat] = prob
        return d

    def classify2(self,course): # same as above function, but stores probabilities as keys instead of values (reverterd) (used for second lstbx function)
        d = {}
        for cat in self.classified.categories():
            prob = self.classified.prob(course, cat)
            d[prob] = cat
        return d

    def onclick(self,event):
        # canvases are created again every time to prevent any overlap in the content
        self.canvas1 = Canvas(self.frame3, width=200, height=40)
        self.canvas1.grid(row=1, column=2, padx=(85, 0))
        self.canvas2 = Canvas(self.frame3, width=200, height=40)
        self.canvas2.grid(row=2, column=2, padx=(85, 0))
        self.canvas3 = Canvas(self.frame3, width=200, height=40)
        self.canvas3.grid(row=3, column=2, padx=(85, 0))
        selection = self.courses_lstbx.get(self.courses_lstbx.curselection())
        course = selection.split('(')[1][:-1].strip() # acquiring the selected course NAME in the lstbx as a string
        lst = [] # used for preserving the sorting of the top3 dictionary (because a dictionary wont sort)
        best = selection.split()[0].strip() # acquiring the correct category of the course
        probs = self.classify(course)
        top3 = {} # dict used to store the top 3 matches for a course
        values = list(probs.values())
        for i in range(3): # loop for obtaining the top 3 ONLY
            m = values.pop(values.index(max(values)))
            for cat in probs:
                if probs[cat] == m and cat not in top3:
                    top3[cat] = m
                    break
        for cat in sorted(top3,key=top3.get,reverse=True):
            lst.append((cat,top3[cat]))
        x = 1 # used for determining which canvas to modify throughout the loop
        for tuple in lst:
            cat = tuple[0]
            prob = tuple[1]
            if x == 1: # first canvas
                self.canvas1.create_text(100,10,text=cat+':'+str('{0:.8f}'.format(prob)))
                if cat == best:
                    self.canvas1.configure(bg='green')
                else: self.canvas1.configure(bg='red')
            elif x == 2:
                self.canvas2.create_text(100, 10, text=cat+':'+str('{0:.8f}'.format(prob)))
                if cat == best:
                    self.canvas2.configure(bg='green')
                else: self.canvas2.configure(bg='red')
            elif x == 3:
                self.canvas3.create_text(100, 10, text=cat+':'+str('{0:.8f}'.format(prob)))
                if cat == best:
                    self.canvas3.configure(bg='green')
                else: self.canvas3.configure(bg='red')
            x += 1
    def onclick2(self,event):
        self.txt_widget.delete(1.0,END) # clearing the text widget first of all
        cat = self.programs_lstbx.get(self.programs_lstbx.curselection()).strip() # acquiring the selected category
        total_courses = float(self.classified.cc[cat]) # using the cc attribute to obtain the total courses in a certain cat
        # this is for checking accuracies
        lst_of_accurate = []
        lst_of_inaccurate = []
        d_of_inaccurate ={} # dictionary used for listing the inaccurate courses at the end
        for course_code in self.categorized.categories[cat]:
            course_name = self.courses[course_code].name
            probs = self.classify2(course_name)
            prediction = probs[max(probs)]
            if prediction == cat: # in case they match each others
                lst_of_accurate.append(course_name)
            else: # in case they dont match
                lst_of_inaccurate.append(course_name)
                d_of_inaccurate[course_code] = prediction
        accurate = len(lst_of_accurate) # number of accurate
        inaccurate = len(lst_of_inaccurate) # number of inaccurate
        accuracy = round((accurate/total_courses) * 100,2) # accuracy percentage
        # inserting the results into the text widget
        self.txt_widget.insert(END,'Accuracy: '+str(accuracy)+'%\n')
        self.txt_widget.insert(END,'  Total Number Of Courses: '+str(int(total_courses))+'\n')
        self.txt_widget.insert(END,'  Accurately Classified: '+str(accurate)+'\n')
        self.txt_widget.insert(END,'  Inaccurate Classification: '+str(inaccurate)+'\n')
        for course in d_of_inaccurate:
            self.txt_widget.insert(END,'\t'+course+' --> '+d_of_inaccurate[course]+'\n')


























app = GUI()
root.mainloop()













