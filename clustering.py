from Tkinter import *
import xlrd
import tkFileDialog
import clusters
from PIL import ImageTk,Image
root = Tk()
root.geometry('800x800')

class Student:
    def __init__(self,name,ID,dept,GPA):
        self.name = name
        self.id = ID
        self.dept = dept
        self.GPA = GPA

class Course:
    def __init__(self,code,name,credit,grade,semester):
        self.code = code
        self.name = name
        self.credit = credit
        self.grade = grade
        self.semester = semester

class GUI:
    def __init__(self):
        self.initGUI()
        self.students = {} # student name as key, Student OBJECT as value
        self.students_courses = {} # student name as key, list of courses taken by this student as value (with course OBJECT as item in the list)
        self.courses_students = {} # course code as key, and list of students taking that course as value
        self.coursesdict = {} # key course code, value is course object
        self.courses = [] # lst of all courses codes
        self.letter_grades = {'A+':4.1,'A':4.0,'A-':3.7,'B+':3.3,'B':3.0,'B-':2.7,'C+':2.3,'C':2.0,'C-':1.7,'D+':1.3,'D':1.0,'D-':0.5,'F':0}
        self.var = StringVar() # used to differentiate between the functions of the three buttons and execute accordingly
        self.leaf_nodes = [] # list which stores all the leaf nodes in a certain cluster
        self.students_data1 = {} # student is the key, vec list (data) is the value
        self.students_data2 = {} # student is the key, vec list (data) is the vlaue (this is for the second button)
        self.students_data3 = {} # course id is the key, vec list (data) is the value (this is for the third button)
        self.depts = ['Computer Science and Engineering Department','Electrical and Electronics Engineering Department','Industrial Engineering Department']

    def initGUI(self):
        frame = Frame(root)
        frame2 = Frame(root)
        frame.pack(fill=BOTH)
        frame2.pack()

        self.title_label = Label(frame,text='Student Course Data Clustering Analysis Tool v. 1.0',bg='red',fg='white',font=('','16','bold'))
        self.title_label.pack(fill=BOTH)

        self.loading_button = Button(frame,text='Load Transcripts',height=2,width=28,command=self.loading_button)
        self.loading_button.pack(pady=10)

        self.students_clustering_button = Button(frame2, text='Cluster Students based on courses', width=28, height=2,command = self.students_clustering)
        self.students_clustering_button.grid(padx=(80,0))

        self.GPA_clustering_button = Button(frame2,text='Cluster Students Based on GPA',width=28,height=2,command=self.GPA_clustering)
        self.GPA_clustering_button.grid(row=0,column=1)

        self.courses_clustering_button = Button(frame2,text='Cluster courses based on students',width=28,height=2,command=self.courses_clustering_button)
        self.courses_clustering_button.grid(row=0,column=2,padx=(0,80)) # adjust the padding distance over here

    def loading_button(self):
        try:
            self.filenames = tkFileDialog.askopenfilenames(initialdir="/",title="Choose Transcripts", filetypes=(('Excel files', '*.xlsx;*.xls'), ('all files', '*.*')))
            for transcript in self.filenames: # self.filenames is a list of all the chosen file paths in the dialouge
                book = xlrd.open_workbook(transcript.encode('utf8')) # opens the excel file
                sheet = book.sheet_by_name('Sheet1') # opens the desired sheet in the file
                self.students[sheet.cell(0,1).value] = Student(sheet.cell(0,1).value,sheet.cell(0,0).value,sheet.cell(0,2).value,sheet.cell(0,3).value) # appending the keys (student names) and values (Student class instances) from the sheet
                for row in range(2,sheet.nrows): # n.rows is the total number of rows in the sheet
                    student = sheet.cell(0,1).value
                    course_code = sheet.cell(row,0).value
                    course_name = sheet.cell(row,1).value
                    grade = sheet.cell(row,2).value
                    credit = sheet.cell(row,3).value
                    semester = sheet.cell(row,4).value
                    self.courses_students.setdefault(course_code, []) # preparing the list of students taking that course (initially empty)
                    if course_code not in self.courses: # adding all distinct courses into the courses list
                        self.courses.append(course_code)
                    if grade != '' : # in case there was a grade in the cell (the student has taken that course)
                        self.students_courses.setdefault(sheet.cell(0,1).value,[]) # adding student name as key and initially empty list as a value
                        self.students_courses[sheet.cell(0,1).value] += [Course(course_code,course_name,credit,grade,semester)] # adding the Course class instance into the list (value)
                        self.coursesdict[course_code] = Course(course_code,course_name,credit,grade,semester) # adding the course id as key and Course class instance as value
                        self.courses_students[course_code] += [student] # adding the student who has taken that course to the list of students taking it too (value)
            with open('matrix1.txt','w') as matrix: # creating the matrix through opening a new text file and writing into it
                matrix.write('\t')
                for course in self.courses: # writing the column labels
                    if course == self.courses[-1]:
                        matrix.write(course+'\n')
                    else:
                        matrix.write(course+'\t')
                for student in self.students_courses: # writing the row labels along with their data (in the same line)
                    studentname = student.replace('\t',' ')
                    matrix.write(studentname+' '+'('+self.students[student].dept+')'+'\t')
                    lst_of_courses = []
                    for course in self.students_courses[student]: # creating a list of all the course codes that the student has taken
                        coursecode = course.code
                        lst_of_courses.append(coursecode)
                    for course in self.courses:
                        if course in lst_of_courses:
                            if course == self.courses[-1]: # if it was the last column
                                matrix.write('1\n')
                            else: # if it was still in the middle
                                matrix.write('1\t')
                        else:
                            if course == self.courses[-1]:
                                matrix.write('0\n')
                            else:
                                matrix.write('0\t')
            with open('matrix2.txt','w') as matrix: # same as applied to matrix 1
                matrix.write('\t')
                for course in self.courses:
                    if course == self.courses[-1]:
                        matrix.write(course+'\n')
                    else:
                        matrix.write(course+'\t')
                for student in self.students_courses:
                    studentname = student.replace('\t',' ')
                    matrix.write(studentname+' '+'('+str(self.students[student].GPA)+')'+'\t')
                    dict_of_courses = {} # key is course code, value is course grade
                    for course in self.students_courses[student]: # creating a dictionary of all the course codes that the student has taken
                        coursecode = course.code
                        coursegrade = course.grade
                        dict_of_courses[coursecode] = coursegrade.strip()
                    for course in self.courses:
                        if course in dict_of_courses:
                            if course == self.courses[-1]:
                                matrix.write(str(self.letter_grades[dict_of_courses[course]])+'\n')
                            else:
                                matrix.write(str(self.letter_grades[dict_of_courses[course]]) + '\t')
                        else:
                            if course == self.courses[-1]:
                                matrix.write('0\n')
                            else:
                                matrix.write('0\t')
            with open('matrix3.txt','w') as matrix: # same as applied in matrix 2
                matrix.write('\t')
                students = self.students.keys()
                for student in students:
                    if student == students[-1]:
                        matrix.write(student + '\n')
                    else:
                        matrix.write(student + '\t')
                for course in self.courses:
                    matrix.write(course + '\t')
                    lst_of_students = []
                    try:
                        for student in self.courses_students[course]:  # creating a list of all the student names that the course has been taken by them
                            lst_of_students.append(student)
                    except:
                        pass
                    for student in self.students.keys():
                        if student in lst_of_students:
                            if student == self.students.keys()[-1]:
                                matrix.write('1\n')
                            else:
                                matrix.write('1\t')
                        else:
                            if student == self.students.keys()[-1]:
                                matrix.write('0\n')
                            else:
                                matrix.write('0\t')
        except:pass

    def students_clustering(self):
        self.var.set('students') # updating the variable so that it behaves accordingly in the analysis part
        try: # this is used to avoid creating more unnecessary widgets in the interface
            self.frame3.destroy()
            self.frame4.destroy()
            self.frame5.destroy()
            self.frame6.destroy()
            self.frame7.destroy()
        except:
            pass
        students,courses,data = clusters.readfile('matrix1.txt')
        self.clust1 = clusters.hcluster(data) # root clust object
        clusters.drawdendrogram(self.clust1,students)
        pic = Image.open('clusters.jpg') # opening the image created by the dendogram function

        i = 0 # this is used to store all the rows with its data list in a dictionary for later usages in the analysis (USED THROUGHOUT THE REST PARTS)
        for student in students:
            self.students_data1[student] = data[i]
            i += 1
        # Adding the analysis widgets
        self.frame3 = Frame(root)
        self.frame4 = Frame(root)
        self.frame5 = Frame(root)
        self.frame6 = Frame(root)
        self.frame7 = Frame(root)
        self.frame3.pack(padx=40)
        self.frame4.pack(padx=40,fill=X)
        self.frame5.pack()
        self.frame6.pack()
        self.frame7.pack(padx=34)

        vscroll = Scrollbar(self.frame3,orient=VERTICAL)
        vscroll2 = Scrollbar(self.frame7,orient=VERTICAL)
        hscroll = Scrollbar(self.frame4,orient=HORIZONTAL)

        canvas = Canvas(self.frame3,width=700,height=250,scrollregion=(0,0,1300,1300))
        canvas.image = ImageTk.PhotoImage(pic)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')
        vscroll.configure(command=canvas.yview)
        hscroll.configure(command=canvas.xview)
        canvas.configure(yscrollcommand=vscroll.set,xscrollcommand=hscroll.set)
        canvas.pack(side=LEFT)
        vscroll.pack(side=LEFT,fill=Y)
        hscroll.pack(fill=X)

        cutting_pt_label = Label(self.frame5,text='Cutting point')
        self.entry1 = Entry(self.frame5,width=6)
        analysis_button = Button(self.frame5,text = 'Run analysis',width=26,height=2,command=self.analysis_button)
        clusters_label = Label(self.frame6,text='Clusters:')
        self.clusters_lstbx1 = Listbox(self.frame6,selectmode='single',width=50)
        self.clusters_lstbx1.bind('<<ListboxSelect>>', self.on_event) # binding this event to the fucntion
        cluster_details_label = Label(self.frame6,text='Cluster Details:')
        self.txt_widget1 = Text(self.frame7,yscrollcommand=vscroll2.set,width=88)
        vscroll2.configure(command=self.txt_widget1.yview)
        cutting_pt_label.pack(side=LEFT)
        self.entry1.pack(side=LEFT)
        analysis_button.pack(side=LEFT)
        clusters_label.pack()
        self.clusters_lstbx1.pack()
        cluster_details_label.pack()
        self.txt_widget1.pack(side=LEFT)
        vscroll2.pack(side=LEFT,fill=Y)


    def GPA_clustering(self):
        self.var.set('GPA') # updating the variable
        try:
            self.frame3.destroy()
            self.frame4.destroy()
            self.frame5.destroy()
            self.frame6.destroy()
            self.frame7.destroy()
        except:
            pass
        students,courses,data = clusters.readfile('matrix2.txt')
        self.clust2 = clusters.hcluster(data)
        clusters.drawdendrogram(self.clust2,students,jpeg='clusters2.jpg')
        pic = Image.open('clusters2.jpg')

        i = 0
        for student in students:
            self.students_data2[student] = data[i]
            i += 1

        self.frame3 = Frame(root)
        self.frame4 = Frame(root)
        self.frame5 = Frame(root)
        self.frame6 = Frame(root)
        self.frame7 = Frame(root)
        self.frame3.pack(padx=40)
        self.frame4.pack(padx=40, fill=X)
        self.frame5.pack()
        self.frame6.pack()
        self.frame7.pack(padx=34)

        vscroll = Scrollbar(self.frame3,orient=VERTICAL)
        vscroll2 = Scrollbar(self.frame7, orient=VERTICAL)
        hscroll = Scrollbar(self.frame4,orient=HORIZONTAL)

        canvas = Canvas(self.frame3,width=700,height=250,scrollregion=(0,0,1300,1300))
        canvas.image = ImageTk.PhotoImage(pic)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')
        vscroll.configure(command=canvas.yview)
        hscroll.configure(command=canvas.xview)
        canvas.configure(yscrollcommand=vscroll.set,xscrollcommand=hscroll.set)
        canvas.pack(side=LEFT)
        vscroll.pack(side=LEFT,fill=Y)
        hscroll.pack(fill=X)

        cutting_pt_label = Label(self.frame5, text='Cutting point')
        self.entry2 = Entry(self.frame5, width=6)
        analysis_button = Button(self.frame5, text='Run analysis', width=26, height=2,command=self.analysis_button)
        clusters_label = Label(self.frame6, text='Clusters:')
        self.clusters_lstbx2 = Listbox(self.frame6, selectmode='single', width=50)
        self.clusters_lstbx2.bind('<<ListboxSelect>>', self.on_event) # binding the event to the function
        cluster_details_label = Label(self.frame6, text='Cluster Details:')
        self.txt_widget2 = Text(self.frame7, yscrollcommand=vscroll2.set, width=88)
        vscroll2.configure(command=self.txt_widget2.yview)
        cutting_pt_label.pack(side=LEFT)
        self.entry2.pack(side=LEFT)
        analysis_button.pack(side=LEFT)
        clusters_label.pack()
        self.clusters_lstbx2.pack()
        cluster_details_label.pack()
        self.txt_widget2.pack(side=LEFT)
        vscroll2.pack(side=LEFT, fill=Y)

        # Analysis part

    def courses_clustering_button(self):
        self.var.set('courses')
        try:
            self.frame3.destroy()
            self.frame4.destroy()
            self.frame5.destroy()
            self.frame6.destroy()
            self.frame7.destroy()
        except:
            pass
        courses,students,data = clusters.readfile('matrix3.txt')
        self.clust3 = clusters.hcluster(data)
        clusters.drawdendrogram(self.clust3,courses,jpeg='clusters3.jpg')
        pic = Image.open('clusters3.jpg')

        i = 0
        for course in courses:
            self.students_data3[course] = data[i]
            i += 1

        self.frame3 = Frame(root)
        self.frame4 = Frame(root)
        self.frame5 = Frame(root)
        self.frame6 = Frame(root)
        self.frame7 = Frame(root)
        self.frame3.pack(padx=40)
        self.frame4.pack(padx=40, fill=X)
        self.frame5.pack()
        self.frame6.pack()
        self.frame7.pack(padx=34)

        vscroll = Scrollbar(self.frame3,orient=VERTICAL)
        vscroll2 = Scrollbar(self.frame7, orient=VERTICAL)
        hscroll = Scrollbar(self.frame4,orient=HORIZONTAL)

        canvas = Canvas(self.frame3,width=700,height=250,scrollregion=(0,0,1300,1300))
        canvas.image = ImageTk.PhotoImage(pic)
        canvas.create_image(0, 0, image=canvas.image, anchor='nw')
        vscroll.configure(command=canvas.yview)
        hscroll.configure(command=canvas.xview)
        canvas.configure(yscrollcommand=vscroll.set,xscrollcommand=hscroll.set)
        canvas.pack(side=LEFT)
        vscroll.pack(side=LEFT,fill=Y)
        hscroll.pack(fill=X)

        cutting_pt_label = Label(self.frame5, text='Cutting point')
        self.entry3 = Entry(self.frame5, width=6)
        analysis_button = Button(self.frame5, text='Run analysis', width=26, height=2,command=self.analysis_button)
        clusters_label = Label(self.frame6, text='Clusters:')
        self.clusters_lstbx3 = Listbox(self.frame6, selectmode='single', width=50)
        self.clusters_lstbx3.bind('<<ListboxSelect>>', self.on_event)
        cluster_details_label = Label(self.frame6, text='Cluster Details:')
        self.txt_widget3 = Text(self.frame7, yscrollcommand=vscroll2.set, width=88)
        vscroll2.configure(command=self.txt_widget3.yview)
        cutting_pt_label.pack(side=LEFT)
        self.entry3.pack(side=LEFT)
        analysis_button.pack(side=LEFT)
        clusters_label.pack()
        self.clusters_lstbx3.pack()
        cluster_details_label.pack()
        self.txt_widget3.pack(side=LEFT)
        vscroll2.pack(side=LEFT, fill=Y)

        # Analysis Part
    def analysis_button(self):
        try:
            if self.var.get() == 'students': # if the interface was showing the first picture (first button)
                self.departments = {}  # key is the cluster number, value is another nested dictionary with departments as keys and number of students as values
                self.lstbx_clusters = {}  # key is the cluster number, value is a list of [dept,total num of students,percentage]
                self.clusters_students = {}  # key is the cluster number, value is a list of all students under that cluster
                self.clusters_lstbx1.delete(0,END) # clearing the lstbox
                n = int(self.entry1.get())
                self.lst_of_clusters1 = []
                self.lst_of_leafs1 = []
                if n == 0:
                    self.lst_of_clusters1.append(self.clust1)
                else:
                    current_clust = [self.clust1]
                    self.lst_of_clusters1 = self.analysis_cut(current_clust)

                x = 0
                for clust in self.lst_of_clusters1:
                    if clust.id > 0:
                        for student in self.students_data1:
                            if self.students_data1[student] == clust.vec:
                                student_name = student.split('(')[0].strip()
                                dept = student.split('(')[-1][0:-1]
                                num = '1'
                                percentage = '100%'
                                self.clusters_lstbx1.insert(END,'cluster'+str(x)+'('+dept+')'+'('+num+')'+'('+percentage+')')
                                self.lstbx_clusters.setdefault(x,[])
                                self.lstbx_clusters[x] = [dept,num,percentage]
                                self.departments.setdefault(x,{})
                                self.departments[x].setdefault(dept, 0)
                                self.departments[x][dept] += 1
                                self.clusters_students.setdefault(x,[])
                                self.clusters_students[x] += [student_name]

                    else:
                        lst_of_students = self.cluster_cut([clust])
                        total_students = float(len(lst_of_students))
                        for clust in lst_of_students:
                            for student in self.students_data1:
                                if self.students_data1[student] == clust.vec:
                                    student_name = student.split('(')[0].strip()
                                    dept = student.split('(')[-1][0:-1]
                                    self.departments.setdefault(x,{})
                                    self.departments[x].setdefault(dept,0)
                                    self.departments[x][dept] += 1
                                    self.clusters_students.setdefault(x,[])
                                    self.clusters_students[x] += [student_name]
                        for dept in self.departments[x]:
                            if self.departments[x][dept] == max(self.departments[x].values()):
                                maxdept = dept
                                test_percentage = '{:.0%}'.format(self.departments[x][maxdept]/total_students)
                                if int(test_percentage.split('%')[0]) > 100:
                                    percentage = '100%'
                                else:
                                    percentage = test_percentage
                                self.lstbx_clusters[x] = [maxdept,str(int(total_students)),percentage]
                                self.clusters_lstbx1.insert(END,'cluster'+str(x)+'('+maxdept+')'+'('+str(int(total_students))+')'+'('+percentage+')')
                    x += 1

            elif self.var.get() == 'GPA':
                self.GPA = {}  # key is the cluster number, value is another nested dictionary with GPA level as keys and number of students as values
                self.lstbx_clusters2 = {}  # key is the cluster number, value is a list of [max_GPA,total num of students,percentage]
                self.clusters_students2 = {}  # key is the cluster number, value is a list of all students under that cluster
                self.clusters_lstbx2.delete(0, END)
                n = int(self.entry2.get())
                self.lst_of_clusters2 = []
                self.lst_of_leafs2 = []
                if n == 0:
                    self.lst_of_clusters2.append(self.clust2)
                else:
                    current_clust = [self.clust2]
                    self.lst_of_clusters2 = self.analysis_cut(current_clust)

                x = 0
                for clust in self.lst_of_clusters2:
                    if clust.id > 0:
                        for student in self.students_data2:
                            if self.students_data2[student] == clust.vec:
                                student_name = student.split('(')[0].strip()
                                GPA = float(student.split('(')[-1][0:-1])
                                if GPA >= 3.5:
                                    GPA_level = 'High GPA'
                                elif GPA < 3.5 and GPA >= 2.75:
                                    GPA_level = 'Medicore GPA'
                                elif GPA < 2.75:
                                    GPA_level = 'Poor GPA'
                                num = '1'
                                percentage = '100%'
                                self.clusters_lstbx2.insert(END, 'cluster' + str(x) + '(' + GPA_level + ')' + '(' + num + ')' + '(' + percentage + ')')
                                self.lstbx_clusters2.setdefault(x, [])
                                self.lstbx_clusters2[x] = [GPA_level, num, percentage]
                                self.GPA.setdefault(x, {})
                                self.GPA[x].setdefault(GPA_level, 0)
                                self.GPA[x][GPA_level] += 1
                                self.clusters_students2.setdefault(x, [])
                                self.clusters_students2[x] += [student_name]
                    else:
                        lst_of_students = self.cluster_cut([clust])
                        total_students = float(len(lst_of_students))
                        for clust in lst_of_students: # clust here is a leaf node
                            for student in self.students_data2:
                                if self.students_data2[student] == clust.vec:
                                    student_name = student.split('(')[0].strip()
                                    GPA = float(student.split('(')[-1][0:-1])
                                    if GPA >= 3.5:
                                        GPA_level = 'High GPA'
                                    elif GPA < 3.5 and GPA >= 2.75:
                                        GPA_level = 'Medicore GPA'
                                    elif GPA < 2.75:
                                        GPA_level = 'Poor GPA'
                                    self.GPA.setdefault(x, {})
                                    self.GPA[x].setdefault(GPA_level, 0)
                                    self.GPA[x][GPA_level] += 1
                                    self.clusters_students2.setdefault(x, [])
                                    self.clusters_students2[x] += [student_name]
                        for GPA_level in self.GPA[x]:
                            if self.GPA[x][GPA_level] == max(self.GPA[x].values()):
                                maxGPA_level = GPA_level
                                test_percentage = '{:.0%}'.format(self.GPA[x][maxGPA_level]/total_students)
                                if int(test_percentage.split('%')[0]) > 100:
                                    percentage = '100%'
                                else:
                                    percentage = test_percentage
                                self.lstbx_clusters2[x] = [maxGPA_level,str(int(total_students)),percentage]
                                self.clusters_lstbx2.insert(END,'cluster'+str(x)+'('+maxGPA_level+')'+'('+str(int(total_students))+')'+'('+percentage+')')
                    x += 1

            elif self.var.get() == 'courses':
                self.departments3 = {}  # key is the cluster number, value is another nested dictionary with GPA level as keys and number of students as values
                self.lstbx_clusters3 = {}  # key is the cluster number, value is a list of [max_dept,total num of students,percentage]
                self.clusters_students3 = {}  # key is the cluster number, value is a list of all courses under that cluster
                self.clusters_lstbx3.delete(0, END)
                n = int(self.entry3.get())
                self.lst_of_clusters3 = []
                self.lst_of_leafs3 = []
                if n == 0:
                    self.lst_of_clusters3.append(self.clust3)
                else:
                    current_clust = [self.clust3]
                    self.lst_of_clusters3 = self.analysis_cut(current_clust)

                x = 0
                for clust in self.lst_of_clusters3:
                    if clust.id > 0:
                        for course in self.students_data3:
                            if self.students_data3[course] == clust.vec:
                                total_students = float(len(self.courses_students[course]))
                                for student in self.courses_students[course]:
                                    self.departments3.setdefault(x, {})
                                    self.departments3[x].setdefault(self.students[student].dept, 0)
                                    self.departments3[x][self.students[student].dept] += 1
                                for dept in self.departments3[x]:
                                    if self.departments3[x][dept] == max(self.departments3[x].values()):
                                        maxdept = dept
                                        test_percentage = '{:.0%}'.format(self.departments3[x][maxdept] / total_students)
                                        if int(test_percentage.split('%')[0]) > 100:
                                            percentage = '100%'
                                        else:
                                            percentage = test_percentage
                                        self.lstbx_clusters3.setdefault(x, [])
                                        self.lstbx_clusters3[x] = [maxdept, str(int(total_students)), percentage]
                                        self.clusters_lstbx3.insert(END, 'cluster' + str(x) + '(' + maxdept + ')' + '(' + str(int(total_students)) + ')' + '(' + percentage + ')')
                                self.clusters_students3.setdefault(x, [])
                                self.clusters_students3[x] += [course]
                    else:
                        lst_of_courses = self.cluster_cut([clust])
                        number = len(lst_of_courses)
                        total_students = 0.0
                        for clust in lst_of_courses:
                            for course in self.students_data3:
                                if self.students_data3[course] == clust.vec:
                                    total_students += len(self.courses_students[course])
                        for clust in lst_of_courses:
                            for course in self.students_data3:
                                if self.students_data3[course] == clust.vec:
                                    for student in self.courses_students[course]:
                                        self.departments3.setdefault(x, {})
                                        self.departments3[x].setdefault(self.students[student].dept, 0)
                                        self.departments3[x][self.students[student].dept] += 1
                                        self.clusters_students3.setdefault(x, [])
                                        self.clusters_students3[x] += [course]
                        for dept in self.departments3[x]:
                            if self.departments3[x][dept] == max(self.departments3[x].values()):
                                maxdept = dept
                                test_percentage = '{:.0%}'.format(
                                    self.departments3[x][maxdept] / total_students)
                                if int(test_percentage.split('%')[0]) > 100:
                                    percentage = '100%'
                                else:
                                    percentage = test_percentage
                                self.lstbx_clusters3.setdefault(x, [])
                                self.lstbx_clusters3[x] = [maxdept, str(number), percentage]
                                self.clusters_lstbx3.insert(END, 'cluster' + str(x) + '(' + maxdept + ')' + '(' + str(number) + ')' + '(' + percentage + ')')
                    x += 1
        except:pass

    def analysis_cut(self, current_clust): # method for analysing up  to a certain RANGE
        try:
            if self.var.get() == 'students':
                n = int(self.entry1.get())
                i = 0
                while True:
                    lst = []
                    for clust in current_clust:
                        try:
                            if clust.id >= 0:  # in case it was a leaf node
                                self.lst_of_leafs1.append(clust)
                            else:  # in case it was a clust
                                lst.append(clust.right)
                                lst.append(clust.left)
                        except:pass
                    i += 1
                    if i == n:
                        break
                    else:
                        current_clust = lst
                for leaf in self.lst_of_leafs1:
                    self.lst_of_clusters1.append(leaf)
                for clust in lst:
                    self.lst_of_clusters1.append(clust)
                return self.lst_of_clusters1
            elif self.var.get() == 'GPA':
                n = int(self.entry2.get())
                i = 0
                while True:
                    lst = []
                    for clust in current_clust:
                        try:
                            if clust.id >= 0:  # in case it was a leaf node
                                self.lst_of_leafs2.append(clust)
                            else:  # in case it was a clust
                                lst.append(clust.right)
                                lst.append(clust.left)
                        except:
                            pass
                    i += 1
                    if i == n:
                        break
                    else:
                        current_clust = lst
                for leaf in self.lst_of_leafs2:
                    self.lst_of_clusters2.append(leaf)
                for clust in lst:
                    self.lst_of_clusters2.append(clust)
                return self.lst_of_clusters2
            elif self.var.get() == 'courses':
                n = int(self.entry3.get())
                i = 0
                while True:
                    lst = []
                    for clust in current_clust:
                        try:
                            if clust.id >= 0:  # in case it was a leaf node
                                self.lst_of_leafs3.append(clust)
                            else:  # in case it was a clust
                                lst.append(clust.right)
                                lst.append(clust.left)
                        except:
                            pass
                    i += 1
                    if i == n:
                        break
                    else:
                        current_clust = lst
                for leaf in self.lst_of_leafs3:
                    self.lst_of_clusters3.append(leaf)
                for clust in lst:
                    self.lst_of_clusters3.append(clust)
                return self.lst_of_clusters3
        except:pass

    def cluster_cut(self,current_clust): # method for analysing up to the leaf nodes level
        self.leaf_nodes = []
        while True:
            lst = []
            for clust in current_clust:
                try:
                    if clust.id >= 0:  # in case it was a leaf node
                        self.leaf_nodes.append(clust)
                    else:  # in case it was a clust
                        lst.append(clust.right)
                        lst.append(clust.left)
                except:
                    pass
            if len(lst) == 0:
                break
            else:
                current_clust = lst
        return self.leaf_nodes


    def on_event(self,event): # fucntion which binds to the event of listbox selection
        try:
            if self.var.get() == 'students': # first button clicked
                self.txt_widget1.delete(1.0,END) # clearing the txt widgets
                selected = self.clusters_lstbx1.curselection()[0]
                self.txt_widget1.insert(END,'Cluster '+str(selected)+' has following number of students for each group:\n')
                try:self.txt_widget1.insert(END,'\tComputer Science and Engineering Department has '+str(self.departments[selected]['Computer Science and Engineering Department'])+' students.\n')
                except:self.txt_widget1.insert(END, '\tComputer Science and Engineering Department has 0 students.\n')
                try:self.txt_widget1.insert(END,'\tElectrical and Electronics Engineering Department has '+str(self.departments[selected]['Electrical and Electronics Engineering Department'])+' students.\n')
                except:self.txt_widget1.insert(END,'\tElectrical and Electronics Engineering Department has 0 students.\n')
                try:self.txt_widget1.insert(END,'\tIndustrial Engineering Department has '+str(self.departments[selected]['Industrial Engineering Department'])+' students.\n')
                except:self.txt_widget1.insert(END,'\tIndustrial Engineering Department has 0 students.\n')
                try:self.txt_widget1.insert(END,'\tManagement has '+str(self.departments[selected]['Management'])+' students.\n')
                except:self.txt_widget1.insert(END,'\tManagement has 0 students.\n')
                self.txt_widget1.insert(END,'For this cluster, the majority is '+str(self.lstbx_clusters[selected][0])+'.'+' This cluster\n')
                self.txt_widget1.insert(END,'\tincludes '+str(self.departments[selected][self.lstbx_clusters[selected][0]])+' students from '+str(self.lstbx_clusters[selected][0])+' out of '+str(self.lstbx_clusters[selected][1])+'. Hence,\n')
                self.txt_widget1.insert(END,'\tthe accuracy is '+self.lstbx_clusters[selected][2]+'.\n---------------- \nStudents list:\n')
                for student in self.clusters_students[selected]: # looping inside the list of student names in this list
                    try:self.txt_widget1.insert(END,'\t'+student+' ('+str(self.students[student.replace(' ','\t')].dept)+') '+'('+str(self.students[student.replace(' ','\t')].GPA)+')\n')
                    except:self.txt_widget1.insert(END,'\t'+student+' ('+str(self.students[student].dept)+') '+'('+str(self.students[student].GPA)+')\n')

            elif self.var.get() == 'GPA': # second button
                self.txt_widget2.delete(1.0, END)
                selected = self.clusters_lstbx2.curselection()[0]
                self.txt_widget2.insert(END, 'Cluster ' + str(selected) + ' has following number of students for each group:\n')
                try:self.txt_widget2.insert(END,'\tMedicore GPA has '+str(self.GPA[selected]['Medicore GPA'])+' students.\n')
                except:self.txt_widget2.insert(END, '\tMedicore GPA has 0 students.\n')
                try:self.txt_widget2.insert(END,'\tPoor GPA has '+str(self.GPA[selected]['Poor GPA'])+' students.\n')
                except:self.txt_widget2.insert(END,'\tPoor GPA has 0 students.\n')
                try:self.txt_widget2.insert(END,'\tHigh GPA has '+str(self.departments[selected]['High GPA'])+' students.\n')
                except:self.txt_widget2.insert(END,'\tHigh GPA has 0 students.\n')
                self.txt_widget2.insert(END, 'For this cluster, the majority is ' + str(self.lstbx_clusters2[selected][0]) + '.' + ' This cluster\n')
                self.txt_widget2.insert(END, '\tincludes ' + str(self.GPA[selected][self.lstbx_clusters2[selected][0]]) + ' students from ' + str(self.lstbx_clusters2[selected][0]) + ' out of ' + str(self.lstbx_clusters2[selected][1]) + '. Hence,\n')
                self.txt_widget2.insert(END, '\tthe accuracy is ' + self.lstbx_clusters2[selected][2] + '.\n---------------- \nStudents list:\n')
                for student in self.clusters_students2[selected]: # looping inside the list of student names in this list
                    try:self.txt_widget2.insert(END,'\t'+student+' ('+str(self.students[student.replace(' ','\t')].dept)+') '+'('+str(self.students[student.replace(' ','\t')].GPA)+')\n')
                    except:self.txt_widget2.insert(END,'\t'+student+' ('+str(self.students[student].dept)+') '+'('+str(self.students[student].GPA)+')\n')

            elif self.var.get() == 'courses': # third button
                self.txt_widget3.delete(1.0, END)
                selected = self.clusters_lstbx3.curselection()[0]
                self.txt_widget3.insert(END, 'Cluster ' + str(selected) + ' has following number of students for each department:\n')
                try:self.txt_widget3.insert(END,'\tNumber of students from Computer Science and Engineering Department is '+str(self.departments3[selected]['Computer Science and Engineering Department'])+'.\n')
                except:self.txt_widget3.insert(END, '\tNumber of students from Computer Science and Engineering Department is 0.\n')
                try:self.txt_widget3.insert(END,'\tNumber of students from Electrical and Electronics Engineering Department is '+str(self.departments3[selected]['Electrical and Electronics Engineering Department'])+'.\n')
                except:self.txt_widget3.insert(END,'\tNumber of students from Electrical and Electronics Engineering Department is 0.\n')
                try:self.txt_widget3.insert(END,'\tNumber of students from Industrial Engineering Department is '+str(self.departments3[selected]['Industrial Engineering Department'])+'.\n')
                except:self.txt_widget3.insert(END,'\tNumber of students from Industrial Engineering Department is 0.\n')
                try:self.txt_widget3.insert(END,'\tNumber of students from Management is '+str(self.departments3[selected]['Management'])+'.\n')
                except:self.txt_widget3.insert(END,'\tNumber of students from Management is 0.\n')
                self.txt_widget3.insert(END, 'For this cluster, the majority is ' + str(self.lstbx_clusters3[selected][0]) + '.' + ' This cluster\n')
                self.txt_widget3.insert(END, '\tincludes ' + str(self.departments3[selected][self.lstbx_clusters3[selected][0]]) + ' students from ' + str(self.lstbx_clusters3[selected][0]) + ' out of ' + str(self.lstbx_clusters3[selected][1]) + '. Hence,\n')
                self.txt_widget3.insert(END, '\tthe accuracy is ' + self.lstbx_clusters3[selected][2] + '.\n---------------- \nStudents list:\n')
                for course in self.clusters_students3[selected]: # looping inside the list of course ids in this list
                    self.txt_widget3.insert(END,'\t'+course+'\n')
        except:pass





















































app = GUI()
root.mainloop()