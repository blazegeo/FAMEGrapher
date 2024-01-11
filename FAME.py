import sys
import PySimpleGUI as sg
import threading
import plotly.io as pio
sg.theme("DarkTeal12")
layout = [[sg.Text("FAME Graph File Location:", font=('Times New Roman', 16)),
           sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
           sg.FileBrowse()], [sg.Text("What type of FAME data is this?", font=('Times New Roman', 16))],
          [sg.Radio("Fermentation", "type", key="Fermentation"),
           sg.Radio("Non-Fermentation", "type", key="Non-Fermentation")],
          [sg.Text('Enter Name of Output HTML:', font=('Times New Roman', 16))], [sg.Input(do_not_clear=False)],
          [sg.Button("Execute"),sg.Button("Close")],
          [sg.ProgressBar(max_value=10, orientation='h', size=(20, 20), key='progress')]
          ]

window = sg.Window("FAME Grapher", layout, margins=(100, 100), element_justification='c')

# Element of the progress bar to make updating easier
progress_bar = window['progress']

while True:
    event, values = window.read()


    if event == "Execute" and values["Fermentation"] == False and values["Non-Fermentation"] == True:
        sav_values = values  # to grab the inputs
        pio.templates.default = "plotly_dark"
        filepath = values["-FILE-"]
        from Functions import figures_to_html_nonferm
        html = threading.Thread(target = figures_to_html_nonferm, args = (values[0] + ".html", filepath, progress_bar))
        html.run()

        if not html.is_alive():
            progress_bar.update_bar(10)
            from Functions import show_in_window

            vis = threading.Thread(target=show_in_window, args=(sav_values,))
            vis.run()

    elif event == "Execute" and values["Fermentation"] == False and values["Non-Fermentation"] == False:
        sav_values = values  # to grab the inputs
        pio.templates.default = "plotly_dark"
        filepath = values["-FILE-"]
        from Functions import figures_to_html_ferm
        html = threading.Thread(target=figures_to_html_ferm, args=(values[0] + ".html", filepath, progress_bar))
        html.run()

        if not html.is_alive():
            progress_bar.update_bar(10)
            from Functions import show_in_window

            vis = threading.Thread(target=show_in_window, args=(sav_values,))
            vis.run()



    elif event == "Execute" and values["Fermentation"] == False and values["Non-Fermentation"] == False:
            sg.popup("Error: You need to select a FAME data type.", font=('Times New Roman', 20))

    elif event == "Close" or sg.WIN_CLOSED:
        break

window.close()




















