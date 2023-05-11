
# imported modules
from Tkinter import *
import ttk
import tkFileDialog
import xlrd
import xlwt

root = Tk()
root.title('attendance tool')


class StudentsList(object):
    def __init__(self):
        self.section = {}  # a dictionary with the section as the key, and the list of STUDENTS IN THAT SECTION as the value

class Student(object): # class which identifies all the attributes of a student in the excel file
    def __init__(self, name, surname, ID, department, section):
        self.name = name
        self.surname = surname
        self.ID = ID
        self.department = department
        self.section = section


class GUI(object):
    def __init__(self):
        self.initGUI() # The interface design
        self.name_surname = {}  # dictionary of the FULL NAME as the key, and a list of [name,surname] as value
        self.students = {}  # dictionary where the SURNAME of the student is the key, and a Student class OBJECT is the value

    def initGUI(self):
        self.box_var = StringVar() # string variable for the combobox of the sections
        self.file_type_var = StringVar() # string variable for the combobox of the export file types
        combobox_vals = ['ENGR 102 07', 'ENGR 102 15', 'ENGR 102 18', 'ENGR 102 12', 'ENGR 102 08', 'ENGR 102 09',
                         'ENGR 102 19', 'ENGR 102 16', 'ENGR 102 04', 'ENGR 102 05', 'ENGR 102 06', 'ENGR 102 14',
                         'ENGR 102 13', 'ENGR 102 01', 'ENGR 102 02', 'ENGR 102 03'] # list of the values which will be shown in the sections combobox
        title_frame = Frame(root) # first frame which will engulf the TITLE AND THE IMPORT BUTTON
        frame2 = Frame(root) # another frame which will hold everything else
        title_frame.pack()
        frame2.pack(fill=BOTH, expand=True)

        self.title_label = Label(title_frame, text='AttendanceKeeper v1.0', font=('', '22', 'bold'), width=30)
        self.title_label.pack(fill=X)

        self.file_select_label = Label(title_frame, text='Select Student List Excel file:', font=('', '11', 'bold'))
        self.file_select_label.pack(side=LEFT)

        self.import_button = Button(title_frame, text='Import List', width=14, command=self.load_file) # the button which will return the file imported and do some stuff with it according to the method defined
        self.import_button.pack(side=LEFT)

        self.select_student_label = Label(frame2, text='Select A Student:', font=('', '11', 'bold'))
        self.select_student_label.grid(columnspan=2, sticky=W) # sticky = W is used to orient the label properly on the left side of the cell

        self.section_label = Label(frame2, text='Section:', font=('', '11', 'bold'))
        self.section_label.grid(row=0, column=2, columnspan=2, sticky=NSEW) # column and row spans are used to fill the other rows and columns of certain widgets so that they become aligned

        self.attended_students_label = Label(frame2, text='Attended Students:', font=('', '11', 'bold'))
        self.attended_students_label.grid(row=0, column=4, columnspan=2, sticky=W)

        self.selection_listbox_scrollbar = Scrollbar(frame2)
        self.selection_listbox_scrollbar.grid(row=1, column=2, rowspan=3, sticky=N + S + W)

        self.selection_listbox = Listbox(frame2, selectmode='multiple', height=3,
                                         yscrollcommand=self.selection_listbox_scrollbar.set) # selectmode is set to multiple so that the user can choose multiple seletions
        self.selection_listbox_scrollbar.configure(command=self.selection_listbox.yview) # attaching the scroll bar to the listbox in the vertical direction
        self.selection_listbox.grid(row=1, column=0, rowspan=3, columnspan=2, sticky=NSEW)

        self.section_combobox = ttk.Combobox(frame2, values=combobox_vals, textvariable=self.box_var, state='readonly') # readonly is used just to resitrict the user with the options iniside the combobox
        self.section_combobox.bind('<Return>',self.combocommand) # when the user presses enter in the combobox
        self.section_combobox.bind('<<ComboboxSelected>>', self.combocommand) # attaching a certain method defined below in case of the event of the user choosing one value of the combobox
        self.section_combobox.grid(row=1, column=3, sticky=NSEW)

        self.attended_students_listbox_scrollbar = Scrollbar(frame2)
        self.attended_students_listbox_scrollbar.grid(row=1, column=6, rowspan=3, sticky=NSEW)

        self.attended_students_listbox = Listbox(frame2, selectmode='multiple', height=3,
                                                 yscrollcommand=self.attended_students_listbox_scrollbar.set)
        self.attended_students_listbox_scrollbar.configure(command=self.attended_students_listbox.yview) # attaching a scrollbar to the other listbox as in the previous one
        self.attended_students_listbox.grid(row=1, column=4, rowspan=3, columnspan=2, sticky=NSEW)

        self.add_button = Button(frame2, text='Add =>', command=self.add_students) # the button responsible for adding the students into the other listbox
        self.add_button.grid(row=2, column=3, sticky=NSEW)

        self.remove_button = Button(frame2, text='<= Remove', command=self.remove_students) # the button responsible for removing the students from the attended students listbox
        self.remove_button.grid(row=3, column=3, sticky=NSEW)

        self.file_type_select_label = Label(frame2, text='Please select file type:', font=('', '10', 'bold'))
        self.file_type_select_label.grid(row=4, column=0, sticky=W)

        self.file_type_combobox = ttk.Combobox(frame2, width=4, values=('xls', 'txt', 'csv'), state='readonly',
                                               textvariable=self.file_type_var) # defining the combobox of the file type selection
        self.file_type_combobox.grid(row=4, column=1, sticky=E)

        self.entry_label = Label(frame2, text='Please Enter Week:', font=('', '10', 'bold'))
        self.entry_label.grid(row=4, column=3, sticky=E)

        self.week_entry = Entry(frame2)
        self.week_entry.grid(row=4, column=4, sticky=NSEW)

        self.export_button = Button(frame2, text='Export as file', command=self.file_export) # defining the export button responsible for creating or writing the new excel and text files
        self.export_button.grid(row=4, column=5, sticky=NSEW)

        for column in range(6): # this code is for making the widgets 'flexible' as the window enlarges
            Grid.columnconfigure(frame2, column, weight=1)
        for row in range(5):
            Grid.columnconfigure(frame2, row, weight=1)

    def load_file(self):
        self.filename = tkFileDialog.askopenfilename(initialdir="/", title="Select students list Excel file",
                                                     filetypes=(('Excel files', '*.xlsx;*.xls'), (
                                                     'all files', '*.*')))  # returns the path of the excel file chosen by the user from the Dialog
        book = xlrd.open_workbook(self.filename)  # opening the excel file (book)
        attendance_sheet = book.sheet_by_name('ENGR 102_studentList.Raw.3.3.20')  # opening the sheet we are willing to read in the file
        self.ENGR102 = StudentsList() # creating the StudentsList object
        for row in range(1, attendance_sheet.nrows): # loop for reading the sheet
            name = attendance_sheet.cell(row, 1).value # full name
            lst = name.split()
            surname = lst.pop() # surname
            firstname = ' '.join(lst) # first name
            section = attendance_sheet.cell(row, 3).value # acquiring the section of the student during the running loop
            self.name_surname[name] = [firstname, surname] # adding to the dictionary the name of the student as a key and a list of their first and last name as the value
            if section not in self.ENGR102.section:
                self.ENGR102.section[section] = [surname] # this adds to the StudentsList object dictionary (attr) the section of the student as the key, and his surname as a value
            else:
                self.ENGR102.section[section] += [surname] # this adds to the StudentsList object dictionary (attr) the section of the student as the key, and his surname as a value which is added to the list of students IN THE SAME SECTION
        for section in self.ENGR102.section: # run a loop inside the sections dictionary
            self.ENGR102.section[section].sort()  # for sorting the surnames in alphabetical order
        for row in range(1, attendance_sheet.nrows):
            name = attendance_sheet.cell(row, 1).value
            lst = name.split()
            surname = lst.pop()
            ID = str(int(attendance_sheet.cell(row, 0).value)) # getting the ID of the student from the file
            dept = attendance_sheet.cell(row, 2).value # getting the department of the student from the file
            section = attendance_sheet.cell(row, 3).value
            self.students[surname] = Student(self.name_surname[name][0], self.name_surname[name][1], ID, dept,
                                             section)  # initiating the student objects over here so that each student will have their own unique attrbs

        self.box_var.set('ENGR 102 01') # just to set the default value (name) of the combobox
        for student in self.ENGR102.section['ENGR 102 01']:  # student will be the SURNAME of the student
            self.selection_listbox.insert(END,
                                          self.students[student].surname + ',' + self.students[student].name + ',' +
                                          self.students[student].ID) # inserting the STUDENTS OF SECTION 01 to the students listbox (default section of combobox)

    def combocommand(self, event): # the event command used to bind the two events of the combobox
        try:
            self.selection_listbox.delete(0, END) # to clear the whole list
            self.attended_students_listbox.delete(0, END) # to clear the whole list
            current_section = self.section_combobox.get() # acquires the current selected section
            for student in self.ENGR102.section[current_section]: # for inserting all the students in the currently selected section
                self.selection_listbox.insert(END,
                                              self.students[student].surname + ',' + self.students[student].name + ',' +
                                              self.students[student].ID)
        except: # in case the user selected an option BEFORE importing the data file
            pass

    def add_students(self):
        selected = self.selection_listbox.curselection() # a tuple of indices of the selected students in the listbox
        for ix in selected:
            student = self.selection_listbox.get(ix) # to get the string (name,surname,ID)  of the current student in the loop
            self.attended_students_listbox.insert(END, student)
        for loop in range(len(selected)):  # for deletion
            updated_selection = self.selection_listbox.curselection()  # TO UPDATE THE 'SELECTED STUDENTS' TUPLE EACH TIME AFTER DELETING A STUDENT IN THE LISTBOX!!!
            if len(updated_selection) != 2:  # in case the tuple consisted of more than two items
                self.selection_listbox.delete(updated_selection[0])
            else:  # in case the 'selected' tuple consisted only of two items (LAST STAGE OF DELETION)
                self.selection_listbox.delete(updated_selection[1])
        self.file_type_var.set('txt')

    def remove_students(self): # removing students button (same as done above, but the opposite)
        selected = self.attended_students_listbox.curselection()
        for ix in selected:
            student = self.attended_students_listbox.get(ix)
            self.selection_listbox.insert(END, student)
        for loop in range(len(selected)):  # for deletion
            updated_selection = self.attended_students_listbox.curselection()  # TO UPDATE THE 'SELECTED' TUPLE EACH TIME AFTER DELETING A STUDENT IN THE LISTBOX!!!
            if len(updated_selection) != 2:  # in case the tuple consisted of more than two items
                self.attended_students_listbox.delete(updated_selection[0])
            else:  # in case the 'selected' tuple consisted only two items (LAST STAGE OF DELETION)
                self.attended_students_listbox.delete(updated_selection[1])

    def file_export(self):
        lst_of_students = []  # list where every ATTENDED student will be stored in
        tuple_of_students = self.attended_students_listbox.get(0, END)  # tuple including the text of the list box
        section = self.section_combobox.get()
        week = self.week_entry.get()
        for text in tuple_of_students:
            student = text.split(',')[0]  # gets the first item in the list which is the STUDENT'S SURNAME
            lst_of_students.append(student)
        lst_of_students.sort()
        if self.file_type_combobox.get() == 'txt':
            with open(section + ' ' + week + '.txt', 'a') as txtfile:
                txtfile.write('The format here comes as Student ID, Name, Depart. \n')
                for student in lst_of_students:  # ID, NAME, DEPT
                    txtfile.write(self.students[student].ID.encode('utf8') + '   ' + self.students[student].name.encode(
                        'utf8') + ' ' + self.students[student].surname.encode('utf8') + '  ' + self.students[
                                      student].department.encode('utf8') + '\n')
                    # the encoding took place just for dealing with the NON-ENGLISH characters in the code
        elif self.file_type_combobox.get() == 'xls': # come as row, column (ID, NAME, DEPT)
            Excel_file = xlwt.Workbook(encoding='utf8')
            sheet = Excel_file.add_sheet('attendance')
            sheet.write(0,0,'ID')
            sheet.write(0,1,'Name')
            sheet.write(0,2,'Dept.')
            row = 1  # initial row number
            for student in lst_of_students:
                sheet.write(row,0,self.students[student].ID.encode('utf8'))
                sheet.write(row,1,self.students[student].name.encode('utf8') + ' ' + self.students[student].surname.encode('utf8'))
                sheet.write(row,2,self.students[student].department.encode('utf8'))
                row += 1
            Excel_file.save(section + ' ' + week + '.xls') # saving the file

        elif self.file_type_combobox.get() == 'csv':
            raise BaseException('File type not supported!')



app = GUI()
root.mainloop()