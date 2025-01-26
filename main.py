import os

exe_keywords = ["avr-gcc", "avr-g++", "avr-objcopy", "avrdude", "avr-size"]
exe_paths = {}
c_compiler_flags = []
cpp_compiler_flags = []
linker_flags = []
include_paths = []
c_src_files = []
cpp_src_files = []

def find_executables():
    with open("testing/arduino.log", "r") as file:
        for line in file.readlines():
            if(len(line.split()) > 0):
                first_word = line.split()[0]
                stripped_word = first_word.strip("\"").replace('\\\\', '\\').replace("\\", "/")
                exe_file = stripped_word+".exe"
                if(os.path.isfile(exe_file)):
                    keyword = stripped_word.split("/")[-1]
                    if(keyword in exe_keywords):
                        exe_paths[keyword] = exe_file

def find_compiler_flags():
    with open("testing/arduino.log", "r") as file:
        for line in file.readlines():
            flag_type = ""
            for word in line.split():
                if(word == line.split()[0]):
                    stripped_word = word.strip("\"").replace('\\\\', '\\').replace("\\", "/")
                    exe_file = stripped_word+".exe"
                    if(os.path.isfile(exe_file)):
                        if(exe_file == exe_paths["avr-gcc"]):
                            flag_type = "c_flag"
                        elif(exe_file == exe_paths["avr-g++"]):
                            flag_type = "cpp_flag"
                elif(flag_type):
                    if(word[0] == "-" and word[1] != "I" and word[1] != "o"):
                        if(flag_type == "c_flag"):
                            if(word not in c_compiler_flags):
                                c_compiler_flags.append(word)
                        elif(flag_type == "cpp_flag"):
                            if(word not in cpp_compiler_flags):
                                cpp_compiler_flags.append(word)

def find_source_files():
    with open("testing/arduino.log", "r") as file:
        for line in file.readlines():
            if(len(line.split()) > 0):
                first_word = line.split()[0]
                stripped_word = first_word.strip("\"").replace('\\\\', '\\').replace("\\", "/")
                exe_file = stripped_word+".exe"
                if (not exe_file in exe_paths.values()):
                    continue
                else:
                    for word in line.split():
                        stripped_word = word.strip("\"").replace('\\\\', '\\').replace("\\", "/")
                        if stripped_word.startswith("-I"):
                            if os.path.exists(stripped_word[2:]):
                                if(not stripped_word[2:] in include_paths):
                                    include_paths.append(stripped_word[2:])
                        elif(os.path.isfile(stripped_word)):
                            if(stripped_word.endswith(".c")):
                                if(not stripped_word in c_src_files):
                                    c_src_files.append(stripped_word)
                            elif(stripped_word.endswith(".cpp")):
                                if(not stripped_word in cpp_src_files):
                                    cpp_src_files.append(stripped_word)

if __name__=="__main__":
    find_executables()
    find_compiler_flags()
    find_source_files()