import copy
import csv
import time
import urllib2
from Tkinter import *


# variables for storing data
root = Tk()
data_dict = {}
copy_dict = {}
last_updated = None
topFrame = middleFrame = bottomFrame = None
show1 = show2 = show3 = show4 = show5 = temp_show = None
temp_show = 1
occupy_percent1, occupy_percent2, occupy_percent3, occupy_percent4, occupy_percent5 = 0, 0, 0, 0, 0
change_percent1, change_percent2, change_percent3, change_percent4, change_percent5 = 0, 0, 0, 0, 0
occupy1, occupy2, occupy3, occupy4, occupy5 = 0, 0, 0, 0, 0
capacity1, capacity2, capacity3, capacity4, capacity5 = 0, 0, 0, 0, 0
last_update1, last_update2, last_update3, last_update4, last_update5 = 0, 0, 0, 0, 0
state1, state2, state3, state4, state5 = 0, 0, 0, 0, 0
color1, color2, color3, color4, color5 = 0, 0, 0, 0, 0
spaces_filled = spaces_total = spaces_available = percentage_filled = spaces = almost_full = full = faulty = i = 0


def updated_csv():
    """ function to download the latest csv file from the website http://data.nottinghamtravelwise.org.uk """

    global last_updated, temp_show, i, spaces_filled, spaces_total, spaces_available, percentage_filled, spaces, almost_full, full, faulty
    url = 'http://data.nottinghamtravelwise.org.uk/parking.csv?noLocation=true?'
    f = urllib2.urlopen(url)
    data = f.read()
    code = open("parking.csv",  "wb")
    code.write(data)
    code.close()
    # print'Latest CSV Loaded'

    # reinitialising the global variables
    spaces_filled = spaces_total = spaces_available = percentage_filled = spaces = almost_full = full = faulty = i = 0
    temp_show = 1

    # capturing last updated time
    last_updated = time.localtime(time.time())
    last_updated = time.strftime("%H:%M", last_updated)


def update_button_clicked():
    """ update button pressed handler """

    # print 'Update button pressed'
    # delete top frame
    topFrame.destroy()
    # delete middle and bottom frames
    delete_frames()
    main()
    # print 'Update button task over'


def left_arrow_button_clicked():
    """ < button pressed handler """

    global temp_show
    temp_show -= 5
    # print '< button pressed'#, temp_show

    if temp_show > 0:
        canvas_logic()
        delete_frames()
        display()
    else:
         temp_show = 1
         # print '< else executed',   temp_show
    # print '< button task over'


def right_arrow_button_clicked():
    """ > button pressed handler """

    global temp_show
    temp_show += 5
    # print '> button pressed'#, temp_show

    if temp_show < 26:
        canvas_logic()
        delete_frames()
        display()
    else:
         temp_show = 21
         # print '> else executed',   temp_show
    # print '> button task over'


def alpha_order_button_clicked():
    """ show alphabetical button pressed handler """

    global i, temp_show, data_dict
    alpha_list = []
    # print 'Show Alphabetical button pressed'

    # for loop for populating parking names in a temp list called alpha_list
    for j in range(1, i):
        alpha_list.append(data_dict[str(j)][3])
    # print 'Alphabet:',  alpha_list
    sorted_list = sorted(alpha_list, key=str.lower)      # alphabetically sorting the names
    # print 'Sorted Alpha:', sorted_list

    # initialise temp dictionary to hold alphabetically sorted data
    sorted_dict = {}
    # for loop to populate sorted_dict based on sorted_list
    for j in range(1, i):
        for k in range(1, i):
            if sorted_list[j-1] == data_dict[str(k)][3]:
                sorted_dict[str(j)] = data_dict[str(k)]

    # data_dict = sorted_dict.copy()
    data_dict = sorted_dict
    # print 'Sorted Dictionary:',  data_dict

    temp_show = 1  # reinitialising variable
    # print 'Show Alphabetical Button Pushed', temp_show
    canvas_logic()
    delete_frames()
    display()
    # print 'Show Alphabetical button task over'


