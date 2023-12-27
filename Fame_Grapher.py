#!/usr/bin/env python
# coding: utf-8

# In[3]:


#!/usr/bin/env python
# coding: utf-8

# <h1> Making the GUI 

# In[1]:

def SampleTypeKey(sortedexcel):
    """Classifies as Whole Broth or Washed Broth"""
    key = []
    for x in sortedexcel.index:
        if "WB" in x:
            key.append("Whole Broth")
        else:
            key.append("Washed Broth")
    return key

def SampleNumKey(sortedexcel):
    """Counts the number of letters in the sample name"""
    num = []
    for x in sortedexcel.index:
        num.append(len(x))
    return num

def LogHour(sortedexcel):
    """Grabs the log hour from the sample name given"""
    Log = []
    for x in range(0, len(sortedexcel.index)):
        try:
            t = sortedexcel.index[x].strip().replace(","," ").split(" ")[2]
            Time = float(t)
            Log.append(Time)
        except IndexError:
            t = 0
            Time = float(t)
            Log.append(Time)
        except ValueError:
            t = sortedexcel.index[x].strip().replace(","," ").split(" ")[1]
            Time = float(t)
            Log.append(Time)
            
    return Log

def Name(sortedexcel):
    """Grabs the name only from the string"""
    name = []
    for x in range(0, len(sortedexcel.index)):
        na = sortedexcel.index[x].strip().replace(","," ").split(" ")[0]
        name.append(na)
    return name

def Time(sortedexcel):
    """Grabs the timestamp"""
    time = []
    for x in range(0, len(sortedexcel.index)):
        try:
            f = sortedexcel.index[x].strip().replace(","," ").split(" ")[1].replace(".","/")
            timestamp = pd.to_datetime(f)
            time.append(timestamp)
        except TypeError:
            timestamp = pd.to_datetime("00.00.00")
            time.append(timestamp)
    return time

def Color(sortedexcel):
    """ Inserts a randomized color for each unique name"""
    import matplotlib
    import numpy as np
    colors = dict(matplotlib.colors.cnames.items())
    hex_colors = tuple(colors.values())
    color = []
    color_d = {}
    #setting the key for each with a value that is a random color generated
    for x in sortedexcel["Name"].unique():
        color_d[x] = np.random.choice(hex_colors, replace = False)
    #Next to iterate 
    for x in sortedexcel["Name"].values:
        if x in color_d:
            color.append(color_d[x])
    return color

def NaNinsert_Washed(df: list, sortedexcel: list):
    """Goal is to insert NaN values where the Name dosen't match
    df: Dataframe"""
    import numpy as np
    import pandas as pd
    #Getting the unique names and the total number of uniquw names to iterate
    unique = sortedexcel["Name"].unique()
    uni_num = len(unique)
    #the iterators
    c = 0
    #Preparing the masks
    mask = sortedexcel["Type"] == "Washed Broth" 
    mask2 = sortedexcel["Name"] == unique[0]
    #Getting the NaN values to insert
    NaN = pd.Series(np.NaN)
    newlist = pd.concat((df[mask & mask2],NaN))
    while c < uni_num - 1:
        mask3 = sortedexcel["Name"] == unique[c + 1]
        newlist = pd.concat((newlist,df[mask & mask3]))
        newlist = pd.concat((newlist,NaN))
        c += 1
    newlist.set_index(["Samples"], inplace = True)
    newlist.drop(0, axis = 1, inplace = True)    
    return newlist

def NaNinsert_Whole(df: list, sortedexcel: list):
    """Goal is to insert NaN values where the Name dosen't match
    df: Dataframe"""
    import numpy as np
    import pandas as pd
    #Getting the unique names and the total number of uniquw names to iterate
    unique = sortedexcel["Name"].unique()
    uni_num = len(unique)
    #the iterators
    c = 0
    #Preparing the masks
    mask = sortedexcel["Type"] == "Whole Broth" 
    mask2 = sortedexcel["Name"] == unique[0]
    #Getting the NaN values to insert
    NaN = pd.Series(np.NaN)
    newlist = pd.concat((df[mask & mask2],NaN))
    while c < uni_num - 1:
        mask3 = sortedexcel["Name"] == unique[c + 1]
        newlist = pd.concat((newlist,df[mask & mask3]))
        newlist = pd.concat((newlist,NaN))
        c += 1
    newlist.set_index(["Samples"], inplace = True)
    newlist.drop(0, axis = 1, inplace = True)    
    return newlist

def figures_to_html(figs, filename):
    '''Saves a list of plotly figures in an html file.

    Parameters
    ----------
    figs : list[plotly.graph_objects.Figure]
        List of plotly figures to be saved.

    filename : str
        File name to save in.

    #https://stackoverflow.com/questions/46821554/multiple-plotly-plots-on-1-page-without-subplot
    '''
    import plotly.offline as pyo
    import io
    dashboard = io.open(filename, 'w', encoding="utf-8")
    dashboard.write("<html><head></head><body>" + "\n")

    add_js = True
    for fig in figs:
        #Here I can add a counter to add a header elementfor Washed / Whole 
        inner_html = pyo.plot(
            fig, include_plotlyjs=add_js, output_type='div'
        )

        dashboard.write(inner_html)
        add_js = False #Saves the file from becoming bloated with javascript

    dashboard.write("</body></html>" + "\n")
    
def show_in_window(values):
    """Will be used to display the html page in its own pop up and not in browser!"""
    import sys, os
    import plotly.offline
    from PyQt6.QtCore import QUrl
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    web = QWebEngineView()
    file_path = os.path.abspath(os.path.join(os.path.dirname(values["-FILE-"]), values[0] + ".html"))
    web.load(QUrl.fromLocalFile(file_path))
    web.show()
    sys.exit(app.exec())

#python -m pip install pysimplegui used Anaconda prompt
########################################################
import sys
import PySimpleGUI as sg
sg.theme("DarkTeal12")
layout = [[   sg.Text("FAME Graph File Location:",font=('Times New Roman',16)),
        sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
        sg.FileBrowse()], [sg.Text("What type of FAME data is this?", font=('Times New Roman',16))], [sg.Radio("Fermentation","type",key = "Fermentation"), sg.Radio("Non-Fermentation","type" ,key = "Non-Fermentation")],
      [sg.Text('Enter Name of Output HTML:', font=('Times New Roman',16))], [sg.Input(do_not_clear=False)],
    
          [sg.Button("Execute")]]

window = sg.Window("FAME Grapher", layout,margins=(100, 100),element_justification='c')


while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Execute" or event == sg.WIN_CLOSED:
        break

window.close()
############################################

# In[8]:



# <h2>Grapher code

# In[3]:



#####Import Block#############
import pandas as pd
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"
#"conda install -c plotly plotly=5.16.1" "for anaconda prompt"

#####################################################
#filepath = input("Path to the FAME sheet: ")
filepath = values["-FILE-"]

