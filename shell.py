import json
import os
import sys
import time

class Shell:

    def __init__(self):
        """Initialize the shell."""
        
        
        if os.path.isfile('./settings/settings.json'):
            self.is_settings = True   
        
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
            
        else:
            self.is_settings = False       
            self.entry_prompt = '> '
            
        if os.path.isfile('./settings/language.json'):
            self.is_language = True 
            
        
        self.commands = {
            "leave": ['exit', "leave", "quit"],
            "help" : ['help', "h", "-help", "-h", "--help", "--h", "?"],
            "setup" : ['setup', "config", "configure"],
            
            
            # Left are linux commands, right are windows commands.
            "liste" : {
                "pwd" : "cd",
                "ls" : "dir", 
                "mv" : "ren",
                "cp" : "copy",
                "mv" : "move",
                "clear" : "cls",
                "rm" : "del",
                "diff" : "fc"
                 
            }
            
        }


        
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
                                    getattr(self, func)(command.split()[1])
                                        
                                except IndexError:
                                    getattr(self, func)()
                                finally:
                                    is_command = True
                                 
            if not is_command:
                try:
                    os.system(command)
                except Exception as e:
                    print(e)

    def prompt(self):
        entry_prompt = []
            
        settings = self.get_json('./settings/settings.json')
            
            
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
    
    def hook(self, tx, clr='YELLOW'):
        return f"[\033[{self.color_panel[clr]}m{tx}\033[0m]"
    
    def menu(self, options):
        """Print a menu."""
        for option in options:
            print(f"[{self.color('YELLOW', f'{options.index(option) + 1}')}] {option}")
    
    def get_json(self, file):
        with open(file, 'r', encoding="utf-8") as f:
            loaded = json.load(f)
            return loaded
    
    def in_json(self, file, value, key="prompt", replace=False):
        loaded = self.get_json(file)
        
        if not replace:
            loaded[key].append(value)
        else:
            loaded[key] = [value]
        
        with open(file, 'w', encoding="utf-8") as f:
            json.dump(loaded, f, indent=4)
    
    def get_lang(self):
        return ''.join(self.get_json('./settings/settings.json')["selected_language"])
        
    
    def get_help(self, command):
        if self.is_language:
            return self.get_json("./settings/language.json")[self.get_lang()][command]
        else: 
            return self.get_json("./settings/language.json")["en"][command]
        
         
    def leave(self, help=False):
        """Exit the shell."""
        if help in self.commands["help"]:
            print(self.get_help("leave"))
        else:
            sys.exit(0)
            

    def help(self, wnd_help=False):
        if wnd_help == "all":
            os.system("help")
            print("\n\n")
        
        for key in self.commands.keys():
            print(self.get_help(key))
                

    def setup(self, help=False):
        """Setup the shell."""
        if help in self.commands["help"]:
            print(self.get_help("setup"))
            
        else:
            text = self.get_json('./settings/language.json')["setup_texte"][self.get_lang()]
            print(f"{self.color('GREEN', tx=text['welcome'])}")
            self.menu(text["choice"])
            
            choice = int(input(f"{self.hook('?')} > "))
            
            if choice == 1:
                
                print(self.color("GREEN", text['prompt']))
                backup = self.entry_prompt
                
                while True:
                    
                    self.menu(text['prompt_choice'])
                    self.entry_prompt = self.prompt()
                    
                    choice = int(input(f"{text['prompt_look']} {self.entry_prompt}\n{self.hook('?')} > "))
                    
                    if choice == 1:
                        """Adding path"""
                        self.in_json('./settings/settings.json', "**path**")
                        
                        
                    elif choice == 2:
                        """Adding the time"""
                        
                        self.menu(text['time'])
                        finish = False
                        while not finish:
                            choice = int(input(f"{self.hook('?')} > ")) 
                            
                            if choice == 1:
                                custom = input(text["custom_text"])
                                self.in_json('./settings/settings.json', custom)
                            
                            elif choice == 2:
                                self.in_json('./settings/settings.json', "**year**")
                            elif choice == 3:
                                self.in_json('./settings/settings.json', "**month**")
                            elif choice == 4:
                                self.in_json('./settings/settings.json', "**day**")
                            elif choice == 5:
                                self.in_json('./settings/settings.json', "**hour**")
                            elif choice == 6:
                                self.in_json('./settings/settings.json', "**minute**")
                            elif choice == 7:
                                self.in_json('./settings/settings.json', "**second**")
                                
                            elif choice == 8:
                                finish = True
                        print("\n\n")
                        
                    elif choice == 3:
                        """Adding user"""
                        self.in_json('./settings/settings.json', "**user**")
                        
                    elif choice == 4:
                        """Adding the hostname"""
                        self.in_json('./settings/settings.json', "**host**")
                        
                    elif choice == 5:
                        """Adding the color"""
                        finish = False
                        
                        self.menu(text['color_type'])
                        choice_color = int(input(f"{self.hook('?')} > "))
                        while not finish:
                            if choice_color == 1:
                                print(text["color_exemple"][0] + self.color("BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = int(input(f"{self.hook('?')} > "))
                                prefix = ""
                                
                            elif choice_color == 2:
                                print(text["color_exemple"][0] + self.back("_BLUE", text["color_exemple"][1]))
                                self.menu(text["color_choice"])
                                choice = int(input(f"{self.hook('?')} > "))
                                prefix = "_"
                                
                            elif choice_color == 3:
                                finish = True
                                choice = 0
                            
                            if choice == 10:
                                while not finish:
                                    self.menu(text["color_choice_2"])
                                    choice = int(input(f"{self.hook('?')} > "))
                                    
                                    if choice in range(1, 8):
                                        self.in_json('./settings/settings.json', f"{prefix}{list(self.color_panel.keys())[choice-1+9]}")
                                        
                                    elif choice == 9:
                                        finish = True
                                finish = False
                            
                            elif choice == 11:
                                finish = True
                            
                            elif choice in range(1, 9):
                                self.in_json('./settings/settings.json', f"{prefix}{list(self.color_panel.keys())[choice-1]}")
                            
                    elif choice == 6:
                        """Adding the style"""
                        finish = False
                        while not finish:
                            for i in text["style_choice"]:
                                if i == "Exit":
                                    print(self.hook("8") + " Exit")
                                else:
                                    print("[" + self.color("YELLOW", str(text['style_choice'].index(i) + 1)) + "] " + self.style(i.upper(), i))
                            
                            choice = int(input(f"{self.hook('?')} > "))
                            
                            if choice == 1:
                                """Adding bold style"""
                                self.in_json('./settings/settings.json', "BOLD")
                                
                            elif choice == 2:
                                """Adding dim style"""
                                self.in_json('./settings/settings.json', "DIM")
                            
                            elif choice == 3:
                                """Adding italic style"""
                                self.in_json('./settings/settings.json', "ITALIC")
                                
                            elif choice == 4:
                                """Adding underline style"""
                                self.in_json('./settings/settings.json', "UNDERLINE")
                                
                            elif choice == 5:
                                """Adding blink style"""
                                self.in_json('./settings/settings.json', "BLINK")
                                
                            elif choice == 6:
                                """Adding reverse style"""
                                self.in_json('./settings/settings.json', "REVERSE")
                                
                            elif choice == 7:
                                """Adding strikethrough style"""
                                self.in_json('./settings/settings.json', "STRIKETHROUGH")
                                
                            elif choice == 8:
                                """Exiting the style"""
                                finish = True
                        
                    
                    elif choice == 7:
                        title = input(text["title"])
                        self.in_json('./settings/settings.json', title, key="title", replace=True)
                        
                    elif choice == 8:
                        custom = input(text["custom_text"])
                        self.in_json('./settings/settings.json', custom)
                                                
                    elif choice == 9:
                        """Reset the prompt"""
                        self.in_json('./settings/settings.json', "", replace=True)
                        print(text["reset"])
                        
                    elif choice == 10:
                        """Go back"""
                        return 
                    
            elif choice == 2:
                finish = False
                while not finish:
                    self.menu(list(self.get_json('./settings/language.json')["setup_texte"].keys()))
                    print(self.hook(len(list(self.get_json('./settings/language.json')["setup_texte"].keys())) + 1) + " Exit")
                    
                    choice = int(input(f"{self.hook('?')} > "))
                    
                    if choice == len(list(self.get_json('./settings/language.json')["setup_texte"].keys())) + 1:
                        finish = True
                    elif choice > len(list(self.get_json('./settings/language.json')["setup_texte"].keys())):
                        print(self.color("RED", text["language_error"]))
                    else:
                        self.in_json('./settings/settings.json', list(self.get_json('./settings/language.json')["setup_texte"].keys())[choice-1], 
                                     key="selected_language", replace=True)
                        finish = True
                finish = False
                
            
      
shell = Shell()
shell.run()