def emptiest_button_clicked():
    """ show emptiest button pressed handler """

    global i, temp_show, data_dict
    empty_list = []
    # print 'Show Empiest button pressed'

    # for loop for populating occupancy percentage in a temp list called empty_list
    for j in xrange(1, i):
        empty_list.append(int(data_dict[str(j)][9]))
    # print 'Empty:',  empty_list
    sorted_empty = sorted(empty_list)
    # print 'Sorted Empty:', sorted_empty

    # initialise temp dictionary to hold sorted data
    sorted_dict = {}
    # temp list named extractor to keep track if a key value pair already exist in sorted_dict
    extracter = []

    # for loop to populate sorted_dict based on sorted_empty
    for j in xrange(1, i):
        for k in xrange(1, i):
            if sorted_empty[j-1] == int(data_dict[str(k)][9]):
                if k in extracter:
                    continue
                else:
                    sorted_dict[str(j)] = data_dict[str(k)]
                    # from temp list named extractor exclude a key value pair that is already present in sorted_dict
                    extracter.append(k)
                    # print 'Loop', j, extracter
                    break
    # print 'extracter:', extracter

    data_dict = sorted_dict
    # print 'Sorted Empty Dictionary:',  data_dict

    temp_show = 1   # reinitialising variable
    # print 'Show Emptiest Button Pushed', temp_show
    canvas_logic()
    delete_frames()
    display()
    # print 'Show Empiest button task over'


def fullest_button_clicked():
    """ show fullest button pressed handler """

    global i, temp_show, data_dict
    full_list = []
    # print 'Show Fullest button pressed'

    # for loop for populating occupancy percentage in a temp list called full_list
    for j in xrange(1, i):
        full_list.append(int(data_dict[str(j)][9]))
    # print 'Full:',  full_list
    sorted_full = sorted(full_list, reverse = True)  # sorting the list in reverse order i.e in descending order
    # print 'Sorted Empty to Full:', sorted_full

    # initialise temp dictionary to hold reverse sorted data
    sorted_dict = {}
    # temp list named extractor to keep track if a key value pair already exist in sorted_dict
    extracter = []
    # sorted_dict = data_dict.copy()
    # print sorted_dict
    # for loop to populate sorted_dict based on sorted_full
    for j in xrange(1, i):
        for k in xrange(1, i):
            if sorted_full[j-1] == int(data_dict[str(k)][9]):
                if k in extracter:
                    continue
                else:
                    sorted_dict[str(j)] = data_dict[str(k)]
                    # from temp list named extractor exclude a key value pair that is already present in sorted_dict
                    extracter.append(k)
                    # print 'Loop', j, extracter
                    break
    # print 'extracter:', extracter
    # data_dict = sorted_dict.copy()
    data_dict = sorted_dict
    # print 'Sorted Full Dictionary:',  data_dict

    temp_show = 1   #reinitialising variable
    # print 'Show Full Button Pushed', temp_show
    canvas_logic()
    delete_frames()
    display()
    # print 'Show Fullest button task over'


def csv_reader():
    """ function for reading CSV file in a dictionary and preparing data for topFrame """

    global data_dict, copy_dict
    global spaces_filled, spaces_total, spaces_available, percentage_filled, spaces, almost_full, full, faulty, i

    # print 'Reading parking.csv ....'
    file = open('parking.csv')
    read_object = csv.reader(file)
    # print 'Reading parking.csv over'
    # copy each row from CSV file into dict
    for row in read_object:
        data_dict[str(i)] = row
        i += 1  # global variable i is used for generating key for dict
    # print i   # printing row count in csv
    # print data_dict

    # modify the dict to include change% in it
    for j in range(1, i):
        # print data_dict[str(j)][8]
        # if-else is used to take care of change% for 1st run of program
        if not bool(copy_dict):
            # print 'copy_dict is empty'
            # append list present in dict to include change% in it for 1st run of program
            data_dict[str(j)].append(0)
        else:
            # print 'copy_dict is not empty'
            # append list present in dict to include change% in it
            data_dict[str(j)].append(int(data_dict[str(j)][9]) - int(copy_dict[str(j)][9]))

        # populate variables to be displayed in topFrame
        spaces_filled += int(data_dict[str(j)][8])
        spaces_total += int(data_dict[str(j)][1])
        if data_dict[str(j)][6] == ' Spaces':
            spaces += 1
        elif data_dict[str(j)][6] == ' Almost Full':
            almost_full += 1
        elif data_dict[str(j)][6] == ' Full':
            full += 1
        elif data_dict[str(j)][6] == ' Faulty':
            faulty += 1

    # copy the data from dict to copy_dict to display change%
    copy_dict = copy.deepcopy(data_dict)
    # copy_dict = data_dict
    # print 'copy_dict:', copy_dict

    # print 'printing dictionary again:', data_dict
    # print 'Spaces Filled: ', spaces_filled
    # print 'Spaces Total: ', spaces_total
    spaces_available = spaces_total-spaces_filled
    # print 'Spaces available: ', spaces_available
    percentage_filled = (spaces_filled*100)/spaces_total
    percentage_filled = str(percentage_filled) + "%"
    # print 'Percent Filled: ', percentage_filled
    # print 'Statuses: Spaces:', spaces, 'Almost Full:', almost_full, 'Full:', full, 'Faulty:', faulty

    file.close()