#####################################################
if values["Fermentation"] == False and values["Non-Fermentation"] == True:
    
    excel = pd.read_excel(io = filepath ,sheet_name = 0)
    maxcol = len(excel.columns) #Grabbing the max column
    colnumber = range(0,maxcol,1) #Grabbing the list of columns numbers 
    #Re-assigning the new columns
    excel = pd.read_excel(io = filepath ,sheet_name = 0, usecols = colnumber)
    #Renames the Sample Column, sets it as the index and sorts the columns
    excel.rename(columns = {"Sample" : "Components"}, inplace = True)
    sortedexcel = excel.pivot_table(columns = "Components")
    sortedexcel.reset_index(inplace = True)
    sortedexcel.rename(columns = {"index" : "Samples"}, inplace = True)
    sortedexcel.sort_values(by = ["Samples"],inplace = True, kind = "mergesort")
    #Added below for non-named numeric samples
    sortedexcel.set_index(["Samples"], inplace = True)
    ##########################################################
    #Assigning to seperate variables for graphing

        #Percentage
    eight_eleven = sortedexcel.loc[:,["%  08:0","%  09:0", "%  10:0","%  11:0", "%  11:1"]]
    twelve_fourteen = sortedexcel.loc[:,["%  12:0", "%  12:1", "%  13:0", "%  13:1", "%  14:0", "%  14:1"]]
    fifteen_sixteen = sortedexcel.loc[:,["%  15:1","%  16:0","%  16:1","%  16:2", "%  16:3"]]
    seventeen_eighteen = sortedexcel.loc[:,["%  17:0", "%  18:0", "%  18:1 n-7", "%  18:1 n-9", "%  18:2"]]
    eighteen_twenty = sortedexcel.loc[:,["%  18:3 n-3","%  18:3 n-6","%  18:4 n-3","%  20:0","%  20:1 n-9"]]
    twenty_ARA = sortedexcel.loc[:,["%  20:2", "%  20:3 n-3", "%  20:3 n-6","%  20:3 n-9", "%  20:4 ARA"]]
    EPA_twentytwo = sortedexcel.loc[:,["%  20:5 n-3 EPA","%  22:0","%  22:1", "%  22:4 n-6", "%  22:5 n-3"]]
    DHA_twentytwo = sortedexcel.loc[:,["%  22:5 n-6", "%  22:6 n-3 DHA", "% 22:2", "% 22:3"]]
    twentyfour = sortedexcel.loc[:,["%  24:0", "%  24:1"]]
    unknown = sortedexcel.loc[:,["% unknown"]]
    percent_fat = sortedexcel.loc[:,[" %Fat (as FAME) using RRFs"]]
    #concentration
    tsmg = sortedexcel.loc[:,["12:0","14:0","16:0","16:1"]]
    emg = sortedexcel.loc[:,[ "18:0", "18:1 n-9", "18:1 n-7","18:2", "18:3 n-6", "18:3 n-3"]]
    immg = sortedexcel.loc[:,[ "ARA", "DHA", "DPA n-3", "DPA n-6", "EPA", "20:3 n-6 mg/g"]]
    dcw = sortedexcel.loc[:,["DCW"]]
    ############################################################

    ###########################################################
    #Making the Graphs
    #GRAPHS (Percentage)

    fig1 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.9, 0.9],                         subplot_titles=("% 08:0", "% 09:0", "% 10:0", "% 11:0","% 11:1"),                         vertical_spacing = 0.06,                         specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig1.add_trace((go.Scatter( x = eight_eleven["%  08:0"].index, y = eight_eleven["%  08:0"].values, name = " %08:0", mode='lines+markers')), row=1, col=1)

    fig1.add_trace((go.Scatter( x = eight_eleven["%  09:0"].index, y = eight_eleven["%  09:0"].values, name = " %09:0", mode='lines+markers')), row=1, col=2)

    fig1.add_trace((go.Scatter( x = eight_eleven["%  10:0"].index, y = eight_eleven["%  10:0"].values, name = "%10:0", mode='lines+markers' )), row=2, col=1)

    fig1.add_trace((go.Scatter( x = eight_eleven["%  11:0"].index, y = eight_eleven["%  11:0"].values, name = "%11:0", mode='lines+markers')), row=2, col=2)

    fig1.add_trace((go.Scatter( x = eight_eleven["%  11:1"].index, y = eight_eleven["%  11:1"].values, name = "%11:1", mode='lines+markers')), row=3, col=2)    

    fig1.update_layout(height=600, width=1000,
                      title_text="Percent of 8:0, 9:0, 10:0, 11:0 and 11:1 Compounds")
    #####################

    fig2 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, vertical_spacing = 0.06,                        subplot_titles=("% 12:0", "% 12:1", "% 13:0", "% 13:1","% 14:0","% 14:1"))

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  12:0"].index, y = twelve_fourteen["%  12:0"].values, name = " %12:0", mode='lines+markers')), row=1, col=1, )

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  12:1"].index, y = twelve_fourteen["%  12:1"].values, name = " %12:1", mode='lines+markers')), row=1, col=2)

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  13:0"].index, y = twelve_fourteen["%  13:0"].values, name = "%13:0", mode='lines+markers')), row=2, col=1)

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  13:1"].index, y = twelve_fourteen["%  13:1"].values, name = "%13:1", mode='lines+markers')), row=2, col=2)

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  14:0"].index, y = twelve_fourteen["%  14:0"].values, name = "%14:0", mode='lines+markers')), row=3, col=1)    

    fig2.add_trace((go.Scatter( x = twelve_fourteen["%  14:1"].index, y = twelve_fourteen["%  14:1"].values, name = "%14:1", mode='lines+markers')), row=3, col=2)

    fig2.update_layout(height=600, width=1000,
                      title_text="Percent of 12:0, 12:1, 13:0, 13:1, 14:0 and 14:1 Compounds")

    fig1.update_xaxes(tickangle=60)
    fig2.update_xaxes(tickangle=60)
    ##################
    fig3 = make_subplots(rows=3, cols=2, shared_yaxes= False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.06,                        subplot_titles=("% 15:1", "% 16:0", "% 16:1", "% 16:2","% 16:3"),                        specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig3.add_trace((go.Scatter( x = fifteen_sixteen["%  15:1"].index, y = fifteen_sixteen["%  15:1"].values, name = " %15:1", mode='lines+markers')), row=1, col=1)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen["%  16:0"].index, y = fifteen_sixteen["%  16:0"].values, name = " %16:0", mode='lines+markers')), row=1, col=2)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen["%  16:1"].index, y = fifteen_sixteen["%  16:1"].values, name = " %16:1", mode='lines+markers')), row=2, col=1)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen["%  16:2"].index, y = fifteen_sixteen["%  16:2"].values, name = "%16:2", mode='lines+markers')), row=2, col=2)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen["%  16:3"].index, y = fifteen_sixteen["%  16:3"].values, name = "%16:3", mode='lines+markers')), row=3, col=2)    

    fig3.update_layout(height=500, width=1000,
                      title_text="Percent of 15:1, 16:0, 16:1, 16:2 and 16:3 Compounds")

    ########

    fig4 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.05,                        subplot_titles=("%  17:0", "%  18:0", "%  18:1 n-7", "%  18:1 n-9","%  18:2"),                        specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig4.add_trace((go.Scatter( x = seventeen_eighteen["%  17:0"].index,                               y = seventeen_eighteen["%  17:0"].values, name = "%17:0", mode='lines+markers')), row=1, col=1)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen["%  18:0"].index,                               y = seventeen_eighteen["%  18:0"].values, name = "%18:0", mode='lines+markers')), row=1, col=2)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen["%  18:1 n-7"].index,                               y = seventeen_eighteen["%  18:1 n-7"].values, name = "%18:1 n-7", mode='lines+markers')), row=2, col=1)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen["%  18:1 n-9"].index,                               y = seventeen_eighteen["%  18:1 n-9"].values, name = "%18:1 n-9", mode='lines+markers')), row=2, col=2)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen["%  18:2"].index,                               y = seventeen_eighteen["%  18:2"].values, name = "%18:2", mode='lines+markers')), row=3, col=2)    

    fig4.update_layout(height=600, width=1000,
                      title_text="Percent of 17:0, 18:0, 18:1 n-7, 18:1 n-9 and 18:2 Compounds")

    fig3.update_xaxes(tickangle=60)
    fig4.update_xaxes(tickangle=60)
    #####
    fig5 = make_subplots(rows=1, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.02,                        subplot_titles=("% 18:3 n-3, % 18:3 n-6 and % 18:4 n-3", "%  20:0 and % 20:1 n-9"))

    fig5.add_trace((go.Scatter( x = eighteen_twenty["%  18:3 n-3"].index, y = eighteen_twenty["%  18:3 n-3"].values, name = "%18:3 n-3", mode='lines+markers'                               )), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty["%  18:3 n-6"].index, y = eighteen_twenty["%  18:3 n-6"].values, name = "%18:3 n-6", mode='lines+markers')), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty["%  18:4 n-3"].index, y = eighteen_twenty["%  18:4 n-3"].values, name = "%18:4 n-3", mode='lines+markers')), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty["%  20:0"].index, y = eighteen_twenty["%  20:0"].values, name = "%20:0", mode='lines+markers')), row=1, col=2)

    fig5.add_trace((go.Scatter( x = eighteen_twenty["%  20:1 n-9"].index, y = eighteen_twenty["%  20:1 n-9"].values, name = "%20:1 n-9", mode='lines+markers')), row=1, col=2)    

    fig5.update_layout(height=500, width=1000,
                      title_text="Percent of 18:3, 18:4, 20:0 and 20:1 Compounds")

    ######

    fig6 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.6, 0.6], vertical_spacing = 0.2,                        subplot_titles=("% 20:2 and % 20:3 n-3", "% ARA", "% 20:3 n-9 and % 20:3 n-6","% EPA"))

    fig6.add_trace((go.Scatter( x = twenty_ARA["%  20:2"].index, y = twenty_ARA["%  20:2"].values, name = "%20:2",mode='lines+markers'                              )), row=1, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA["%  20:3 n-3"].index, y = twenty_ARA["%  20:3 n-3"].values, name = "%20:3 n-3", mode='lines+markers')), row=1, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA["%  20:3 n-6"].index, y = twenty_ARA["%  20:3 n-6"].values, name = "%20:3 n-6", mode='lines+markers')), row=2, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA["%  20:3 n-9"].index, y = twenty_ARA["%  20:3 n-9"].values, name = "%20:3 n-9", mode='lines+markers')), row=2, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA["%  20:4 ARA"].index, y = twenty_ARA["%  20:4 ARA"].values, name = "%20:4 ARA", mode='lines+markers')), row=1, col=2)    

    fig6.add_trace((go.Scatter( x = EPA_twentytwo["%  20:5 n-3 EPA"].index, y = EPA_twentytwo["%  20:5 n-3 EPA"].values, name = "%20:5 n-3 EPA", mode='lines+markers')), row=2, col=2)

    fig6.update_layout(height=500, width=1000,
                      title_text="Percent of 20:2, 20:3, ARA and EPA Compounds")
    ###
    fig5.update_xaxes(tickangle=60)
    fig6.update_xaxes(tickangle=60)
    ###
    fig7 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7],                         vertical_spacing = 0.2, subplot_titles=("% 22:0 and % 22:1", "% 22:2, % 22:3 and % 22:4 n-6", "% 22:5 n-3 and % 22:5 n-6", "% DHA"))

    fig7.add_trace((go.Scatter( x = EPA_twentytwo["%  22:0"].index, y = EPA_twentytwo["%  22:0"].values,name = "%22:0", mode='lines+markers')), row=1, col=1)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo["%  22:1"].index, y = EPA_twentytwo["%  22:1"].values,name = "%22:1", mode='lines+markers')), row=1, col=1)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo["% 22:2"].index, y = DHA_twentytwo["% 22:2"].values,name = "% 22:2", mode='lines+markers')), row=1, col=2)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo["% 22:3"].index, y = DHA_twentytwo["% 22:3"].values,name = "% 22:3", mode='lines+markers')), row=1, col=2)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo["%  22:4 n-6"].index, y = EPA_twentytwo["%  22:4 n-6"].values,name = "%22:4 n-6", mode='lines+markers')), row=1, col=2)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo["%  22:5 n-3"].index, y = EPA_twentytwo["%  22:5 n-3"].values,name = "%22:5 n-3", mode='lines+markers')), row=2, col=1)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo["%  22:5 n-6"].index, y = DHA_twentytwo["%  22:5 n-6"].values, name = "%22:5 n-6", mode='lines+markers')), row=2, col=1)    

    fig7.add_trace((go.Scatter( x = DHA_twentytwo["%  22:6 n-3 DHA"].index, y = DHA_twentytwo["%  22:6 n-3 DHA"].values,name = "%22:6 n-3 DHA", mode='lines+markers')), row=2, col=2)

    fig7.update_layout(height=500, width=1000,
                      title_text="Percent of 22:X and DHA Compounds")
    fig7.update_xaxes(tickangle=60)
    ######################
    fig8 = make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes = True, vertical_spacing = 0.2,                        subplot_titles=("24:0","24:1"))

    fig8.add_trace((go.Scatter( x = twentyfour["%  24:0"].index, y = twentyfour["%  24:0"].values,name = "%24:0", mode='lines+markers')), row=1, col=1)

    fig8.add_trace((go.Scatter( x = twentyfour["%  24:1"].index, y = twentyfour["%  24:1"].values,name = "%24:1", mode='lines+markers')), row=2, col=1)

    fig8.update_layout(height=500, width=1000,
                      title_text="Percent of 24:0 and 24:1 Compounds")
    fig8.update_xaxes(tickangle=60)
    ######################
    fig9 = make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.5,                        subplot_titles=("% Fat","% Unknown"))

    fig9.add_trace((go.Scatter( x = percent_fat[" %Fat (as FAME) using RRFs"].index, y = percent_fat[" %Fat (as FAME) using RRFs"].values,                               name = "%Fat (as FAME) using RRFs", mode='lines+markers')), row=1, col=1)

    fig9.add_trace((go.Scatter( x = unknown["% unknown"].index, y = unknown["% unknown"].values,name = "%unknown", mode='lines+markers')), row=2, col=1)
    fig9.update_xaxes(tickangle=60)
    fig9.update_layout(height=500, width=1000,
                      title_text="Percent of Unknown and Fat")
    ###########################
    fig11 = px.line(data_frame = dcw,x = dcw.index, y = dcw["DCW"].values, labels=dict(x="Samples", y="Amount (mg/g)"))
    fig11.update_layout(height=500, width=1000,
                  title_text="Dry Cell Weight of Samples" )
    fig11.update_xaxes(tickangle=60)
    fig11.update_traces(showlegend=False)
    fig11.update_traces(mode="markers+lines")

    ##########WASHED GRAPHS (concentration)#########

    tsmgfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("12:0 mg/g", "14:0 mg/g","16:0 mg/g", "16:1 mg/g" ))
    tsmgfig.add_trace((go.Scatter( x = tsmg["12:0"].index, y = tsmg["12:0"].values, name = "12:0 mg/g",
                                 mode = 'lines+markers')), row = 1, col = 1)
    tsmgfig.add_trace((go.Scatter( x = tsmg["14:0"].index, y = tsmg["14:0"].values, name = "14:0 mg/g",
                                 mode = 'lines+markers')), row = 1, col = 2)
    tsmgfig.add_trace((go.Scatter( x = tsmg["16:0"].index, y = tsmg["16:0"].values, name = "16:0 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 1)
    tsmgfig.add_trace((go.Scatter( x = tsmg["16:1"].index, y = tsmg["16:1"].values, name = "16:1 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 2)
    tsmgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 12:0, 14:0, 16:0, 16:1") 
    tsmgfig.update_xaxes(tickangle=60)
    ##############
    emgfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("18:0 mg/g", "18:1 n-9 mg/g and 18:1 n-7 mg/g","18:2 mg/g", "18:3 n-6 mg/g and 18:3 n-3 mg/g" ))
    emgfig.add_trace((go.Scatter( x = emg["18:0"].index, y = emg["18:0"].values, name = "18:0 mg/g",
                                 mode = 'lines+markers')), row = 1, col = 1)
    emgfig.add_trace((go.Scatter( x = emg["18:1 n-9"].index, y = emg["18:1 n-9"].values, name = "18:1 n-9 mg/g",
                                 mode = 'lines+markers')), row = 1, col = 2)
    emgfig.add_trace((go.Scatter( x = emg["18:1 n-7"].index, y = emg["18:1 n-7"].values, name = "18:1 n-7 mg/g",
                                 mode = 'lines+markers')), row = 1, col = 2)
    emgfig.add_trace((go.Scatter( x = emg["18:2"].index, y = emg["18:2"].values, name = "18:2 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 1)
    emgfig.add_trace((go.Scatter( x = emg["18:3 n-6"].index, y = emg["18:3 n-6"].values, name = "18:3 n-6 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 2)
    emgfig.add_trace((go.Scatter( x = emg["18:3 n-3"].index, y = emg["18:3 n-3"].values, name = "18:3 n-3 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 2)
    emgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 18:X") 
    emgfig.update_xaxes(tickangle=60)
    ##################
    immgfig = make_subplots(rows=2, cols=3, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("ARA mg/g", "DHA mg/g", "EPA mg/g","DPA n-3 mg/g","DPA n-6 mg/g", "20:3 n-6 mg/g" ))
    immgfig.add_trace((go.Scatter( x = immg["ARA"].index, y = immg["ARA"].values, name = "ARA mg/g",
                                 mode = 'lines+markers')), row = 1, col = 1)
    immgfig.add_trace((go.Scatter( x = immg["DHA"].index, y = immg["DHA"].values, name = "DHA mg/g",
                                 mode = 'lines+markers')), row = 1, col = 2)
    immgfig.add_trace((go.Scatter( x = immg["DPA n-3"].index, y = immg["DPA n-3"].values, name = "DPA n-3 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 1)
    immgfig.add_trace((go.Scatter( x = immg["DPA n-6"].index, y = immg["DPA n-6"].values, name = "DPA n-6 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 2)
    immgfig.add_trace((go.Scatter( x = immg["EPA"].index, y = immg["EPA"].values, name = "EPA mg/g",
                                 mode = 'lines+markers')), row = 1, col = 3)
    immgfig.add_trace((go.Scatter( x = immg["20:3 n-6 mg/g"].index, y = immg["20:3 n-6 mg/g"].values, name = "20:3 n-6 mg/g",
                                 mode = 'lines+markers')), row = 2, col = 3)
    immgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of ARA, DHA, DPA, EPA and 20:3") 
    immgfig.update_xaxes(tickangle=60)
    # <h2>Making the Web Browser Display

    figs = [fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig11,tsmgfig,emgfig,immgfig]
    figures_to_html(figs,filename= values[0] + ".html")
    show_in_window(values)

    
elif values["Fermentation"] == True and values["Non-Fermentation"] == False:
    excel = pd.read_excel(io = filepath ,sheet_name = 0)
    maxcol = len(excel.columns) - 1 #Grabbing the max column
    colnumber = range(0,maxcol,1) #Grabbing the list of columns numbers 
    #Re-assigning the new columns
    excel = pd.read_excel(io = filepath ,sheet_name = 0, usecols = colnumber)
    #Renames the Sample Column, sets it as the index and sorts the columns
    excel.rename(columns = {"Sample" : "Components"}, inplace = True)
    sortedexcel = excel.pivot_table(columns = "Components")

    try:
        sortedexcel["Type"] = SampleTypeKey(sortedexcel)
        sortedexcel["Hour"] = LogHour(sortedexcel)
        sortedexcel["Name"] = Name(sortedexcel)
        sortedexcel["Color"] = Color(sortedexcel)
        sortedexcel["Date"] = Time(sortedexcel)
        sortedexcel.reset_index(inplace = True)
        sortedexcel.rename(columns = {"index" : "Samples"}, inplace = True)
        sortedexcel.sort_values(by = ["Name","Type","Date", "Hour"],inplace = True, kind = "mergesort")
    except TypeError:
        sortedexcel.reset_index(inplace = True)
        sortedexcel.rename(columns = {"index" : "Samples"}, inplace = True)
        sortedexcel.sort_values(by = ["Samples"],inplace = True, kind = "mergesort")
    except ValueError:
            
        sortedexcel["Type"] = SampleTypeKey(sortedexcel)
        sortedexcel["Hour"] = LogHour(sortedexcel)
        sortedexcel["Name"] = Name(sortedexcel)
        sortedexcel["Color"] = Color(sortedexcel)
        sortedexcel["Num"] = SampleNumKey(sortedexcel)
        sortedexcel.reset_index(inplace = True)
        sortedexcel.rename(columns = {"index" : "Samples"}, inplace = True)
        sortedexcel.sort_values(by = ["Name","Num","Type", "Hour"],inplace = True, kind = "mergesort")
    ##########################################################
    #Assigning to seperate variables for graphing

    #Percentage
    eight_eleven = sortedexcel.loc[:,["Samples","Color","%  08:0","%  09:0", "%  10:0","%  11:0", "%  11:1"]]
    twelve_fourteen = sortedexcel.loc[:,["Samples","Color","%  12:0", "%  12:1", "%  13:0", "%  13:1", "%  14:0", "%  14:1"]]
    fifteen_sixteen = sortedexcel.loc[:,["Samples","Color","%  15:1","%  16:0","%  16:1","%  16:2", "%  16:3"]]
    seventeen_eighteen = sortedexcel.loc[:,["Samples","Color","%  17:0", "%  18:0", "%  18:1 n-7", "%  18:1 n-9", "%  18:2"]]
    eighteen_twenty = sortedexcel.loc[:,["Samples","Color","%  18:3 n-3","%  18:3 n-6","%  18:4 n-3","%  20:0","%  20:1 n-9"]]
    twenty_ARA = sortedexcel.loc[:,["Samples","Color","%  20:2", "%  20:3 n-3", "%  20:3 n-6","%  20:3 n-9", "%  20:4 ARA"]]
    EPA_twentytwo = sortedexcel.loc[:,["Samples","Color","%  20:5 n-3 EPA","%  22:0","%  22:1", "%  22:4 n-6", "%  22:5 n-3"]]
    DHA_twentytwo = sortedexcel.loc[:,["Samples","Color","%  22:5 n-6", "%  22:6 n-3 DHA", "% 22:2", "% 22:3"]]
    twentyfour = sortedexcel.loc[:,["Samples","Color","%  24:0", "%  24:1"]]
    unknown = sortedexcel.loc[:,["Samples","Color","% unknown"]]
    percent_fat = sortedexcel.loc[:,["Samples","Color"," %Fat (as FAME) using RRFs"]]
    #concentration
    tsmg = sortedexcel.loc[:,["Samples","Color","12:0","14:0","16:0","16:1"]]
    emg = sortedexcel.loc[:,["Samples","Color", "18:0", "18:1 n-9", "18:1 n-7","18:2", "18:3 n-6", "18:3 n-3"]]
    immg = sortedexcel.loc[:,["Samples","Color", "ARA", "DHA", "DPA n-3", "DPA n-6", "EPA", "20:3 n-6 mg/g"]]
    dcw = sortedexcel.loc[:,["Samples","Color","DCW"]]
    ############################################################
    #Creating the Washed dataframes for plotting
    eight_eleven_washed = NaNinsert_Washed(eight_eleven,sortedexcel)
    twelve_fourteen_washed = NaNinsert_Washed(twelve_fourteen,sortedexcel)
    fifteen_sixteen_washed = NaNinsert_Washed(fifteen_sixteen,sortedexcel)
    seventeen_eighteen_washed = NaNinsert_Washed(seventeen_eighteen,sortedexcel)
    eighteen_twenty_washed = NaNinsert_Washed(eighteen_twenty,sortedexcel)
    twenty_ARA_washed = NaNinsert_Washed(twenty_ARA,sortedexcel)
    EPA_twentytwo_washed = NaNinsert_Washed(EPA_twentytwo,sortedexcel)
    DHA_twentytwo_washed = NaNinsert_Washed(DHA_twentytwo,sortedexcel)
    twentyfour_washed = NaNinsert_Washed(twentyfour,sortedexcel)
    unknown_washed = NaNinsert_Washed(unknown,sortedexcel)
    percent_fat_washed = NaNinsert_Washed(percent_fat,sortedexcel)
    dcw_washed = NaNinsert_Washed(dcw,sortedexcel)
    tsmg_washed = NaNinsert_Washed(tsmg, sortedexcel)
    emg_washed = NaNinsert_Washed(emg, sortedexcel)
    immg_washed = NaNinsert_Washed(immg, sortedexcel)
    #############
    #Creating the Whole dataframes for plotting
    eight_eleven_whole = NaNinsert_Whole(eight_eleven,sortedexcel)
    twelve_fourteen_whole = NaNinsert_Whole(twelve_fourteen,sortedexcel)
    fifteen_sixteen_whole = NaNinsert_Whole(fifteen_sixteen,sortedexcel)
    seventeen_eighteen_whole = NaNinsert_Whole(seventeen_eighteen,sortedexcel)
    eighteen_twenty_whole = NaNinsert_Whole(eighteen_twenty,sortedexcel)
    twenty_ARA_whole = NaNinsert_Whole(twenty_ARA,sortedexcel)
    EPA_twentytwo_whole = NaNinsert_Whole(EPA_twentytwo,sortedexcel)
    DHA_twentytwo_whole = NaNinsert_Whole(DHA_twentytwo,sortedexcel)
    twentyfour_whole = NaNinsert_Whole(twentyfour,sortedexcel)
    unknown_whole = NaNinsert_Whole(unknown,sortedexcel)
    percent_fat_whole = NaNinsert_Whole(percent_fat,sortedexcel)
    dcw_whole = NaNinsert_Whole(dcw,sortedexcel)
    tsmg_whole = NaNinsert_Whole(tsmg, sortedexcel)
    emg_whole = NaNinsert_Whole(emg, sortedexcel)
    immg_whole = NaNinsert_Whole(immg, sortedexcel)
    ###########################################################
    #Making the Graphs
    #WASHED GRAPHS (Percentage)

    fig1 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.9, 0.9],                         subplot_titles=("% 08:0", "% 09:0", "% 10:0", "% 11:0","% 11:1"),                         vertical_spacing = 0.06,                         specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig1.add_trace((go.Scatter( x = eight_eleven_washed["%  08:0"].index, y = eight_eleven_washed["%  08:0"].values, name = " %08:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=1)

    fig1.add_trace((go.Scatter( x = eight_eleven_washed["%  09:0"].index, y = eight_eleven_washed["%  09:0"].values, name = " %09:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=2)

    fig1.add_trace((go.Scatter( x = eight_eleven_washed["%  10:0"].index, y = eight_eleven_washed["%  10:0"].values, name = "%10:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=1)

    fig1.add_trace((go.Scatter( x = eight_eleven_washed["%  11:0"].index, y = eight_eleven_washed["%  11:0"].values, name = "%11:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=2)

    fig1.add_trace((go.Scatter( x = eight_eleven_washed["%  11:1"].index, y = eight_eleven_washed["%  11:1"].values, name = "%11:1", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=3, col=2)    

    fig1.update_layout(height=600, width=1000,
                      title_text="Percent of 8:0, 9:0, 10:0, 11:0 and 11:1 Compounds (Washed Broth)")
    #####################

    fig2 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, vertical_spacing = 0.06,                        subplot_titles=("% 12:0", "% 12:1", "% 13:0", "% 13:1","% 14:0","% 14:1"))

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  12:0"].index, y = twelve_fourteen_washed["%  12:0"].values, name = " %12:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=1, )

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  12:1"].index, y = twelve_fourteen_washed["%  12:1"].values, name = " %12:1", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=2)

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  13:0"].index, y = twelve_fourteen_washed["%  13:0"].values, name = "%13:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=1)

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  13:1"].index, y = twelve_fourteen_washed["%  13:1"].values, name = "%13:1", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=2)

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  14:0"].index, y = twelve_fourteen_washed["%  14:0"].values, name = "%14:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=3, col=1)    

    fig2.add_trace((go.Scatter( x = twelve_fourteen_washed["%  14:1"].index, y = twelve_fourteen_washed["%  14:1"].values, name = "%14:1", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=3, col=2)

    fig2.update_layout(height=600, width=1000,
                      title_text="Percent of 12:0, 12:1, 13:0, 13:1, 14:0 and 14:1 Compounds (Washed Broth)")

    fig1.update_xaxes(tickangle=60)
    fig2.update_xaxes(tickangle=60)
    ##################
    fig3 = make_subplots(rows=3, cols=2, shared_yaxes= False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.06,                        subplot_titles=("% 15:1", "% 16:0", "% 16:1", "% 16:2","% 16:3"),                        specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig3.add_trace((go.Scatter( x = fifteen_sixteen_washed["%  15:1"].index, y = fifteen_sixteen_washed["%  15:1"].values, name = " %15:1", mode='lines+markers', marker_color = fifteen_sixteen_washed["Color"])), row=1, col=1)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen_washed["%  16:0"].index, y = fifteen_sixteen_washed["%  16:0"].values, name = " %16:0", mode='lines+markers', marker_color = fifteen_sixteen_washed["Color"])), row=1, col=2)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen_washed["%  16:1"].index, y = fifteen_sixteen_washed["%  16:1"].values, name = " %16:1", mode='lines+markers', marker_color = fifteen_sixteen_washed["Color"])), row=2, col=1)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen_washed["%  16:2"].index, y = fifteen_sixteen_washed["%  16:2"].values, name = "%16:2", mode='lines+markers', marker_color = fifteen_sixteen_washed["Color"])), row=2, col=2)

    fig3.add_trace((go.Scatter( x = fifteen_sixteen_washed["%  16:3"].index, y = fifteen_sixteen_washed["%  16:3"].values, name = "%16:3", mode='lines+markers', marker_color = fifteen_sixteen_washed["Color"])), row=3, col=2)    

    fig3.update_layout(height=500, width=1000,
                      title_text="Percent of 15:1, 16:0, 16:1, 16:2 and 16:3 Compounds (Washed Broth)")

    ########

    fig4 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.05,                        subplot_titles=("%  17:0", "%  18:0", "%  18:1 n-7", "%  18:1 n-9","%  18:2"),                        specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig4.add_trace((go.Scatter( x = seventeen_eighteen_washed["%  17:0"].index,                               y = seventeen_eighteen_washed["%  17:0"].values, name = "%17:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=1)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen_washed["%  18:0"].index,                               y = seventeen_eighteen_washed["%  18:0"].values, name = "%18:0", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=1, col=2)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen_washed["%  18:1 n-7"].index,                               y = seventeen_eighteen_washed["%  18:1 n-7"].values, name = "%18:1 n-7", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=1)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen_washed["%  18:1 n-9"].index,                               y = seventeen_eighteen_washed["%  18:1 n-9"].values, name = "%18:1 n-9", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=2, col=2)

    fig4.add_trace((go.Scatter( x = seventeen_eighteen_washed["%  18:2"].index,                               y = seventeen_eighteen_washed["%  18:2"].values, name = "%18:2", mode='lines+markers', marker_color = eight_eleven_washed["Color"])), row=3, col=2)    

    fig4.update_layout(height=600, width=1000,
                      title_text="Percent of 17:0, 18:0, 18:1 n-7, 18:1 n-9 and 18:2 Compounds (Washed Broth)")

    fig3.update_xaxes(tickangle=60)
    fig4.update_xaxes(tickangle=60)
    #####
    fig5 = make_subplots(rows=1, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7], vertical_spacing = 0.02,                        subplot_titles=("% 18:3 n-3, % 18:3 n-6 and % 18:4 n-3", "%  20:0 and % 20:1 n-9"))

    fig5.add_trace((go.Scatter( x = eighteen_twenty_washed["%  18:3 n-3"].index, y = eighteen_twenty_washed["%  18:3 n-3"].values, name = "%18:3 n-3", mode='lines+markers',                               marker_color = eighteen_twenty_washed["Color"])), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty_washed["%  18:3 n-6"].index, y = eighteen_twenty_washed["%  18:3 n-6"].values, name = "%18:3 n-6", mode='lines+markers',                              marker_color = eighteen_twenty_washed["Color"])), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty_washed["%  18:4 n-3"].index, y = eighteen_twenty_washed["%  18:4 n-3"].values, name = "%18:4 n-3", mode='lines+markers',                              marker_color = eighteen_twenty_washed["Color"])), row=1, col=1)

    fig5.add_trace((go.Scatter( x = eighteen_twenty_washed["%  20:0"].index, y = eighteen_twenty_washed["%  20:0"].values, name = "%20:0", mode='lines+markers',                              marker_color = eighteen_twenty_washed["Color"])), row=1, col=2)

    fig5.add_trace((go.Scatter( x = eighteen_twenty_washed["%  20:1 n-9"].index, y = eighteen_twenty_washed["%  20:1 n-9"].values, name = "%20:1 n-9", mode='lines+markers',                              marker_color = eighteen_twenty_washed["Color"])), row=1, col=2)    

    fig5.update_layout(height=500, width=1000,
                      title_text="Percent of 18:3, 18:4, 20:0 and 20:1 Compounds (Washed Broth)")

    ######

    fig6 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.6, 0.6], vertical_spacing = 0.2,                        subplot_titles=("% 20:2 and % 20:3 n-3", "% ARA", "% 20:3 n-9 and % 20:3 n-6","% EPA"))

    fig6.add_trace((go.Scatter( x = twenty_ARA_washed["%  20:2"].index, y = twenty_ARA_washed["%  20:2"].values, name = "%20:2",mode='lines+markers',                              marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA_washed["%  20:3 n-3"].index, y = twenty_ARA_washed["%  20:3 n-3"].values, name = "%20:3 n-3", mode='lines+markers',                              marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA_washed["%  20:3 n-6"].index, y = twenty_ARA_washed["%  20:3 n-6"].values, name = "%20:3 n-6", mode='lines+markers',                              marker_color = twenty_ARA_washed["Color"])), row=2, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA_washed["%  20:3 n-9"].index, y = twenty_ARA_washed["%  20:3 n-9"].values, name = "%20:3 n-9", mode='lines+markers',
                              marker_color = twenty_ARA_washed["Color"])), row=2, col=1)

    fig6.add_trace((go.Scatter( x = twenty_ARA_washed["%  20:4 ARA"].index, y = twenty_ARA_washed["%  20:4 ARA"].values, name = "%20:4 ARA", mode='lines+markers',                              marker_color = twenty_ARA_washed["Color"])), row=1, col=2)    

    fig6.add_trace((go.Scatter( x = EPA_twentytwo_washed["%  20:5 n-3 EPA"].index, y = EPA_twentytwo_washed["%  20:5 n-3 EPA"].values, name = "%20:5 n-3 EPA", mode='lines+markers',                              marker_color = twenty_ARA_washed["Color"])), row=2, col=2)

    fig6.update_layout(height=500, width=1000,
                      title_text="Percent of 20:2, 20:3, ARA and EPA Compounds  (Washed Broth)")
    ###
    fig5.update_xaxes(tickangle=60)
    fig6.update_xaxes(tickangle=60)
    ###
    fig7 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7],                         vertical_spacing = 0.2, subplot_titles=("% 22:0 and % 22:1", "% 22:2, % 22:3 and % 22:4 n-6", "% 22:5 n-3 and % 22:5 n-6", "% DHA"))

    fig7.add_trace((go.Scatter( x = EPA_twentytwo_washed["%  22:0"].index, y = EPA_twentytwo_washed["%  22:0"].values,                               name = "%22:0", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo_washed["%  22:1"].index, y = EPA_twentytwo_washed["%  22:1"].values,                               name = "%22:1", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo_washed["% 22:2"].index, y = DHA_twentytwo_washed["% 22:2"].values,                               name = "% 22:2", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=2)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo_washed["% 22:3"].index, y = DHA_twentytwo_washed["% 22:3"].values,                               name = "% 22:3", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=2)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo_washed["%  22:4 n-6"].index, y = EPA_twentytwo_washed["%  22:4 n-6"].values,                               name = "%22:4 n-6", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=2)

    fig7.add_trace((go.Scatter( x = EPA_twentytwo_washed["%  22:5 n-3"].index, y = EPA_twentytwo_washed["%  22:5 n-3"].values,                               name = "%22:5 n-3", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=2, col=1)

    fig7.add_trace((go.Scatter( x = DHA_twentytwo_washed["%  22:5 n-6"].index, y = DHA_twentytwo_washed["%  22:5 n-6"].values,                               name = "%22:5 n-6", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=2, col=1)    

    fig7.add_trace((go.Scatter( x = DHA_twentytwo_washed["%  22:6 n-3 DHA"].index, y = DHA_twentytwo_washed["%  22:6 n-3 DHA"].values,                               name = "%22:6 n-3 DHA", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=2, col=2)

    fig7.update_layout(height=500, width=1000,
                      title_text="Percent of 22:X and DHA Compounds (Washed Broth)")
    fig7.update_xaxes(tickangle=60)
    ######################
    fig8 = make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes = True, vertical_spacing = 0.2,                        subplot_titles=("24:0","24:1"))

    fig8.add_trace((go.Scatter( x = twentyfour_washed["%  24:0"].index, y = twentyfour_washed["%  24:0"].values,                               name = "%24:0", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig8.add_trace((go.Scatter( x = twentyfour_washed["%  24:1"].index, y = twentyfour_washed["%  24:1"].values,                               name = "%24:1", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=2, col=1)

    fig8.update_layout(height=500, width=1000,
                      title_text="Percent of 24:0 and 24:1 Compounds (Washed Broth)")
    fig8.update_xaxes(tickangle=60)
    ######################
    fig9 = make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.5,                        subplot_titles=("% Fat","% Unknown"))

    fig9.add_trace((go.Scatter( x = percent_fat_washed[" %Fat (as FAME) using RRFs"].index, y = percent_fat_washed[" %Fat (as FAME) using RRFs"].values,                               name = "%Fat (as FAME) using RRFs", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=1, col=1)

    fig9.add_trace((go.Scatter( x = unknown_washed["% unknown"].index, y = unknown_washed["% unknown"].values,                               name = "%unknown", mode='lines+markers', marker_color = twenty_ARA_washed["Color"])), row=2, col=1)
    fig9.update_xaxes(tickangle=60)
    fig9.update_layout(height=500, width=1000,
                      title_text="Percent of Unknown and Fat (Washed Broth)")
    ###########################
    fig11 = px.line(data_frame = dcw_washed,x = dcw_washed.index, y = dcw_washed["DCW"].values, labels=dict(x="Samples", y="Amount (mg/g)"),                color = "Color", hover_data = {"Color" : False})
    fig11.update_layout(height=500, width=1000,
                  title_text="Dry Cell Weight of Washed Broth Samples" )
    fig11.update_xaxes(tickangle=60)
    fig11.update_traces(showlegend=False)
    fig11.update_traces(mode="markers+lines")
    #############################
    #WHOLE BROTH GRAPHS
    fig10 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.9, 0.9],                          vertical_spacing = 0.2,                          subplot_titles=("% 08:0", "% 09:0","% 10:0","% 11:0","","% 11:1"),
                         specs=[[{},{}],\
                                [{},{}],\
                                [None,{}]])

    fig10.add_trace((go.Scatter( x = eight_eleven_whole["%  08:0"].index,    y = eight_eleven_whole["%  08:0"].values, name = " % 08:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])),                    row=1, col=1)

    fig10.add_trace((go.Scatter( x = eight_eleven_whole["%  09:0"].index,    y = eight_eleven_whole["%  09:0"].values, name = " % 09:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])),                    row=1, col=2)

    fig10.add_trace((go.Scatter( x = eight_eleven_whole["%  10:0"].index,    y = eight_eleven_whole["%  10:0"].values, name = "% 10:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])),                    row=2, col=1)

    fig10.add_trace((go.Scatter( x = eight_eleven_whole["%  11:0"].index,    y = eight_eleven_whole["%  11:0"].values, name = "% 11:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])),                    row=2, col=2)

    fig10.add_trace((go.Scatter( x = eight_eleven_whole["%  11:1"].index,    y = eight_eleven_whole["%  11:1"].values, name = "% 11:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])),                    row=3, col=2)    

    fig10.update_layout(height=600, width=1000,
                      title_text="Percent of 8:0, 9:0, 10:0, 11:0 and 11:1 Compounds (Whole Broth)")
    #####################

    fig20 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True,                          vertical_spacing = 0.2,                         subplot_titles=("% 12:0", "% 12:1","% 13:0","% 13:1","% 14:0","% 14:1"))

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  12:0"].index,    y = twelve_fourteen_whole["%  12:0"].values, name = " % 12:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1, )

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  12:1"].index,    y = twelve_fourteen_whole["%  12:1"].values, name = " % 12:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  13:0"].index,    y = twelve_fourteen_whole["%  13:0"].values, name = "% 13:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=1)

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  13:1"].index,    y = twelve_fourteen_whole["%  13:1"].values, name = "% 13:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=2)

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  14:0"].index,    y = twelve_fourteen_whole["%  14:0"].values, name = "% 14:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=3, col=1)    

    fig20.add_trace((go.Scatter( x = twelve_fourteen_whole["%  14:1"].index,    y = twelve_fourteen_whole["%  14:1"].values, name = "% 14:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=3, col=2)

    fig20.update_layout(height=600, width=1000,
                      title_text="Percent of 12:0, 12:1, 13:0, 13:1, 14:0 and 14:1 Compounds (Whole Broth)")
    fig10.update_xaxes(tickangle=60)
    fig20.update_xaxes(tickangle=60)
    ######
    fig30 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True,                    column_widths = [0.5, 0.7], vertical_spacing = 0.2,                         subplot_titles=("% 15:1", "% 16:0", "% 16:1", "% 16:2","% 16:3"),                                specs= [[{},{}],                                [{},{}],                                [None,{}]])

    fig30.add_trace((go.Scatter( x = fifteen_sixteen_whole["%  15:1"].index, y = fifteen_sixteen_whole["%  15:1"].values,                name = "% 15:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig30.add_trace((go.Scatter( x = fifteen_sixteen_whole["%  16:0"].index, y = fifteen_sixteen_whole["%  16:0"].values,                name = "% 16:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)

    fig30.add_trace((go.Scatter( x = fifteen_sixteen_whole["%  16:1"].index, y = fifteen_sixteen_whole["%  16:1"].values,                name = "% 16:1", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=1)

    fig30.add_trace((go.Scatter( x = fifteen_sixteen_whole["%  16:2"].index, y = fifteen_sixteen_whole["%  16:2"].values,                name = "% 16:2", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=2)

    fig30.add_trace((go.Scatter( x = fifteen_sixteen_whole["%  16:3"].index, y = fifteen_sixteen_whole["%  16:3"].values,                name = "% 16:3", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=3, col=2)    

    fig30.update_layout(height=500, width=1000,
                      title_text="Percent of 15:1, 16:0, 16:1, 16:2 and 16:3 Compounds (Whole Broth)")

    ########

    fig40 = make_subplots(rows=3, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7],                          vertical_spacing = 0.2, subplot_titles=("%  17:0", "%  18:0", "%  18:1 n-7", "%  18:1 n-9","%  18:2"),                         specs=[[{},{}],                                [{},{}],                                [None,{}]])

    fig40.add_trace((go.Scatter( x = seventeen_eighteen_whole["%  17:0"].index, y = seventeen_eighteen_whole["%  17:0"].values,                name = "%17:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig40.add_trace((go.Scatter( x = seventeen_eighteen_whole["%  18:0"].index, y = seventeen_eighteen_whole["%  18:0"].values,                name = "%18:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)

    fig40.add_trace((go.Scatter( x = seventeen_eighteen_whole["%  18:1 n-7"].index, y = seventeen_eighteen_whole["%  18:1 n-7"].values, name = "%18:1 n-7",                mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=1)

    fig40.add_trace((go.Scatter( x = seventeen_eighteen_whole["%  18:1 n-9"].index, y = seventeen_eighteen_whole["%  18:1 n-9"].values,                name = "%18:1 n-9", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=2)

    fig40.add_trace((go.Scatter( x = seventeen_eighteen_whole["%  18:2"].index, y = seventeen_eighteen_whole["%  18:2"].values,                name = "%18:2", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=3, col=2)    

    fig40.update_layout(height=600, width=1000,
                      title_text="Percent of 17:0, 18:0, 18:1 n-7, 18:1 n-9 and 18:2 Compounds (Whole Broth)")

    fig30.update_xaxes(tickangle=60)
    fig40.update_xaxes(tickangle=60)
    ########
    fig50 = make_subplots(rows=1, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7],                          vertical_spacing = 0.02, subplot_titles=("% 18:3 n-3, % 18:3 n-6 and % 18:4 n-3", "% 20:0 and %  20:1 n-9"))

    fig50.add_trace((go.Scatter( x = eighteen_twenty_whole["%  18:3 n-3"].index, y = eighteen_twenty_whole["%  18:3 n-3"].values,                                name = "%18:3 n-3", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig50.add_trace((go.Scatter( x = eighteen_twenty_whole["%  18:3 n-6"].index, y = eighteen_twenty_whole["%  18:3 n-6"].values,                                name = "%18:3 n-6", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig50.add_trace((go.Scatter( x = eighteen_twenty_whole["%  18:4 n-3"].index, y = eighteen_twenty_whole["%  18:4 n-3"].values,                                name = "%18:4 n-3", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig50.add_trace((go.Scatter( x = eighteen_twenty_whole["%  20:0"].index, y = eighteen_twenty_whole["%  20:0"].values,                                name = "%20:0", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)

    fig50.add_trace((go.Scatter( x = eighteen_twenty_whole["%  20:1 n-9"].index, y = eighteen_twenty_whole["%  20:1 n-9"].values,                                name = "%20:1 n-9", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)    

    fig50.update_layout(height=500, width=1000,
                      title_text="Percent of 18:3, 18:4, 20:0 and 20:1 Compounds (Whole Broth)")

    ######

    fig60 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True, column_widths = [0.5, 0.7],                          vertical_spacing = 0.2,subplot_titles=("% 20:2 and % 20:3 n-3", "% ARA", "%  20:3 n-9 and %  20:3 n-6", "% EPA"))

    fig60.add_trace((go.Scatter( x = twenty_ARA_whole["%  20:2"].index, y = twenty_ARA_whole["%  20:2"].values,                                name = "%20:2", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig60.add_trace((go.Scatter( x = twenty_ARA_whole["%  20:3 n-3"].index, y = twenty_ARA_whole["%  20:3 n-3"].values,                                name = "%20:3 n-3", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=1)

    fig60.add_trace((go.Scatter( x = twenty_ARA_whole["%  20:3 n-6"].index, y = twenty_ARA_whole["%  20:3 n-6"].values,                                name = "%20:3 n-6", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=1)

    fig60.add_trace((go.Scatter( x = twenty_ARA_whole["%  20:3 n-9"].index, y = twenty_ARA_whole["%  20:3 n-9"].values,                                name = "%20:3 n-9", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=1)

    fig60.add_trace((go.Scatter( x = twenty_ARA_whole["%  20:4 ARA"].index, y = twenty_ARA_whole["%  20:4 ARA"].values,                                name = "%20:4 ARA", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=1, col=2)    

    fig60.add_trace((go.Scatter( x = EPA_twentytwo_whole["%  20:5 n-3 EPA"].index, y = EPA_twentytwo_whole["%  20:5 n-3 EPA"].values,                                name = "%20:5 n-3 EPA", mode='lines+markers', marker_color = eight_eleven_whole["Color"])), row=2, col=2)

    fig60.update_layout(height=500, width=1000,
                      title_text="Percent of 20:2, 20:3, ARA and EPA Compounds  (Whole Broth)")
    fig50.update_xaxes(tickangle=60)
    fig60.update_xaxes(tickangle=60)
    ########
    fig70 = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = True,                          column_widths = [0.5, 0.7], vertical_spacing = 0.05,                        subplot_titles=("% 22:0 and % 22:1","% 22:2, % 22:3 and % 22:4 n-6" , "% 22:5 n-3 and % 22:5 n-6", "% DHA") )

    fig70.add_trace((go.Scatter( x = EPA_twentytwo_whole["%  22:0"].index, y = EPA_twentytwo_whole["%  22:0"].values,                                name = "% 22:0", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=1)

    fig70.add_trace((go.Scatter( x = EPA_twentytwo_whole["%  22:1"].index, y = EPA_twentytwo_whole["%  22:1"].values,                                name = "% 22:1", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=1)

    fig70.add_trace((go.Scatter( x = DHA_twentytwo_whole["% 22:2"].index, y = DHA_twentytwo_whole["% 22:2"].values,                                name = "% 22:2", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=2)

    fig70.add_trace((go.Scatter( x = DHA_twentytwo_whole["% 22:3"].index, y = DHA_twentytwo_whole["% 22:3"].values,                                name = "% 22:3", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=2)

    fig70.add_trace((go.Scatter( x = EPA_twentytwo_whole["%  22:4 n-6"].index, y = EPA_twentytwo_whole["%  22:4 n-6"].values,                                name = "% 22:4 n-6", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=2)

    fig70.add_trace((go.Scatter( x = EPA_twentytwo_whole["%  22:5 n-3"].index, y = EPA_twentytwo_whole["%  22:5 n-3"].values,                                name = "% 22:5 n-3", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=2, col=1)

    fig70.add_trace((go.Scatter( x = DHA_twentytwo_whole["%  22:5 n-6"].index, y = DHA_twentytwo_whole["%  22:5 n-6"].values,                                name = "% 22:5 n-6", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=2, col=1)    

    fig70.add_trace((go.Scatter( x = DHA_twentytwo_whole["%  22:6 n-3 DHA"].index, y = DHA_twentytwo_whole["%  22:6 n-3 DHA"].values,                                name = "% 22:6 n-3 DHA", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=2, col=2)

    fig70.update_layout(height=500, width=1000,
                      title_text="Percent of 22:X and DHA Compounds (Whole Broth)")
    fig70.update_xaxes(tickangle=60)
    #################
    fig80 = make_subplots(rows=2, cols=1, shared_yaxes=False,                          shared_xaxes = True, vertical_spacing = 0.05,                         subplot_titles=("%  24:0", "% 24:1"))

    fig80.add_trace((go.Scatter( x = twentyfour_whole["%  24:0"].index, y = twentyfour_whole["%  24:0"].values,                                name = "% 24:0", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=1, col=1)

    fig80.add_trace((go.Scatter( x = twentyfour_whole["%  24:1"].index, y = twentyfour_whole["%  24:1"].values,                                name = "% 24:1", mode='lines+markers', marker_color = twentyfour_whole["Color"])), row=2, col=1)

    fig80.update_layout(height=500, width=1000,
                      title_text="Percent of 24:0 and 24:1 Compounds (Whole Broth)")
    fig80.update_xaxes(tickangle=60)
    #################
    fig90 = make_subplots(rows=2, cols=1, shared_yaxes=False,                          shared_xaxes = False, vertical_spacing = 0.60,                         subplot_titles=("% Fat", "% Unknown"))

    fig90.add_trace((go.Scatter( x = percent_fat_whole[" %Fat (as FAME) using RRFs"].index, y = percent_fat_whole[" %Fat (as FAME) using RRFs"].values,                                name = "% Fat (as FAME)",                                mode='lines+markers',                               marker_color = percent_fat_whole["Color"])), row=1, col=1)

    fig90.add_trace((go.Scatter( x = unknown_whole["% unknown"].index, y = unknown_whole["% unknown"].values,                                name = "%unknown",                                mode='lines+markers',                               marker_color = unknown_whole["Color"])), row=2, col=1)

    fig90.update_layout(height=500, width=1000,
                      title_text="Percent of Unknown and Fat (Whole Broth)")

    fig90.update_xaxes(tickangle=60)
    ###############
    fig100 = px.line(data_frame = dcw_whole, x = dcw_whole.index, y = dcw_whole["DCW"].values, labels=dict(x="Samples", y="Amount (mg/g)"),                color = "Color", hover_data = {"Color" : False})
    fig100.update_layout(height=500, width=1000,
                  title_text="Dry Cell Weight of Whole Broth Samples" )
    fig100.update_xaxes(tickangle=60)
    fig100.update_traces(showlegend=False)
    fig100.update_traces(mode="markers+lines")
    #######################################
    ##########WASHED GRAPHS (concentration)#########

    tsmgfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("12:0 mg/g", "14:0 mg/g","16:0 mg/g", "16:1 mg/g" ))
    tsmgfig.add_trace((go.Scatter( x = tsmg_washed["12:0"].index, y = tsmg_washed["12:0"].values, name = "12:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_washed["Color"])), row = 1, col = 1)
    tsmgfig.add_trace((go.Scatter( x = tsmg_washed["14:0"].index, y = tsmg_washed["14:0"].values, name = "14:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_washed["Color"])), row = 1, col = 2)
    tsmgfig.add_trace((go.Scatter( x = tsmg_washed["16:0"].index, y = tsmg_washed["16:0"].values, name = "16:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_washed["Color"])), row = 2, col = 1)
    tsmgfig.add_trace((go.Scatter( x = tsmg_washed["16:1"].index, y = tsmg_washed["16:1"].values, name = "16:1 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_washed["Color"])), row = 2, col = 2)
    tsmgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 12:0, 14:0, 16:0, 16:1 (Washed Broth)") 
    tsmgfig.update_xaxes(tickangle=60)
    ##############
    emgfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("18:0 mg/g", "18:1 n-9 mg/g and 18:1 n-7 mg/g","18:2 mg/g", "18:3 n-6 mg/g and 18:3 n-3 mg/g" ))
    emgfig.add_trace((go.Scatter( x = emg_washed["18:0"].index, y = emg_washed["18:0"].values, name = "18:0 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 1, col = 1)
    emgfig.add_trace((go.Scatter( x = emg_washed["18:1 n-9"].index, y = emg_washed["18:1 n-9"].values, name = "18:1 n-9 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 1, col = 2)
    emgfig.add_trace((go.Scatter( x = emg_washed["18:1 n-7"].index, y = emg_washed["18:1 n-7"].values, name = "18:1 n-7 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 1, col = 2)
    emgfig.add_trace((go.Scatter( x = emg_washed["18:2"].index, y = emg_washed["18:2"].values, name = "18:2 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 2, col = 1)
    emgfig.add_trace((go.Scatter( x = emg_washed["18:3 n-6"].index, y = emg_washed["18:3 n-6"].values, name = "18:3 n-6 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 2, col = 2)
    emgfig.add_trace((go.Scatter( x = emg_washed["18:3 n-3"].index, y = emg_washed["18:3 n-3"].values, name = "18:3 n-3 mg/g",
                                 mode = 'lines+markers', marker_color = emg_washed["Color"])), row = 2, col = 2)
    emgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 18:X (Washed Broth)") 
    emgfig.update_xaxes(tickangle=60)
    ##################
    immgfig = make_subplots(rows=2, cols=3, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("ARA mg/g", "DHA mg/g", "EPA mg/g","DPA n-3 mg/g","DPA n-6 mg/g", "20:3 n-6 mg/g"))
    immgfig.add_trace((go.Scatter( x = immg_washed["ARA"].index, y = immg_washed["ARA"].values, name = "ARA mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 1, col = 1)
    immgfig.add_trace((go.Scatter( x = immg_washed["DHA"].index, y = immg_washed["DHA"].values, name = "DHA mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 1, col = 2)
    immgfig.add_trace((go.Scatter( x = immg_washed["DPA n-3"].index, y = immg_washed["DPA n-3"].values, name = "DPA n-3 mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 2, col = 1)
    immgfig.add_trace((go.Scatter( x = immg_washed["DPA n-6"].index, y = immg_washed["DPA n-6"].values, name = "DPA n-6 mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 2, col = 2)
    immgfig.add_trace((go.Scatter( x = immg_washed["EPA"].index, y = immg_washed["EPA"].values, name = "EPA mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 1, col = 3)
    immgfig.add_trace((go.Scatter( x = immg_washed["20:3 n-6 mg/g"].index, y = immg_washed["20:3 n-6 mg/g"].values, name = "20:3 n-6 mg/g",
                                 mode = 'lines+markers', marker_color = immg_washed["Color"])), row = 2, col = 3)
    immgfig.update_layout(height=600, width=1000,
                      title_text="Concentration of ARA, DHA, DPA, EPA and 20:3 (Washed Broth)") 
    immgfig.update_xaxes(tickangle=60)
    #WHOLE GRAPHS (concentration)

    tsmgwbfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("12:0 mg/g", "14:0 mg/g","16:0 mg/g", "16:1 mg/g" ))
    tsmgwbfig.add_trace((go.Scatter( x = tsmg_whole["12:0"].index, y = tsmg_whole["12:0"].values, name = "12:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_whole["Color"])), row = 1, col = 1)
    tsmgwbfig.add_trace((go.Scatter( x = tsmg_whole["14:0"].index, y = tsmg_whole["14:0"].values, name = "14:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_whole["Color"])), row = 1, col = 2)
    tsmgwbfig.add_trace((go.Scatter( x = tsmg_whole["16:0"].index, y = tsmg_whole["16:0"].values, name = "16:0 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_whole["Color"])), row = 2, col = 1)
    tsmgwbfig.add_trace((go.Scatter( x = tsmg_whole["16:1"].index, y = tsmg_whole["16:1"].values, name = "16:1 mg/g",
                                 mode = 'lines+markers', marker_color = tsmg_whole["Color"])), row = 2, col = 2)
    tsmgwbfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 12:0, 14:0, 16:0, 16:1 (Whole Broth)") 
    tsmgwbfig.update_xaxes(tickangle=60)
    ######

    emgwbfig = make_subplots(rows=2, cols=2, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("18:0 mg/g", "18:1 n-9 mg/g and 18:1 n-7 mg/g","18:2 mg/g", "18:3 n-6 mg/g and 18:3 n-3 mg/g" ))
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:0"].index, y = emg_whole["18:0"].values, name = "18:0 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 1, col = 1)
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:1 n-9"].index, y = emg_whole["18:1 n-9"].values, name = "18:1 n-9 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 1, col = 2)
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:1 n-7"].index, y = emg_whole["18:1 n-7"].values, name = "18:1 n-7 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 1, col = 2)
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:2"].index, y = emg_whole["18:2"].values, name = "18:2 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 2, col = 1)
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:3 n-6"].index, y = emg_whole["18:3 n-6"].values, name = "18:3 n-6 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 2, col = 2)
    emgwbfig.add_trace((go.Scatter( x = emg_whole["18:3 n-3"].index, y = emg_whole["18:3 n-3"].values, name = "18:3 n-3 mg/g",
                                 mode = 'lines+markers', marker_color = emg_whole["Color"])), row = 2, col = 2)
    emgwbfig.update_layout(height=600, width=1000,
                      title_text="Concentration of 18:X (Whole Broth)") 
    emgwbfig.update_xaxes(tickangle=60)
    #####

    immgwbfig = make_subplots(rows=2, cols=3, shared_yaxes=False, shared_xaxes = False, vertical_spacing = 0.40,                         subplot_titles=("ARA mg/g", "DHA mg/g", "EPA mg/g","DPA n-3 mg/g","DPA n-6 mg/g", "20:3 n-6 mg/g"))
    immgwbfig.add_trace((go.Scatter( x = immg_whole["ARA"].index, y = immg_whole["ARA"].values, name = "ARA mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 1, col = 1)
    immgwbfig.add_trace((go.Scatter( x = immg_whole["DHA"].index, y = immg_whole["DHA"].values, name = "DHA mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 1, col = 2)
    immgwbfig.add_trace((go.Scatter( x = immg_whole["DPA n-3"].index, y = immg_whole["DPA n-3"].values, name = "DPA n-3 mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 2, col = 1)
    immgwbfig.add_trace((go.Scatter( x = immg_whole["DPA n-6"].index, y = immg_whole["DPA n-6"].values, name = "DPA n-6 mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 2, col = 2)
    immgwbfig.add_trace((go.Scatter( x = immg_whole["EPA"].index, y = immg_whole["EPA"].values, name = "EPA mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 1, col = 3)
    immgwbfig.add_trace((go.Scatter( x = immg_whole["20:3 n-6 mg/g"].index, y = immg_whole["20:3 n-6 mg/g"].values, name = "20:3 n-6 mg/g",
                                 mode = 'lines+markers', marker_color = immg_whole["Color"])), row = 2, col = 3)
    immgwbfig.update_layout(height=600, width=1000,
                      title_text="Concentration of ARA, DHA, DPA, EPA and 20:3 (Whole Broth)") 
    immgwbfig.update_xaxes(tickangle=60)

    # <h2>Making the Web Browser Display
    # In[4]:


    figs = [fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8,fig9,fig11,tsmgfig,emgfig,immgfig,fig10,fig20,fig30,fig40,fig50,fig60,fig70,fig80,fig90,fig100,tsmgwbfig,emgwbfig,immgwbfig ]
    figures_to_html(figs,filename= values[0] + ".html")
    show_in_window(values)

elif values["Fermentation"] == False and values["Non-Fermentation"] == False:
    if event == "Execute":
        sg.popup("Error: You need to select a FAME data type.", font=('Times New Roman',20))





# In[ ]:




