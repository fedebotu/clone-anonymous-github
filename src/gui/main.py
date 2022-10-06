import PySimpleGUI as gui
import webbrowser
import darkdetect

from src.gui.images import LOGO_B64
from src.download import download_repo
from src.config import load_config, get_config_from_values
from src.utils import ThreadWithException

DEFAULT_THEME = 'Reddit'
DEFAULT_FONT = 'Calibri 12'
MAX_WIDTH = 60
APP_NAME = "Clone Anonymous Github"
APP_VERSION = "0.2.0"
GITHUB_PAGE = "https://github.com/fedebotu/clone-anonymous-github"
MAIN_TEXT = "Easily clone/download Anonymous Github repositories from anonymous.4open.science with a GUI interface"
MAIN_HELP_TEXT = "Copy and paste the URL of a target repository (should work also from a file, its parent repo will be targeted), select your download folder and press the clone button. You may stop the download thread at any time by pressing the stop button. "
ABOUT_TEXT = 'Easily clone/download Anonymous Github repositories from anonymous.4open.science with a GUI interface\n\nA thanks to all contributors, including tdurieux for the website and ShoufaChen, kynehc for their download scripts!'
HELP_TEXT_VIRUS = "Windows may flag the program as a virus since it contains browser automation. But hey, guess what, it isn`t :) Try to temporarily deactivate or make an exception in Windows Defender."
HELP_TEXT_OTHER = "Did you encounter another bug? Feel free to search/open an issue on GitHub!"

# Set theme
if not darkdetect.isDark():
    gui.theme("LightGrey")
    BACKGROUND_COLOR = "#232020"
    INPUT_BACKGROUND_COLOR = '#ADD8E6'
    gui.theme_background_color(BACKGROUND_COLOR)
    gui.theme_text_element_background_color(BACKGROUND_COLOR)
    gui.theme_text_color("White")
    gui.theme_button_color((BACKGROUND_COLOR, INPUT_BACKGROUND_COLOR))
    gui.theme_input_background_color(INPUT_BACKGROUND_COLOR)
    gui.theme_input_text_color('#000000')
    TAB_TEXT_COLOR="Black"
else:
    BACKGROUND_COLOR = "#FAFAFA"
    INPUT_BACKGROUND_COLOR = '#0079D3'
    TAB_TEXT_COLOR="White"
    gui.theme("LightGrey")


def main_page():
    """Main page"""

    config = load_config()

    layout_tab1 = [
        [gui.Text('Clone Anonymous Github', font='Calibri 14')],
        [gui.Text(MAIN_TEXT, size=(MAX_WIDTH, 2))],
        [gui.Text('Get started', font='Calibri 12')],
        [gui.Text(MAIN_HELP_TEXT, size=(MAX_WIDTH, 5))],
        [gui.Text(f'Target URL')],
        [gui.InputText('', key='url', tooltip='Your Anonymous Github URL you want to clone')],
        [gui.Text('Choose download folder', justification='right')],
        [gui.InputText(config['save_dir'], key='save_dir'), gui.FolderBrowse(tooltip='Choose target download folder')]
        ]

    layout_tab2 = [
        [gui.Text('Maximum connections')],
        [gui.Slider(range=(1, 512), default_value=config['max_conns'], orientation='h', size=(MAX_WIDTH//2, 10), key='max_conns', tooltip='Maximum number of concurrent connections')],
        [gui.Text('Maximum retries')],
        [gui.Slider(range=(1, 10), default_value=config['max_retry'], orientation='h', size=(MAX_WIDTH//2, 10), key='max_retry', tooltip='Maximum number of retries for each file')]
    ]

    layout_tab3 = [
        [gui.Text('Virus Detection',font='Calibri 16')],
        [gui.Text(HELP_TEXT_VIRUS, size=(MAX_WIDTH, 4), enable_events=True)],
        [gui.Text('Other Bugs',font='Calibri 16')],
        [gui.Text(HELP_TEXT_OTHER, size=(MAX_WIDTH, 4), enable_events=True)],
        [gui.Button("Github Issues")],
        ]

    layout_tab4 = [
        [gui.Text(APP_NAME, font="Calibri 18")],
        [gui.Column([[gui.Image(data=LOGO_B64, size=(150,150), subsample=(2))]], justification='center')],
        [gui.Text(ABOUT_TEXT, size=(MAX_WIDTH, 6))],
        [gui.Text(f"Application version: {APP_VERSION}",font=DEFAULT_FONT)],
        [gui.Button("Github Repository"),gui.Button("Official Anonymous Github Page")],
    ]

    layout = [[gui.TabGroup([[gui.Tab('Main', layout_tab1, title_color='Blue',
                                tooltip='Main settings', background_color=BACKGROUND_COLOR),
                             gui.Tab('Advanced Settings', layout_tab2, title_color='Blue',
                                tooltip='Extra stuff you might want to look into', background_color=BACKGROUND_COLOR),
                            gui.Tab('Help', layout_tab3, title_color='Blue',
                                tooltip='For quick help', background_color=BACKGROUND_COLOR),
                             gui.Tab('About', layout_tab4, title_color='Blue',
                                tooltip='About page and details', background_color=BACKGROUND_COLOR),
                            ]], background_color=BACKGROUND_COLOR, tab_background_color=INPUT_BACKGROUND_COLOR, title_color=TAB_TEXT_COLOR)],
    
            [[gui.Text('Debug window', font=("Calibri", 18))],
            [gui.Multiline("", size=(MAX_WIDTH, 20), autoscroll=True, reroute_stdout=True, reroute_stderr=True, key='STDOUT', disabled=True)],
            [gui.Button('Clone', tooltip='Run program with current configuration'), gui.Button('Stop', tooltip='Stop current run'), gui.Button('Exit')],]]
            

    window = gui.Window(APP_NAME, layout, icon=LOGO_B64)

    thread = None    
    driver = None
    while True:
        event, values = window.read(timeout=10)

        if event == 'Clone':
            print('Starting downloads...')
            config = get_config_from_values(values)
            thread = ThreadWithException(target=download_repo,  args=(config,))
            thread.start()
            
        elif event == 'Stop':
            if thread:
                thread.raise_exception()
                print("Run was manually terminated")
                thread = None
            else:
                print("No thread is currently running")

        elif event == "Github Repository":
            webbrowser.open(GITHUB_PAGE,2)
        elif event == "Official Anonymous Github Page":
            webbrowser.open("https://anonymous.4open.science/",2)
        elif event == "Github Issues":
            webbrowser.open(GITHUB_PAGE+'/issues',2)
        elif event == gui.WIN_CLOSED or event == 'Exit':
            break

    print("Closing remaing threads and windows...")
    if thread: thread.raise_exception()
    if driver: 
        # driver.close()
        driver.quit()
    window.close()
    exit()



if __name__ == "__main__":
    main_page()