def canvas_logic():
    """ function for preparing data for middleFrame """

    global data_dict
    global show1, show2, show3, show4, show5, temp_show
    global occupy_percent1, occupy_percent2, occupy_percent3, occupy_percent4, occupy_percent5
    global change_percent1, change_percent2, change_percent3, change_percent4, change_percent5
    global occupy1, occupy2, occupy3, occupy4, occupy5
    global capacity1, capacity2, capacity3, capacity4, capacity5
    global last_update1, last_update2, last_update3, last_update4, last_update5
    global state1, state2, state3, state4, state5
    global color1, color2, color3, color4, color5

    # populating variables to be displayed in middleFrame
    # temp_show = 1
    # print 'temp_show', temp_show
    show1 = data_dict[str(temp_show)][3]
    occupy_percent1 = data_dict[str(temp_show)][9]
    occupy1 = data_dict[str(temp_show)][8]
    capacity1 = data_dict[str(temp_show)][1]
    last_update1 = data_dict[str(temp_show)][13]
    change_percent1 = data_dict[str(temp_show)][14]
    state1 = data_dict[str(temp_show)][6]
    if state1 == ' Spaces':
        color1 = 'Green'
    elif state1 == ' Almost Full':
        color1 = 'Orange'
    elif state1 == ' Full':
        color1 = 'Red'
    elif state1 == ' Faulty':
        color1 = 'White'
    else:
        color1 = 'Yellow'

    show2 = data_dict[str(temp_show + 1)][3]
    occupy_percent2 = data_dict[str(temp_show + 1)][9]
    occupy2 = data_dict[str(temp_show + 1)][8]
    capacity2 = data_dict[str(temp_show + 1)][1]
    last_update2 = data_dict[str(temp_show + 1)][13]
    change_percent2 = data_dict[str(temp_show + 1)][14]
    state2 = data_dict[str(temp_show + 1)][6]
    if state2 == ' Spaces':
        color2 = 'Green'
    elif state2 == ' Almost Full':
        color2 = 'Orange'
    elif state2 == ' Full':
        color2 = 'Red'
    elif state2 == ' Faulty':
        color2 = 'White'
    else:
        color2 = 'Yellow'

    show3 = data_dict[str(temp_show + 2)][3]
    occupy_percent3 = data_dict[str(temp_show + 2)][9]
    occupy3 = data_dict[str(temp_show + 2)][8]
    capacity3 = data_dict[str(temp_show + 2)][1]
    last_update3 = data_dict[str(temp_show + 2)][13]
    change_percent3 = data_dict[str(temp_show + 2)][14]
    state3 = data_dict[str(temp_show + 2)][6]
    if state3 == ' Spaces':
        color3 = 'Green'
    elif state3 == ' Almost Full':
        color3 = 'Orange'
    elif state3 == ' Full':
        color3 = 'Red'
    elif state3 == ' Faulty':
        color3 = 'White'
    else:
        color3 = 'Yellow'

    show4 = data_dict[str(temp_show + 3)][3]
    occupy_percent4 = data_dict[str(temp_show + 3)][9]
    occupy4 = data_dict[str(temp_show + 3)][8]
    capacity4 = data_dict[str(temp_show + 3)][1]
    last_update4 = data_dict[str(temp_show + 3)][13]
    change_percent4 = data_dict[str(temp_show + 3)][14]
    state4 = data_dict[str(temp_show + 3)][6]
    if state4 == ' Spaces':
        color4 = 'Green'
    elif state4 == ' Almost Full':
        color4 = 'Orange'
    elif state4 == ' Full':
        color4 = 'Red'
    elif state4 == ' Faulty':
        color4 = 'White'
    else:
        color4 = 'Yellow'

    show5 = data_dict[str(temp_show + 4)][3]
    occupy_percent5 = data_dict[str(temp_show + 4)][9]
    occupy5 = data_dict[str(temp_show + 4)][8]
    capacity5 = data_dict[str(temp_show + 4)][1]
    last_update5 = data_dict[str(temp_show + 4)][13]
    change_percent5 = data_dict[str(temp_show + 4)][14]
    state5 = data_dict[str(temp_show + 4)][6]
    if state5 == ' Spaces':
        color5 = 'Green'
    elif state5 == ' Almost Full':
        color5 = 'Orange'
    elif state5 == ' Full':
        color5 = 'Red'
    elif state5 == ' Faulty':
        color5 = 'White'
    else:
        color5 = 'Yellow'


