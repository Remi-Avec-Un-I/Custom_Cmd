import json
import os
import sys
import time
# import urllib.request
import random as rd
from dataclasses import dataclass
rn = time.time()
 
 
@dataclass
class List:
    name: str
    original: str
 
@dataclass
class Command:
    name: str
    alias: list[str]
    descrition: list[str]
    arguments: list[str]

class Shell:
    
    path = os.getenv('APPDATA') + "\\Shell\\"
    
    commands = {
        "leave": ["exit", "leave", "quit"],
        "help" : ["help", "h", "-help", "-h", "--help", "--h", "?"],
        "setup" : ["setup", "config", "configure"],
        "pwd"   : ["pwd", "cd"],
        "randnum" : ["randint", "randomint", "random", "rdint", "rd", "randnum", "rand"],
        "art" : ["art", "1-line"],
        "calc" : ["calc", "calculator", "calcul", "calculatrice"],
        "preset" : ["preset", "pst", "new_command", "add_command", "add_preset", "add_preset", "custom_command", "custom_preset"],
        
        
        # Left are linux commands, right are windows commands.
        "liste" : {
            "ls"        : "dir", 
            "mv"        : "ren",
            "cp"        : "copy",
            "mv"        : "move",
            "clear"     : "cls",
            "rm"        : "del",
            "diff"      : "fc"
                
        }
        
    }
    
    
    color_panel = {
        "BLACK"           : 30,
        "RED"             : 31,
        "GREEN"           : 32,
        "YELLOW"          : 33,
        "BLUE"            : 34,
        "MAGENTA"         : 35,
        "CYAN"            : 36,
        "WHITE"           : 37,
        "RESET"           : 39,
        "LIGHTBLACK_EX"   : 90,
        "LIGHTRED_EX"     : 91,
        "LIGHTGREEN_EX"   : 92,
        "LIGHTYELLOW_EX"  : 93,
        "LIGHTBLUE_EX"    : 94,
        "LIGHTMAGENTA_EX" : 95,
        "LIGHTCYAN_EX"    : 96,
        "LIGHTWHITE_EX"   : 97
    }
    
    back_color_panel = {
        "_BLACK"          : 40,
        "_RED"            : 41,
        "_GREEN"          : 42,
        "_YELLOW"         : 43,
        "_BLUE"           : 44,
        "_MAGENTA"        : 45,
        "_CYAN"           : 46,
        "_WHITE"          : 47,
        "_RESET"          : 49,
        "_LIGHTBLACK_EX"  : 100,
        "_LIGHTRED_EX"    : 101,
        "_LIGHTGREEN_EX"  : 102,
        "_LIGHTYELLOW_EX" : 103,
        "_LIGHTBLUE_EX"   : 104,
        "_LIGHTMAGENTA_EX": 105,
        "_LIGHTCYAN_EX"   : 106,
        "_LIGHTWHITE_EX"  : 107
    }
    
    style_panel = {
        "RESET"           : 0,
        "BOLD"            : 1,
        "DIM"             : 2,
        "ITALIC"          : 3,
        "UNDERLINE"       : 4,
        "BLINK"           : 5,
        "REVERSE"         : 7,
        "STRIKTHROUGH"    : 9
    }
    

    def __init__(self):
        """Initialize the shell."""
        
        
        if os.path.isfile(self.path + 'settings\\settings.json'):
            self.is_settings = True   
        
        else:
            self.is_settings = False       
            self.entry_prompt = '> '
            os.mkdir(self.path + 'settings')
            with open(self.path + 'settings\\settings.json', 'w+') as f:
                json.dump({"prompt" : [], "title" : [], "selected_language" : [], "preset" : {}}, f, indent=4)
            
                
        if os.path.isfile(self.path + 'settings\\language.json'):
            pass
        else:
            import urllib.request
            
            print(self.color("YELLOW", "The language file doesn't exist yet. Downloading it..."))
            urllib.request.urlretrieve("https://raw.githubusercontent.com/Remi-Avec-Un-I/Custom_Cmd/main/language.json", 
                                       self.path + 'settings\\language.json')
            print(self.color("GREEN", "Downloaded."))
            
        
        try:
            # Load art.py.
            with open(self.path + 'settings\\art.py', 'r', encoding='utf-8') as f:
                art = f.read()
                art = art.split('\n')
                art = art[1:]
                art = '\n'.join(art)
                art = '{' + art
                self.art_dict = dict(eval(art))
            
        except:
            import urllib.request
            
            print(self.color("YELLOW", "The art file, for the art command doesn't exist. Downloading it..."))
            urllib.request.urlretrieve("https://raw.githubusercontent.com/Remi-Avec-Un-I/Custom_Cmd/main/art.py",
                                       self.path + 'settings\\art.py')
            try:
                with open(self.path + 'settings\\art.py', 'r', encoding='utf-8') as f:
                    art = f.read()
                    art = art.split('\n')
                    art = art[1:]
                    art = '\n'.join(art)
                    art = '{' + art
                    self.art_dict = dict(eval(art))
            except:
                print(self.color("RED", "The art file, for the art command, is corrupted. \nPlease contact the creator (on github : https://github.com/Remi-Avec-Un-I)."))

        
        print(self.color("CYAN", f"{self.color('WHITE', 'Shell')} {self.color('CYAN', 'started')} {self.color('WHITE', f'in {time.time() - rn} seconds.')}"))



    # Main function, where the shell is started using infinite loop.
    def run(self):
        """Run the shell."""
        while True:
            is_command = False
            self.txt = self.get_json(self.path + 'settings\\language.json')
            self.settings = self.get_json(self.path + 'settings\\settings.json')
            if self.is_settings:
                self.entry_prompt = self.prompt()
                
            usage = self.get_json(self.path + 'settings\\language.json')["usage"][self.get_lang()]
            self.commands = []
            for i in usage:
                self.commands.append(
                    Command(i, usage[i]["Alias"], usage[i]["Description"], usage[i]["Arguments"])
                )
                
            List_egal_command = self.get_json(self.path + 'settings\\language.json')["List_egal_command"]
            for i in List_egal_command:
                self.commands.append(
                    List(i, List_egal_command[i])
                )
            # self.get_commands("List"))
            # self.get_commands("Command"))
            command = input(self.entry_prompt).lower()
            commands = self.get_List()
            
            
            # Check for command in List dataclass.
            if command == "":
                pass
            elif command.split()[0] in commands.keys():
                try:
                    os.system(f"{commands[command.split()[0]]} {command.split()[1]}")
                except:
                    os.system(commands[command.split()[0]])
                is_command = True
                    
            else: 
                commands = self.get_commands('Command')
                for val in self.commands:
                    try:
                        val = getattr(val, "alias")
                    except: 
                        val = []
                    if command.split()[0] in val and is_command == False:
                        
                        try:
                            args = command.split()[1:]
                            getattr(self, val[0])(command.split()[1:])
                        except IndexError:
                            try:
                                getattr(self, val[0])()
                                break
                            except Exception as e:
                                print(e)
                                print(self.texte("arg_error")[0] + command.split()[0] + self.texte("arg_error")[1])
                        finally:
                            is_command = True
                                 
            if not is_command:
                try:
                    os.system(command)
                except Exception as e:
                    print(e)

    # Create the prompt, with the current parameters.
    def prompt(self):
        entry_prompt = []
            
        settings = self.settings
            
            
        if settings["title"] != "":
            os.system(f"title {''.join(settings['title'])}")
        
        if settings["prompt"] == [""]:
            return ''
        elif settings["prompt"] == []:
            return '> '
        
        for item in settings["prompt"]:
            if item == "**path**":
                entry_prompt.append(os.getcwd())
                            
            elif item == "**user**":
                entry_prompt.append(os.getlogin())
                            
            elif item == "**host**":
                entry_prompt.append(sys.platform)
                
            elif item == "**hour**":
                entry_prompt.append(time.strftime("%H", time.localtime()))                            
            elif item == "**minute**":
                entry_prompt.append(time.strftime("%M", time.localtime()))
            elif item == "**second**":
                entry_prompt.append(time.strftime("%S", time.localtime()))
            elif item == "**day**":
                entry_prompt.append(time.strftime("%d", time.localtime()))
            elif item == "**month**":
                entry_prompt.append(time.strftime("%m", time.localtime()))
            elif item == "**year**":
                entry_prompt.append(time.strftime("%Y", time.localtime()))
                
            elif item in self.color_panel.keys():
                entry_prompt.append("\033[" + str(self.color_panel[item]) + 'm')
                
            elif item in self.back_color_panel.keys():
                entry_prompt.append("\033[" + str(self.back_color_panel[item]) + "m")
                
            elif item in self.style_panel.keys():
                entry_prompt.append("\033[" + str(self.style_panel[item]) + "m") 
                
            else:
                entry_prompt.append(item)

                    
        return ''.join(entry_prompt)
    
    def color(self, color, tx=False):
        if tx:
            return f"\033[{self.color_panel[color]}m{tx}\033[0m"
        return f"\033[{self.color_panel[color]}m"
    
    def back(self, color, tx=False):
        if tx:
            return f"\033[{self.back_color_panel[color]}m{tx}\033[0m"
        return f"\033[{self.back_color_panel[color]}m"
    
    def style(self, style, tx=False):
        if tx:
            return f"\033[{self.style_panel[style]}m{tx}\033[0m"
        return f"\033[{self.style_panel[style]}m"
    
    def reset(self):
        return f"\033[0m"
    
    # Return [somthings] with color
    def hook(self, tx, clr='YELLOW'):
        return f"[\033[{self.color_panel[clr]}m{tx}\033[0m]"
    
    """    
    def up(self, line=1):
        for i in self.counter:
            if i != 0:
                print("\033[F")
            else:
                print(f"\033[{int(i/os.get_terminal_size().columns)}F")
        
        print(f"\033[{line}F" + (" " * os.get_terminal_size().columns + "\n") * (line)) # get_terminal_size to replace with blank
        return f"\033[{line+2}F"
    """

    """
    # Custom print to count the lines used to be able to replace them with blank
    def cprint(self, *objects, sep=' ', end='\n', file=sys.stdout, flush=False):
        # count the lines used by objects
        for i in ''.join(objects).splitlines():
            if i[-1:] == '\n':
                self.counter += 1
            self.counter.append(len(i))

        print(*objects, sep=sep, end=end, file=file, flush=flush)
    """
    
    # Preventing the shell from closing in case of ValueError.
    def intinput(self, tx, clr='RED', log=False):
        fail = "\033[F"
        while True:
            choice = input(tx)
            try:
                choice = int(choice)
                if log:
                    self.log.append((tx, choice))
                return choice
            except:
                print(fail + self.color(clr, self.texte("int_error")))
                if fail == "\033[F":
                    fail = "\033[F\033[F"
            
    # Create a menu to choose an option.
    def menu(self, options):
        """Print a menu."""
        for option, index in zip(options, range(len(options))):
            print(f"[{self.color('YELLOW', f'{index + 1}')}] {option}")
            
    # Get json variables. 
    def get_json(self, file):
        with open(file, 'r', encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
        
    # To get texte from language file.
    def texte(self, name):
        return self.txt["texte"][self.get_lang()][name]
    
    # To get all commands.
    def get_commands(self, data=False):
        commands = []
        for i in self.commands:
            if not data:
                commands.append(i.name)
            elif data and type(i).__name__ == data:
                commands.append(i.name)
                
        return commands
    
    # To get a dict of List commands.
    def get_List(self):
        liste = dict()
        for i in self.commands:
            if type(i).__name__ == "List":
                liste[i.name] = i.original
        return liste
    
    # To get the data of a specfiic command.
    def get_datacmd(self, name):
        for i in self.commands:
            if i.name == name:
                return i
    
    
    # Change json content, or replace
    def in_json(self, file, value, key="prompt", replace=False, new_element=False):
        """
        Use to append or replace a value in a json file.
        """
        loaded = self.get_json(file)
        
        if not new_element:
            if not replace:
                loaded[key].append(value)
            else:
                loaded[key] = [value]
        else:
            if isinstance(value, list):
                loaded[key] = [''.join(value)]
        
        with open(file, 'w', encoding="utf-8") as f:
            json.dump(loaded, f, indent=4)
    
    # Return the current language.
    def get_lang(self):
        if self.settings["selected_language"] != []:
            return ''.join(self.settings["selected_language"])
        else:
            return "en"
        
    # Used to modify or create a preset, in preset()
    def modify_preset(self, texte, name, new_element=False):
        with open(self.path + 'settings\\settings.json', 'r', encoding="utf-8") as f:
            f = json.load(f)
        if not new_element:
            f["preset"][name].append(texte)
            self.in_json(self.path + 'settings\\settings.json', f, replace=True)
            """
            try:
                self.in_json(self.path + 'settings\\settings.json', texte, key="preset")
            except:
                self.in_json(self.path + 'settings\\settings.json', texte, key="preset", new_element=True)
            """
        else:
            try:
                self.in_json(self.path + 'settings\\settings.json', texte, key="preset", new_element=True)
            except:
                pass
    
    
    # Return the help for a command.
    def get_help(self, command):
        dict_help = self.txt["usage"][self.get_lang()][command]
            
        text = f"{self.color('GREEN', list(dict_help.keys())[0])} : "
        for x in dict_help[list(dict_help.keys())[0]]:
            text += f"{x}, "
        text = text[:-2]
        text += f"\n{self.color('GREEN', list(dict_help.keys())[1])} : {''.join(dict_help['Description'])}\n"
        text += f"{self.color('GREEN', list(dict_help.keys())[2])} : "
        for x in dict_help[list(dict_help.keys())[2]]:
            text += f"{x}\n"

        return text
        
    # Command : leave
    def leave(self, help=False):
        """Exit the shell."""
        if ''.join(help) in self.get_datacmd("help").alias:
            print(self.get_help("leave"))
        else:
            sys.exit(0)
            
    # Command : help
    def help(self, wnd_help=False):
        if wnd_help == "all":
            os.system("help")
            print("\n\n")
        
        print(self.get_commands("List"))
        for cmd in self.get_commands("Command"):
            print(self.txt[self.get_lang()][cmd])
        for cmd in self.get_List().keys():
            print(cmd  + " " *(12 - len(cmd)) + self.texte("help_liste") + self.get_List()[cmd])
        
                
    # Command : setup (pretty big one isn't it ?)
    def setup(self, help=False):
        """Setup the shell."""
        if ''.join(help) in self.get_datacmd("help").alias:
            print(self.get_help("setup"))
            
        else:
            text = self.txt["texte"][self.get_lang()]
            print(f"{self.color('GREEN', tx=text['welcome'])}")
            self.menu(text["choice"])
            
            choice = self.intinput(f"{self.hook('?')} > ")
            """
            1 : Prompt
            2 : Language
            3 : Exit
            """
            
            
            if choice == 1:
                
                print(self.color("GREEN", text['prompt']))
                
                while True:
                    
                    self.menu(text['prompt_choice'])
                    self.entry_prompt = self.prompt()
                    
                    choice = self.intinput(f"{text['prompt_look']} {self.entry_prompt}\n{self.hook('?')} > ")
                    """
                    1 : Path
                    2 : Time
                    3 : User
                    4 : Host
                    5 : Color
                    6 : Style
                    7 : Window Title
                    8 : Custom text
                    9 : Reset
                    10: Exit
                    """
                    
                    if choice == 1:
                        """Adding path"""
                        self.in_json(self.path + 'settings\\settings.json', "**path**")
                        
                        
                    elif choice == 2:
                        """Adding the time"""
                        
                        self.menu(text['time'])
                        while (choice := self.intinput(f"{self.hook('?')} > ")) != 8:
                            """
                            1 : Custom text (to separate the time for exemple)
                            2 : Year
                            3 : Month
                            4 : Day
                            5 : Hour
                            6 : Minute
                            7 : Second
                            8 : Exit
                            """
                            if choice == 1:
                                custom = input(text["custom_text"])
                                self.in_json(self.path + 'settings\\settings.json', custom)
                            
                            elif choice == 2:
                                self.in_json(self.path + 'settings\\settings.json', "**year**")
                            elif choice == 3:
                                self.in_json(self.path + 'settings\\settings.json', "**month**")
                            elif choice == 4:
                                self.in_json(self.path + 'settings\\settings.json', "**day**")
                            elif choice == 5:
                                self.in_json(self.path + 'settings\\settings.json', "**hour**")
                            elif choice == 6:
                                self.in_json(self.path + 'settings\\settings.json', "**minute**")
                            elif choice == 7:
                                self.in_json(self.path + 'settings\\settings.json', "**second**")
                        print("\n\n")
                        
                    elif choice == 3:
                        """Adding user"""
                        self.in_json(self.path + 'settings\\settings.json', "**user**")
                        
                    elif choice == 4:
                        """Adding the hostname"""
                        self.in_json(self.path + 'settings\\settings.json', "**host**")
                        
                    elif choice == 5:
                        """Adding the color"""
                        finish = False
                        
                        self.menu(text['color_type'])
                        choice_color = self.intinput(f"{self.hook('?')} > ")
                        """
                        1 : Foreground
                        2 : Background
                        3 : Back
                        """
                        while not finish:
                            if choice_color == 1:
                                print(text["color_exemple"][0] + self.color("BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = self.intinput(f"{self.hook('?')} > ")
                                """
                                [1-9] : Color
                                10 : More
                                11 : Exit
                                """
                                prefix = ""
                                
                            elif choice_color == 2:
                                print(text["color_exemple"][0] + self.back("_BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = self.intinput(f"{self.hook('?')} > ")
                                """
                                [1-9] : Color
                                10 : More
                                11 : Exit
                                """
                                prefix = "_"
                                
                            elif choice_color == 3:
                                finish = True
                                choice = 0
                            
                            if choice == 10:
                                while not finish:
                                    self.menu(text["color_choice_2"])
                                    choice = self.intinput(f"{self.hook('?')} > ")
                                    """
                                    [1-8] : Color
                                    9 : Back
                                    """
                                    if choice in range(1, 8):
                                        self.in_json(self.path + 'settings\\settings.json', f"{prefix}{list(self.color_panel.keys())[choice-1+9]}")
                                        
                                    elif choice == 9:
                                        finish = True
                                finish = False
                            
                            elif choice == 11:
                                finish = True
                            
                            elif choice in range(1, 9):
                                self.in_json(self.path + 'settings\\settings.json', f"{prefix}{list(self.color_panel.keys())[choice-1]}")
                            
                    elif choice == 6:
                        """Adding the style"""
                        finish = False
                        while not finish:
                            for i, index in zip(text["style_choice"], range(len(text["style_choice"]))):
                                if i == "Exit":
                                    print(self.hook("8") + " Exit")
                                else:
                                    print("[" + self.color("YELLOW", str(index + 1)) + "] " + self.style(i.upper(), i))
                            
                            choice = self.intinput(f"{self.hook('?')} > ")
                            """
                            [1-7] : Different Style
                            8 : Exit
                            """
                            
                            if choice == 1:
                                """Adding bold style"""
                                self.in_json(self.path + 'settings\\settings.json', "BOLD")
                                
                            elif choice == 2:
                                """Adding dim style"""
                                self.in_json(self.path + 'settings\\settings.json', "DIM")
                            
                            elif choice == 3:
                                """Adding italic style"""
                                self.in_json(self.path + 'settings\\settings.json', "ITALIC")
                                
                            elif choice == 4:
                                """Adding underline style"""
                                self.in_json(self.path + 'settings\\settings.json', "UNDERLINE")
                                
                            elif choice == 5:
                                """Adding blink style"""
                                self.in_json(self.path + 'settings\\settings.json', "BLINK")
                                
                            elif choice == 6:
                                """Adding reverse style"""
                                self.in_json(self.path + 'settings\\settings.json', "REVERSE")
                                
                            elif choice == 7:
                                """Adding strikethrough style"""
                                self.in_json(self.path + 'settings\\settings.json', "STRIKETHROUGH")
                                
                            elif choice == 8:
                                """Exiting the style"""
                                finish = True
                        
                    
                    elif choice == 7:
                        title = input(text["title"])
                        """
                        Choose the name  of the windows :
                        """
                        self.in_json(self.path + 'settings\\settings.json', title, key="title", replace=True)
                        
                    elif choice == 8:
                        custom = input(text["custom_text"])
                        """
                        Enter your text :
                        """
                        self.in_json(self.path + 'settings\\settings.json', custom)
                                                
                    elif choice == 9:
                        """Reset the prompt"""
                        self.in_json(self.path + 'settings\\settings.json', "", replace=True)
                        print(text["reset"])
                        
                    elif choice == 10:
                        """Go back"""
                        return 
                    
            elif choice == 2:
                finish = False
                while not finish:
                    self.menu(list(self.txt["texte"].keys()))
                    print(self.hook(0) + self.txt["texte"][self.get_lang()]["exit"])
                    
                    choice = self.intinput(f"{self.hook('?')} > ")
                    """
                    [1-...] : All available languages
                    0 : Exit 
                    """
                    
                    if choice == 0:
                        finish = True
                    elif choice > len(list(self.txt["texte"].keys())):
                        print(self.color("RED", text["language_error"]))
                    else:
                        self.in_json(self.path + 'settings\\settings.json', list(self.txt["texte"].keys())[choice-1], 
                                     key="selected_language", replace=True)
                        finish = True
                finish = False
                
    # Command : pwd
    def pwd(self, path):
        if path[0] in self.get_datacmd("help").alias:
            print(self.get_help("pwd"))
            return
        try:
            os.chdir(' '.join(path).replace("\\", "\\\\"))
        except Exception as e:
            print(e)
    
    # Command : randnum
    def randnum(self, args):
        if args[0] in self.get_datacmd("help").alias:
            print(self.get_help("randnum"))
            return
        
        if len(args) == 1:
            try:
                print(rd.randint(0, int(args[0])))
            except:
                print(self.texte("value_error"))
            
        else:
            try: 
                if args[-1] == "float":
                    print(rd.uniform(float(args[0]), float(args[1])))
                else:
                    print(rd.randint(int(args[0]), int(args[1])))
            except ValueError:
                print(self.texte("value_error"))
    

    # Command : art
    def art(self, args=['']):
        if args[0] in self.get_datacmd("help").alias:
            print(self.get_help("art"))
        
        elif self.art_dict:
            if args[0] == "random" or args == ['']:
                print(list(self.art_dict.values())[rd.randint(0, len(list(self.art_dict.keys())))])
            else:
                try:
                    print(self.art_dict[' '.join(args)])
                except:
                    print(self.texte("art_error") + list(self.art_dict.keys())[rd.randint(0, len(list(self.art_dict.keys())))])
                    
        else:
            print(self.color("RED", self.texte("art_error_2")))
                    
    # Command : calc
    def calc(self, args):
        if args[0] in self.get_datacmd("help").alias:
            print(self.get_help("calc"))

        else:
            try:
                print(eval(' '.join(args)))
            except Exception:
                print(self.texte("calc_error"))
                
    # Command : preset
    def preset(self, args=['']):
        if args[0] in self.get_datacmd("help").alias:
            print(self.get_help("preset"))
        
        else:
            self.menu(self.txt["texte"][self.get_lang()]["preset"])
            choice = self.intinput(f"{self.hook('?')} > ")
            """
            1 : Create a new preset command
            2 : Modify a preset command
            3 : Delete a preset command
            4 : Exit
            """
            if choice == 1: # Create a preset command
                finish = False  
                
                print(self.txt["texte"][self.get_lang()]["preset_name"])
                preset_name = input(f"{self.hook('?')} > ")           
                while not finish:
                    """
                    Enter the name of the preset command :
                    """
                    
                    self.menu(self.txt["texte"][self.get_lang()]["preset_list2"])
                    choice = self.intinput(f"{self.hook('?')} > ")
                    """
                    1 : Start an application
                    2 : Create a file/folder
                    3 : Write in a file
                    4 : Excecute a command in the terminal
                    5 : Exit
                    """
                    
                    if choice == 1: # Start an application
                        self.menu(self.txt["texte"][self.get_lang()]["app_list"])
                        app_choice = self.intinput(f"{self.hook('?')} > ")
                        """
                        1 : From startup folder
                        2 : From the path
                        """
                        
                        if app_choice == 1: # From startup folder
                            path = "C:/Users/" + os.getlogin() + "/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"
                            apps = []
                            for _, _, files in os.walk(path, topdown=False):
                                for name in files:
                                    if name.endswith((".lnk", ".url", ".bat", ".exe", ".py", ".jar", ".msi", ".vbs")):
                                        apps.append(os.path.join(name))
                            self.menu(apps)
                            print(self.hook(0) + self.txt["texte"][self.get_lang()]["back"])
                            app_choice = self.intinput(f"{self.hook('?')} > ")
                            """
                            [Not assign] : All application in the startup folder
                            [Last] : Back
                            """
                            if app_choice == 0:
                                pass
                            else:
                                try:
                                    self.in_json(self.path + 'settings\\settings.json', "start:" + apps[app_choice-1], key="preset")
                                except Exception as e:
                                    print(e)
                                    self.in_json(self.path + 'settings\\settings.json', "start:" + apps[app_choice-1], key="preset", new_element=True)
                            
                        elif app_choice == 2: # From path
                            
                            while not (os.path.isfile(app_choice := input(f"{self.hook(self.get_json(self.path + 'settings/language.json')['texte'][self.get_lang()]['app_choice'])} > "))):
                                """
                                The full path of the application :
                                """
                                pass
                            
                            try:
                                self.in_json(self.path + 'settings\\settings.json', "start:" + app_choice, key="preset")
                            except:
                                self.in_json(self.path + 'settings\\settings.json', "start: " + app_choice, key="preset", new_element=True)
                    
                    elif choice == 2: # Create a file/folder
                        
                        self.menu(self.txt["texte"][self.get_lang()]["create_file"])
                        choice = self.intinput(f"{self.hook('?')} > ")
                        
                        """
                        1 : File
                        2 : Folder
                        
                        """
                        if choice == 1:
                            print(self.color("GREEN", self.txt['texte'][self.get_lang()]['file_name']))
                            name = input(f"{self.hook('?')} > ")
                            """
                            Enter the name of the file :
                            """
                            self.modify_preset("create_file:" + name, preset_name)
                            
                    elif choice == 5:
                        break


shell = Shell()
shell.run()
