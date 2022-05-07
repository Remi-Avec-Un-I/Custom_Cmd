import json
import os
import sys
import time
import numpy as np
import urllib.request


class Shell:

    def __init__(self):
        """Initialize the shell."""
        
        self.path = os.getenv('APPDATA') + "\\Shell\\"
        if os.path.isfile(self.path + 'settings\\settings.json'):
            self.is_settings = True   
        
        else:
            self.is_settings = False       
            self.entry_prompt = '> '
            os.mkdir(self.path + 'settings')
            with open(self.path + 'settings\\settings.json', 'w+') as f:
                json.dump({"prompt" : [], "title" : [], "selected_language" : []}, f, indent=4)
        
        self.color_panel = {
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
        
        self.back_color_panel = {
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
        
        self.style_panel = {
            "RESET"           : 0,
            "BOLD"            : 1,
            "DIM"             : 2,
            "ITALIC"          : 3,
            "UNDERLINE"       : 4,
            "BLINK"           : 5,
            "REVERSE"         : 7,
            "STRIKTHROUGH"    : 9
        }
            

                
        if os.path.isfile(self.path + 'settings\\language.json'):
            pass
        else:
            print(self.color("YELLOW", "The language file doesn't exist yet. Downloading it..."))
            urllib.request.urlretrieve("https://raw.githubusercontent.com/Remi-Avec-Un-I/Custom_Cmd/main/language.json?token=GHSAT0AAAAAABUDSGYFJZJOD6JDGPDYHEQ4YTWSAMA", self.path + 'settings\\language.json')
            print(self.color("GREEN", "Downloaded."))
            
            
        
        self.commands = {
            "leave": ["exit", "leave", "quit"],
            "help" : ["help", "h", "-help", "-h", "--help", "--h", "?"],
            "setup" : ["setup", "config", "configure"],
            "pwd"   : ["pwd", "cd"],
            "randint" : ["randint", "randomint", "random", "rdint"],
            "art" : ["art", "1-line"],
            
            
            # Left are linux commands, right are windows commands.
            "liste" : {
                "ls" : "dir", 
                "mv" : "ren",
                "cp" : "copy",
                "mv" : "move",
                "clear" : "cls",
                "rm" : "del",
                "diff" : "fc"
                 
            }
            
        }
        
        try:
            # Load art.py.
            with open(self.path + 'settings__\\art.py', 'r', encoding='utf-8') as f:
                art = f.read()
                art = art.split('\n')
                art = art[1:]
                art = '\n'.join(art)
                art = '{' + art
                self.art_dict = dict(eval(art))
            
        except:
            self.art = False


    # Main function, where the shell is started using infinite loop.
    def run(self):
        """Run the shell."""
        
        while True:
            is_command = False
            if self.is_settings:
                self.entry_prompt = self.prompt()
                
            command = input(self.entry_prompt).lower()
            
            if command == "":
                pass
            elif command.split()[0] in self.commands["liste"]:
                try:
                    os.system(f"{self.commands['liste'][command.split()[0]]} {command.split()[1]}")
                except:
                    os.system(self.commands['liste'][command.split()[0]])
                is_command = True
                    
            else: 
                for val in self.commands.values():
                    
                    if command.split()[0] in val:
                        for func in self.commands.keys():
                            if self.commands[func] == val:
                                
                                try:
                                    args = command.split()[1:]
                                    getattr(self, func)(command.split()[1:])
                                        
                                except IndexError:
                                    getattr(self, func)()
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
            
        settings = self.get_json(self.path + 'settings\\settings.json')
            
            
        if settings["title"] != "":
            os.system(f"title {''.join(settings['title'])}")
        
        if settings["prompt"] == [""]:
            return ''
        
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
    
    # Preventing the shell from closing in case of ValueError.
    def intinput(self, tx, clr='RED'):
        while True:
            choice = input(tx)
            try:
                choice = int(choice)
                return choice
            except:
                print(self.color(clr, self.texte("int_error")))
            
    # Create a menu to choose an option.
    def menu(self, options):
        """Print a menu."""
        for option in options:
            print(f"[{self.color('YELLOW', f'{options.index(option) + 1}')}] {option}")
            
    # Get json variables. 
    def get_json(self, file):
        with open(file, 'r', encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
        
    # To get texte from language file.
    def texte(self, name):
        return self.get_json(self.path + 'settings\\language.json')["texte"][self.get_lang()][name]
    
    # Change json content, or replace
    def in_json(self, file, value, key="prompt", replace=False):
        loaded = self.get_json(file)
        
        if not replace:
            loaded[key].append(value)
        else:
            loaded[key] = [value]
        
        with open(file, 'w', encoding="utf-8") as f:
            json.dump(loaded, f, indent=4)
    
    # Return the current language.
    def get_lang(self):
        if self.get_json(self.path + 'settings\\settings.json')["selected_language"] != []:
            return ''.join(self.get_json(self.path + 'settings\\settings.json')["selected_language"])
        else:
            return "en"
        
    # Return the help for a command.
    def get_help(self, command):
        dict_help = self.get_json(self.path + 'settings\\language.json')["usage"][self.get_lang()][command]
            
        text = f"{self.color('GREEN', list(dict_help.keys())[0])} : "
        for x in dict_help[list(dict_help.keys())[0]]:
            text += f"{x}, "
        text = text[:-2]
        text += f"\n{self.color('GREEN', list(dict_help.keys())[1])} : {''.join(dict_help['Description'])}\n"
        text += f"{self.color('GREEN', list(dict_help.keys())[2])} : "
        for x in dict_help[list(dict_help.keys())[2]]:
            text += f"{x},\n"
            
        return text
                
        
    # Command : leave
    def leave(self, help=False):
        """Exit the shell."""
        if help in self.commands["help"]:
            print(self.get_help("leave"))
        else:
            sys.exit(0)
            
    # Command : help
    def help(self, wnd_help=False):
        if wnd_help == "all":
            os.system("help")
            print("\n\n")
        
        for key in self.commands.keys():
            print(self.get_json(self.path + "settings\\language.json")[self.get_lang()][key])
                
    # Command : setup (pretty big one isn't it ?)
    def setup(self, help=False):
        """Setup the shell."""
        if help in self.commands["help"]:
            print(self.get_help("setup"))
            
        else:
            text = self.get_json(self.path + 'settings\\language.json')["texte"][self.get_lang()]
            print(f"{self.color('GREEN', tx=text['welcome'])}")
            self.menu(text["choice"])
            
            choice = self.intinput(f"{self.hook('?')} > ")
            
            if choice == 1:
                
                print(self.color("GREEN", text['prompt']))
                backup = self.entry_prompt
                
                while True:
                    
                    self.menu(text['prompt_choice'])
                    self.entry_prompt = self.prompt()
                    
                    choice = self.intinput(f"{text['prompt_look']} {self.entry_prompt}\n{self.hook('?')} > ")
                    
                    if choice == 1:
                        """Adding path"""
                        self.in_json(self.path + 'settings\\settings.json', "**path**")
                        
                        
                    elif choice == 2:
                        """Adding the time"""
                        
                        self.menu(text['time'])
                        finish = False
                        while not finish:
                            choice = self.intinput(f"{self.hook('?')} > ")
                            
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
                                
                            elif choice == 8:
                                finish = True
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
                        while not finish:
                            if choice_color == 1:
                                print(text["color_exemple"][0] + self.color("BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = self.intinput(f"{self.hook('?')} > ")
                                prefix = ""
                                
                            elif choice_color == 2:
                                print(text["color_exemple"][0] + self.back("_BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = self.intinput(f"{self.hook('?')} > ")
                                prefix = "_"
                                
                            elif choice_color == 3:
                                finish = True
                                choice = 0
                            
                            if choice == 10:
                                while not finish:
                                    self.menu(text["color_choice_2"])
                                    choice = self.intinput(f"{self.hook('?')} > ")
                                    
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
                            for i in text["style_choice"]:
                                if i == "Exit":
                                    print(self.hook("8") + " Exit")
                                else:
                                    print("[" + self.color("YELLOW", str(text['style_choice'].index(i) + 1)) + "] " + self.style(i.upper(), i))
                            
                            choice = self.intinput(f"{self.hook('?')} > ")
                            
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
                        self.in_json(self.path + 'settings\\settings.json', title, key="title", replace=True)
                        
                    elif choice == 8:
                        custom = input(text["custom_text"])
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
                    self.menu(list(self.get_json(self.path + 'settings\\language.json')["texte"].keys()))
                    print(self.hook(len(list(self.get_json(self.path + 'settings\\language.json')["texte"].keys())) + 1) + " Exit")
                    
                    choice = self.intinput(f"{self.hook('?')} > ")
                    
                    if choice == len(list(self.get_json(self.path + 'settings\\language.json')["texte"].keys())) + 1:
                        finish = True
                    elif choice > len(list(self.get_json(self.path + 'settings\\language.json')["texte"].keys())):
                        print(self.color("RED", text["language_error"]))
                    else:
                        self.in_json(self.path + 'settings\\settings.json', list(self.get_json(self.path + 'settings\\language.json')["texte"].keys())[choice-1], 
                                     key="selected_language", replace=True)
                        finish = True
                finish = False
                
    # Command : pwd
    def pwd(self, path):
        """double all \ from path[0]"""
        if "\\" in path: 
            os.chdir(path[0].replace("\\", "\\\\"))
        else:
            print
    
    # Command : randint
    def randint(self, args):
        if args[0] in self.commands["help"]:
            print(self.get_help("randint"))
            return
        
        max = size = None
        if len(args) == 1:
            try:
                print(np.random.randint(args[0]))
            except:
                print(self.texte("value_error"))
            
        else:
            for i in args:
                if i == args[0]:
                    pass
                else:
                    if i.startswith("max="):
                        max = i.split("=")[1] # max
                    elif i.startswith("size="):
                        size = i.split("=")[1] # size
            try: 
                print(np.random.randint(args[0], int(max) if max != None else max, int(size) if size != None else size))
            except ValueError:
                print(self.texte("value_error"))

    # Command : art
    def art(self, args=['']):
        if args[0] in self.commands["help"]:
            print(self.get_help("art"))
        
        elif self.art_dict:
            if args[0] == "random" or args == ['']:
                print(list(self.art_dict.values())[np.random.randint(len(list(self.art_dict.keys())))])
            else:
                try:
                    print(self.art_dict[' '.join(args)])
                except:
                    print(self.texte("art_error") + list(self.art_dict.keys())[np.random.randint(len(list(self.art_dict.keys())))])
      
shell = Shell()
shell.run()