def delete_frames():
    """ function to delete frames when a button is clicked """
    # topFrame.destroy()
    middleFrame.destroy()
    bottomFrame.destroy()


def display():
    """ function for displaying widgets for middleFrame and bottomFrame """

    global middleFrame, bottomFrame, last_updated

    middleFrame = Frame(root, bg='White')
    bottomFrame = Frame(root, relief=RAISED, bg='White')
    middleFrame.pack(fill=BOTH)
    bottomFrame.pack(fill=X)

    # Grid layout for bottomFrame
    button2_1 = Button(bottomFrame, text="<", bg='White', anchor=E, command=left_arrow_button_clicked).grid(row=0, column=0, sticky=E, pady=2)
    label2_1 = Label(bottomFrame, text="%d-%d/25"%(temp_show, temp_show+4), bg='White').grid(row=0, column=1, pady=2)
    button2_2 = Button(bottomFrame, text=">", bg='White', anchor=W, command=right_arrow_button_clicked).grid(row=0, column=2, sticky=W, pady=2)

    button3_1 = Button(bottomFrame, text="Show Alphabetical", bg='White', anchor=E, command=alpha_order_button_clicked).grid(row=1, column=0, sticky=E, pady=2)
    button3_2 = Button(bottomFrame, text="Show Emptiest", bg='White', command=emptiest_button_clicked).grid(row=1, column=1, pady=2)
    button3_3 = Button(bottomFrame, text="Show Fullest", bg='White', anchor=W, command=fullest_button_clicked).grid(row=1, column=2, sticky=W, pady=2)

    button4_1 = Button(bottomFrame, text="Update", bg='White', anchor=E, command=update_button_clicked).grid(row=2, column=0, sticky=E, pady=2)
    label4_1 = Label(bottomFrame, text="Last update: %s"%last_updated, bg='White').grid(row=2, column=1, pady=2)

    label2_2 = Label(bottomFrame, text="        Contains public sector information licensed under the Open Government Licence v1.0.", bg='White').grid(row=3, columnspan=3)

    # Grid layout & Canvas for middleFrame
    label1_mid = Label(middleFrame, text="Car Parks", font='bold 10', bg='White').grid(row=0, column=1, padx=3, pady=3)

    w1 = Canvas(middleFrame, width=500, height=40, relief=GROOVE, bg='White')
    w1.grid(row=1, columnspan=3, padx=3, pady=3)
    w1.create_rectangle(0,  20,  1.50*float(occupy_percent1),  37,  width=1,  fill=color1)
    w1.create_text(0, 10, text=show1, anchor=W)
    w1.create_text(0, 30, text=occupy_percent1+'%', anchor=W)
    w1.create_text(185, 10, text=occupy1+'  of '+capacity1+' places filled', anchor=W)
    w1.create_text(185, 30, text='Last updated at:'+last_update1[:17], anchor=W)
    w1.create_text(430, 30, text='Change: '+str(change_percent1)+'%', anchor=W)

    w2 = Canvas(middleFrame, width=500, height=40, relief=GROOVE, bg='White')
    w2.grid(row=2, columnspan=3, padx=3, pady=3)
    w2.create_rectangle(0,  20,  1.50*float(occupy_percent2),  37,  width=1,  fill=color2)
    w2.create_text(0, 10, text=show2, anchor=W)
    w2.create_text(0, 30, text=occupy_percent2+'%', anchor=W)
    w2.create_text(185, 10, text=occupy2+'  of '+capacity2+' places filled', anchor=W)
    w2.create_text(185, 30, text='Last updated at:'+last_update2[:17], anchor=W)
    w2.create_text(430, 30, text='Change: '+str(change_percent2)+'%', anchor=W)

    w3 = Canvas(middleFrame, width=500, height=40, relief=GROOVE, bg='White')
    w3.grid(row=3, columnspan=3, padx=3, pady=3)
    w3.create_rectangle(0,  20,  1.50*float(occupy_percent3),  37,  width=1,  fill=color3)
    w3.create_text(0, 10, text=show3, anchor=W)
    w3.create_text(0, 30, text=occupy_percent3+'%', anchor=W)
    w3.create_text(185, 10, text=occupy3+'  of '+capacity3+' places filled', anchor=W)
    w3.create_text(185, 30, text='Last updated at:'+last_update3[:17], anchor=W)
    w3.create_text(430, 30, text='Change: '+str(change_percent3)+'%', anchor=W)

    w4 = Canvas(middleFrame, width=500, height=40, relief=GROOVE, bg='White')
    w4.grid(row=4, columnspan=3, padx=3, pady=3)
    w4.create_rectangle(0,  20,  1.50*float(occupy_percent4),  37,  width=1,  fill=color4)
    w4.create_text(0, 10, text=show4, anchor=W)
    w4.create_text(0, 30, text=occupy_percent4+'%', anchor=W)
    w4.create_text(185, 10, text=occupy4+'  of '+capacity4+' places filled', anchor=W)
    w4.create_text(185, 30, text='Last updated at:'+last_update4[:17], anchor=W)
    w4.create_text(430, 30, text='Change: '+str(change_percent4)+'%', anchor=W)

    w5 = Canvas(middleFrame, width=500, height=40, relief=GROOVE, bg='White')
    w5.grid(row=5, columnspan=3, padx=3, pady=3)
    w5.create_rectangle(0,  20,  1.50*float(occupy_percent5),  37,  width=1,  fill=color5)
    w5.create_text(0, 10, text=show5, anchor=W)
    w5.create_text(0, 30, text=occupy_percent5+'%', anchor=W)
    w5.create_text(185, 10, text=occupy5+'  of '+capacity5+' places filled', anchor=W)
    w5.create_text(185, 30, text='Last updated at:'+last_update5[:17], anchor=W)
    w5.create_text(430, 30, text='Change: '+str(change_percent5)+'%', anchor=W)


def main():
    """ main function for starting the program execution """

    # whole window is divided into 3 frames
    global topFrame, middleFrame, bottomFrame
    print 'Main program started'
    updated_csv()
    csv_reader()
    canvas_logic()

    # Grid layout for topFrame
    topFrame = Frame(root, relief=RAISED)
    topFrame.pack(fill=BOTH)

    label1 = Label(topFrame, text="Overview", font='bold 11').grid(row=0, sticky=W)
    label2 = Label(topFrame, text="Spaces Filled: %d" % spaces_filled).grid(row=1, column=0, sticky=W)
    label3 = Label(topFrame, text="Spaces Available: %d" % spaces_available).grid(row=1, column=1)
    label4 = Label(topFrame, text="Percentage Filled: %s" % percentage_filled).grid(row=1, column=2, sticky=E)
    label5 = Label(topFrame, text="Statuses: Spaces: %d,  Almost Full: %d,  Full: %d,  Faulty: %d" % (spaces, almost_full, full, faulty)).grid(row=2, column=1)

    display()


main()
root.title('Nottingham Car Parks Monitor')
root.resizable(0, 0)    # preventing window to maximize
root.mainloop() # main event loop
