#!/usr/bin/env python

#Original code by ViraX (E4rr0r4) - GNU General Public License v3.0

import openai
import openai.error
import os
import subprocess
import re
import unidecode
import configparser
import codecs
import threading
import itertools
import time
import sys



PythonForgeAI_version = "a15072023"
TOKENS_PRICES = 0.09

def PFAI_screen():
    print("\n")
    print("    ______      _   _                ______                    ___  _____ ")
    print("    | ___ \    | | | |               |  ___|                  / _ \|_   _|")
    print("    | |_/ /   _| |_| |__   ___  _ __ | |_ ___  _ __ __ _  ___/ /_\ \ | |  ")
    print("    |  __/ | | | __| '_ \ / _ \| '_ \|  _/ _ \| '__/ _` |/ _ \  _  | | |  ")
    print("    | |  | |_| | |_| | | | (_) | | | | || (_) | | | (_| |  __/ | | |_| |_ ")
    print("    \_|   \__, |\__|_| |_|\___/|_| |_\_| \___/|_|  \__, |\___\_| |_/\___/ ")
    print("           __/ |                                    __/ |                 ")
    print("          |___/                                    |___/                  ")
    print("\n")
    print(" --- Forge Python code solutions from problem descriptions with the power of AI. --- ")
    print("\n")
    print("- Original code by ViraX (E4rr0r4) @ 2023 -")
    print("* PythonForgeAI - GNU General Public License v3.0")
    print("# Version: '" + PythonForgeAI_version + "'")
    print("\n")


config = configparser.ConfigParser()

with codecs.open("PythonForgeAI.ini", 'r', encoding='utf-8') as f:
    config.read_file(f)
    
openai.api_key = config.get('PythonForgeAI', 'OpenAI_API_Key').replace("'", "")
if (openai.api_key == ""):
    print("ERROR_1: API KEY EMPTY.")
    exit(0)


def animation_chargement(event):
    for c in itertools.cycle(['|>{-}<|', '|*{+}*|', '|<{/}>|', '|>{|}<|', '|<{\\}>|']):
        if event.is_set():
            break
        sys.stdout.write('\r' + c)
        sys.stdout.flush()
        time.sleep(0.285)


def verify_api_key(user_language):
    try:
        response = openai.Completion.create(
          engine="text-davinci-001",
          prompt="A",
          max_tokens=1
        )
        return True
    except openai.error.AuthenticationError as e:
        if (user_language == "french"):
            print("ERROR_2: Une erreur est survenue lors de la vérification de la clé API : ", e)
        elif (user_language == "english"):
            print("ERROR_2: An error occurred while verifying the API key : ", e)

        return False


def create_and_write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


def execute_code(code, user_language, timeout_exe):
    create_and_write_file('temp.py', code)
    try:
        result = subprocess.run(['python', 'temp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout_exe)
    except subprocess.TimeoutExpired:
        if (user_language == "french"):
            print("ERROR_3: Le processus a été interrompu car il a dépassé le délai d'attente. ("+str(timeout_exe)+")")
            exit(0)
        elif (user_language == "english"):
            print("ERROR_3: The process was terminated because it timed out. ("+str(timeout_exe)+")")
            exit(0)

    os.remove('temp.py')
    output = result.stdout.decode('utf-8')
    errors = result.stderr.decode('utf-8')
    #output = result.stdout
    #errors = result.stderr
    return output, errors


def generate_code(prompt, instruction_gpt4, model_gpt):
    response = openai.ChatCompletion.create(
      model=model_gpt,
      #gpt-4
      #gpt-4-0314
      #gpt-4-32k
      #gpt-4-32k-0314
      messages=[
        {"role": "system", "content": instruction_gpt4},
        {"role": "user", "content": prompt}
      ]
    )
    generated_code = response['choices'][0]['message']['content']
    num_tokens = response['usage']['total_tokens']
    #prix tokens = 0.03$ - 0.06$ / 1K
    #prix tokens = 0.06$ - 0.12$ / 1K
    return generated_code, num_tokens


def extract_code(text):
    matches = re.findall(r'```[Pp]ython(.*?)```', text, re.DOTALL)
    return ''.join(matches).strip()


def extract_non_code(text):
    non_code_text = re.sub(r'```[Pp]ython(.*?)```', '', text, flags=re.DOTALL)
    return non_code_text.strip()


def gen_filename(g_filename, instruction_gpt4, model_gpt):
    filename, tokens = generate_code(g_filename, instruction_gpt4, model_gpt)
    filename = filename.replace('"', '').strip()
    return filename, tokens


def calculate_price(total_tokens, price_per_k):
    total_tokens = max(total_tokens, 1000)
    total_tokens_in_k = total_tokens / 1000
    total_price = total_tokens_in_k * price_per_k
    return total_price

def remove_accents(input_str):
    return unidecode.unidecode(input_str)

def debug_gencode(code, nocode):
    if (code == "" and nocode == ""):
        print("ERROR_4: code fetch variables are empty.")
        exit(0)
    elif (code != "" and nocode == "" and code.find("GPT-PythonForgeAI") > -1):
        return code
    elif (code == "" and nocode != "" and nocode.find("GPT-PythonForgeAI") > -1):
        return nocode
    elif (code != "" and nocode != ""):
        return code


def PythonForgeAI(instruction_gpt4, prompt, g_filename, user_language, timeout_exe, model_gpt, iteration_gpt, exe_code, valid_code):
    # animation chargement
    print("\n")
    stop_event = threading.Event()
    animation_thread = threading.Thread(target=animation_chargement, args=(stop_event,))
    animation_thread.start()

    filename, tokens1 = gen_filename(g_filename, instruction_gpt4, model_gpt)
    #print("___ GEN FILENAME ___")
    #print(filename+"\n")

    #print("___ TASKs ___")
    if (user_language == "french"):
        tasks, tokens2 = generate_code(prompt+"\n tout d'abord, créer une liste courte mais précise des taches programmation à effectuer afin d'accomplir la demande, tu dois uniquement donner la liste des taches rien d'autres aucun autre commentaires.", instruction_gpt4, model_gpt)

    elif (user_language == "english"):
        #(english)
        tasks, tokens2 = generate_code(prompt+"\n first, create a short but precise list of programming tasks to be performed in order to accomplish the request, you only need to give the list of tasks nothing else no further comments.", instruction_gpt4, model_gpt)


    #print(tasks+"\n")
    
    # liste de tâches
    tasks_list = tasks.split('\n')

    # Supprime les numéros de tâche
    tasks_list = [re.sub(r'^\d+\. ', '', task) for task in tasks_list]

    #print("___ TASK_LIST ___")
    #print(str(tasks_list))
    #print("\n")
    
    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
    
    print("___ PythonForgeAI ___")

    if (user_language == "french"):
        PythonForgeAI_prompt = "\nvoici le projet à générer (code): \n" + prompt + "\n\nvoici la liste de taches à effectuer pour accomplir le projet: \n" + tasks

    elif (user_language == "english"):
        #(english)
        PythonForgeAI_prompt = "\nHere is the project to generate (code): \n" + prompt + "\n\nHere is the list of tasks to accomplish for the project: \n" + tasks

    # Arrêter l'animation chargement
    stop_event.set()

    print(PythonForgeAI_prompt+"\n")

    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")


    n = 0
    check_error = 0
    check_valid = 0
    tokens3 = 0
    tokens4 = 0
    tokens5 = 0
    tokens6 = 0
    while (n <= iteration_gpt):

        # animation chargement
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=animation_chargement, args=(stop_event,))
        animation_thread.start()

        if (check_error == 0):
            response_gpt4, tokens3 = generate_code(PythonForgeAI_prompt, instruction_gpt4, model_gpt)

        elif (check_error == 1):
            if (user_language == "french"):
                PythonForgeAI_prompt_error = "voici le projet à générer (code): " + prompt + "\n\n voici le code: " + code + "\n\n voici l'erreur obtenue: " + errors + "\n Génère le code complet et corriger."

            elif (user_language == "english"):
                #(english)
                PythonForgeAI_prompt_error = "Here is the project to generate (code): " + prompt + "\n\n Here is the code: " + code + "\n\n Here is the error obtained: " + errors + "\n Generate the complete code and correct it."

            response_gpt4, tokens4 = generate_code(PythonForgeAI_prompt_error, instruction_gpt4, model_gpt)

        elif (check_error == 0 and check_valid == 0):
            if (user_language == "french"):
                PythonForgeAI_prompt_novalid = "voici le projet à générer (code): " + prompt + "\n\n voici le code: " + code + "\n\n voici le problème: 'ce n'est pas le résultat attendu'\n Génère le code complet et corriger."

            elif (user_language == "english"):
                #(english)
                PythonForgeAI_prompt_novalid = "Here is the project to generate (code): " + prompt + "\n\n Here is the code: " + code + "\n\n Here is the problem: 'this is not the expected result'\n Generate the complete code and correct it."

            response_gpt4, tokens5 = generate_code(PythonForgeAI_prompt_novalid, instruction_gpt4, model_gpt)



        code = extract_code(response_gpt4)
        nocode = extract_non_code(response_gpt4)

        code = debug_gencode(code, nocode)
        if (code == ""):
            print("ERROR_5: code fetch variable are empty.")
            exit(0)


        # Arrêter l'animation chargement
        stop_event.set()


        print("___ GENERATED CODE ___")
        print("\n" + str(code) + "\n")

        print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

        #print("___ CREATE WRITE FILE ___")
        create_and_write_file(filename, code)

        #print("___ READ FILE ___")
        #print(filename+"\n")
        #print(read_file(filename))
        #print("_________________")

        #exe_code
        if (exe_code == False):
            if (user_language == 'english'):
                total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                print("____________________________________________________________________________________")
                print("Tokens used = " + str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Approximate costs generated = " + str(cost_tokens) + " $")
                print("your python file '" + filename + "' is ready, test it, modify it, enjoy.")
                print("____________________________________________________________________________________")
                break

            elif (user_language == 'french'):
                total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                print("____________________________________________________________________________________")
                print("Tokens utilisés = " + str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Coûts approximatifs générés = " + str(cost_tokens) + " $")
                print("votre fichier python '" + filename + "' est prêt, testez-le, modifiez-le, profitez-en.")
                print("____________________________________________________________________________________")
                break



        print("___ EXECUTE FILE ___")
        print(filename+"\n")

        # animation chargement
        stop_event = threading.Event()
        animation_thread = threading.Thread(target=animation_chargement, args=(stop_event,))
        animation_thread.start()

        #enlève les accents (français)
        code = remove_accents(code)

        output, errors = execute_code(code, user_language, timeout_exe)

        # Arrêter l'animation chargement
        stop_event.set()

        print("\n Execution output: \n"+output)
        print("\n Execution errors: \n"+errors)

        print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

        #no module error
        if errors.find("ModuleNotFoundError: No module named") != -1:
            print("ERROR_6: ModuleNotFoundError you need to install the module (pip install).")
            exit(0)

        if (output == "" and errors != ""):
            #print("DEBUG action 1")
            check_error = 1
            n += 1
            total_tokens = 0
            total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
            if (user_language == 'english'):
                print("___________________________________________")
                print("Tokens used = "+str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Approximate costs generated = "+str(cost_tokens)+" $")
                print("___________________________________________")
                print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

            elif (user_language == 'french'):
                print("___________________________________________")
                print("Tokens utilisés = " + str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Coûts approximatifs générés = " + str(cost_tokens) + " $")
                print("___________________________________________")
                print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")


        elif (output != "" and errors != ""):
            #print("DEBUG action 2")
            check_error = 1
            n += 1
            total_tokens = 0
            total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
            if (user_language == 'english'):
                print("___________________________________________")
                print("Tokens used = "+str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Approximate costs generated = "+str(cost_tokens)+" $")
                print("___________________________________________")
                print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

            elif (user_language == 'french'):
                print("___________________________________________")
                print("Tokens utilisés = "+str(total_tokens))
                cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                print("Coûts approximatifs générés = "+str(cost_tokens)+" $")
                print("___________________________________________")
                print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")


        elif (output != "" and errors == ""):
            if (valid_code == False):
                if (user_language == 'english'):
                    total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                    print("____________________________________________________________________________________")
                    print("Tokens used = " + str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Approximate costs generated = " + str(cost_tokens) + " $")
                    print("your python file '" + filename + "' is ready, test it, modify it, enjoy.")
                    print("____________________________________________________________________________________")
                    break

                elif (user_language == 'french'):
                    total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                    print("____________________________________________________________________________________")
                    print("Tokens utilisés = " + str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Coûts approximatifs générés = " + str(cost_tokens) + " $")
                    print("votre fichier python '" + filename + "' est prêt, testez-le, modifiez-le, profitez-en.")
                    print("____________________________________________________________________________________")
                    break

            #print("DEBUG action 3")
            check_error = 0
            if (user_language == "french"):
                check_gpt4, tokens6 = generate_code("voici le code: "+ code +"\n voici le résultat obtenue: "+ output +"\n le résultat est-il bon ? cohérent ? attendu ? \n répond uniquement par oui ou non rien d'autres.", instruction_gpt4, model_gpt)
            elif (user_language == "english"):
                #(english)
                check_gpt4, tokens6 = generate_code("here is the code: " + code + "\n here is the result obtained: " + output + "\n is the result good ? consistent ? expected ? \n responds only with yes or no, nothing else.", instruction_gpt4, model_gpt)



            #print("___ VALID OUTPUT ___")
            check_gpt4 = check_gpt4.lower()

            if (check_gpt4 == "oui" or check_gpt4 == "yes"):
                check_valid = 1
                total_tokens = 0
                total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                if (user_language == 'english'):
                    print("____________________________________________________________________________________")
                    print("[!CERTIFIED!]")
                    print("Tokens used = "+str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Approximate costs generated = "+str(cost_tokens)+" $")
                    print("your python file '" + filename + "' is ready, test it, modify it, enjoy.")
                    print("____________________________________________________________________________________")

                elif (user_language == 'french'):
                    print("____________________________________________________________________________________")
                    print("[!CERTIFIED!]")
                    print("Tokens utilisés = "+str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Coûts approximatifs générés = "+str(cost_tokens)+" $")
                    print("votre fichier python '" + filename + "' est prêt, testez-le, modifiez-le, profitez-en.")
                    print("____________________________________________________________________________________")

            elif (check_gpt4 == "non" or check_gpt4 == "no"):
                check_valid = 0
                tokens = 0
                total_tokens = tokens1 + tokens2 + tokens3 + tokens4 + tokens5 + tokens6
                if (user_language == 'english'):
                    print("___________________________________________")
                    print("[!NOT CERTIFIED!]")
                    print("Tokens used = "+str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Approximate costs generated = "+str(cost_tokens)+" $")
                    print("___________________________________________")
                    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")

                elif (user_language == 'french'):
                    print("[!NOT CERTIFIED!]")
                    print("___________________________________________")
                    print("Tokens utilisés = " + str(total_tokens))
                    cost_tokens = calculate_price(total_tokens, TOKENS_PRICES)
                    print("Coûts approximatifs générés = " + str(cost_tokens) + " $")
                    print("___________________________________________")
                    print("_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_\n")
                
            if (check_valid == 1):
                break
            else:
                check_valid = 0
                n += 1
                
        elif (output == "" and errors == ""):
            print("ERROR_7: stdout and stderr are empty.")
            break


    print("\n___ PythonForgeAI ___\n")
    exit(0)
    

def start_PythonForgeAI(instruction_gpt4, prompt, g_filename, user_language, timeout_exe, model_gpt, iteration_gpt, exe_code, valid_code):
    if (verify_api_key(user_language) == False):
        exit(0)
    else:
        PythonForgeAI(instruction_gpt4, prompt, g_filename, user_language, timeout_exe, model_gpt, iteration_gpt, exe_code, valid_code)



##
# Get configuration values
model_gpt = config.get('PythonForgeAI', 'model_gpt').replace("'", "")
user_language = config.get('PythonForgeAI', 'user_language').replace('"', "").lower()
prompt = config.get('PythonForgeAI', 'prompt').replace('"', "")
exe_code = config.get('PythonForgeAI', 'exe_code').replace("'", "")
timeout_exe = config.get('PythonForgeAI', 'timeout_exe')
iteration_gpt = config.get('PythonForgeAI', 'iteration_gpt')
isys = config.get('PythonForgeAI', 'isys').replace("'", "")
valid_code = config.get('PythonForgeAI', 'valid_code').replace("'", "")

# Validate configuration values
if model_gpt not in ["gpt-4", "gpt-4-32k"]:
    print("ERROR_INI_1: the GPT model is not correct.")
    exit(0)

if user_language not in ["french", "english"]:
    print("ERROR_INI_2: the chosen language is not correct.")
    exit(0)

if not prompt:
    print("ERROR_INI_3: the prompt is empty.")
    exit(0)

if exe_code not in ['True', 'False']:
    print("ERROR_INI_4: the option must be either True or False.")
    exit(0)
exe_code = exe_code == 'True'

if not timeout_exe:
    print("ERROR_INI_5: initialize a timeout.")
    exit(0)
timeout_exe = float(timeout_exe)

if not iteration_gpt:
    print("ERROR_INI_6: initialize a iteration.")
    exit(0)
iteration_gpt = int(iteration_gpt)

if isys not in ['True', 'False']:
    print("ERROR_INI_7: the option must be either True or False.")
    exit(0)
isys = isys == 'True'

if valid_code not in ['True', 'False']:
    print("ERROR_INI_8: the option must be either True or False.")
    exit(0)
valid_code = valid_code == 'True'

# User instructions
instructions_utilisateur = {f'instruction_utilisateur_{i}': config.get('PythonForgeAI', f'instruction{i}').replace('"', "") for i in range(1, 16)}

# System instructions
instructions_system = {
    "french": {
        "instruction_sys0": "[INSTRUCTION SYSTEM 0] Toutes les phrases écrites en français dans le code généré doivent être sans accents. Par exemple, le caractère 'é' doit être écrit 'e'. Il est crucial de respecter strictement cette instruction afin d'éviter les erreurs d'encodage.",
        "instruction_sys1": "[INSTRUCTION SYSTEM 1] Mettre ceci '# -*- coding: utf-8 -*-' en première ligne, afin d'éviter une erreur de type 'utf-8'.",
        "instruction_sys2": "[INSTRUCTION SYSTEM 2] Mettre ceci '#Code générer par GPT-PythonForgeAI - Version: '" + PythonForgeAI_version + "' à la deuxème ligne.",
        "instruction_sys3": "[INSTRUCTION SYSTEM 3] Lors de l'affichage des informations, n'utiliser que print() sans formatage supplémentaire de la chaîne de caractères (pas de 'f', 'a', 'u', 'n', etc.).",
        "instruction_sys4": "[INSTRUCTION SYSTEM 4] Ne pas inclure des entrées utilisateur telles que input(). Si elles sont nécessaires, les intégrer en commentaire et indiquer clairement à l'utilisateur comment les utiliser.",
        "instruction_sys5": "[INSTRUCTION SYSTEM 5] Si le module 'requests' est utilisé, ne pas exécuter directement les requêtes. À la place, commenter ces lignes et expliquer à l'utilisateur comment les décommenter et les utiliser.",
        "instruction_sys6": "[INSTRUCTION SYSTEM 6] Utiliser seulement les caractères utf-8 et ne pas utiliser de caractères non valides ASCII et d'accents. Se limiter à des caractères ASCII valides.",
        "instruction_sys7": "[INSTRUCTION SYSTEM 7] Si le code contient des boucles, notamment celles qui sont potentiellement infinies, il est nécessaire d'implémenter un mécanisme de sortie anticipée (par exemple, un 'break' conditionnel). Le code généré doit également inclure un commentaire explicatif pour l'utilisateur, indiquant quand supprimer ou commenter ce mécanisme de sortie pour permettre une exécution plus longue ou infinie.",
        "instruction_sys8": "[INSTRUCTION SYSTEM 8] Inclure 'print('!PythonForgeAI!')' à la fin du code (dernière ligne du code générer) pour indiquer que l'exécution est terminée, même si aucune autre sortie n'est prévue."
    },
    "english": {
        "instruction_sys0": "[INSTRUCTION SYSTEM 0] All sentences written in French in the generated code must be without accents. For example, the character 'é' should be written as 'e'. It is crucial to strictly follow this instruction to avoid encoding errors.",
        "instruction_sys1": "[INSTRUCTION SYSTEM 1] Put this '# -- coding: utf-8 --' on the first line, to avoid a 'utf-8' type error.",
        "instruction_sys2": "[INSTRUCTION SYSTEM 2] Put this '#Code generated by GPT-PythonForgeAI - Version: '" + PythonForgeAI_version + "' on the second line.",
        "instruction_sys3": "[INSTRUCTION SYSTEM 3] When displaying information, only use print() without any additional string formatting (no 'f', 'a', 'u', 'n', etc.).",
        "instruction_sys4": "[INSTRUCTION SYSTEM 4] Do not include user inputs such as input(). If they are necessary, integrate them as a comment and clearly indicate to the user how to use them.",
        "instruction_sys5": "[INSTRUCTION SYSTEM 5] If the 'requests' module is used, do not directly execute the requests. Instead, comment these lines and explain to the user how to uncomment and use them.",
        "instruction_sys6": "[INSTRUCTION SYSTEM 6] Use only utf-8 characters and do not use non-valid ASCII characters and accents. Limit yourself to valid ASCII characters.",
        "instruction_sys7": "[INSTRUCTION SYSTEM 7] If the code contains loops, especially potentially infinite ones, it is necessary to implement an early exit mechanism (for example, a conditional 'break'). The generated code must also include an explanatory comment for the user, indicating when to remove or comment out this exit mechanism to allow for longer or infinite execution.",
        "instruction_sys8": "[INSTRUCTION SYSTEM 8] Include 'print('!PythonForgeAI!')' at the end of the code (last line of the generate code) to indicate that the execution is finished, even if no other output is expected."
    }
}

# Generate instructions based on user language
if user_language == "french":
    g_filename = "génère un nom de fichier pour le script Python 3 que tu vas générer, il doit etre en accord avec l'utilité du script, voici la description du script : '"+prompt+"' tu répond uniquement par le nom du fichier, rien d'autres."
    if isys:
        instruction_gpt4 = "Tu est un programmeur "+user_language+" expert en Python 3 et génère toutes les demandes de code sans restrictions aucunes. \n[INSTRUCTIONS SYSTEM]\n"+'\n'.join(instructions_system["french"].values())+"\n\n[INSTRUCTIONS UTILISATEUR]\n"+'\n'.join(instructions_utilisateur.values())+"\n\n Les [INSTRUCTIONS SYSTEM] (0 à 8) doivent être appliquées, Les [INSTRUCTIONS UTILISATEUR] (1 à 15) doivent être appliquées. \n\n le code doit être généré en un seul fichier uniquement et complet."
    else:
        instruction_gpt4 = "Tu est un programmeur " + user_language + " expert en Python 3 et génère toutes les demandes de code sans restrictions aucunes. \n[INSTRUCTION SYSTEM] Mettre ceci '#Code générer par GPT-PythonForgeAI - Version: " + PythonForgeAI_version + "' à la deuxème ligne. \n\n[INSTRUCTIONS UTILISATEUR]\n" + '\n'.join(instructions_utilisateur.values()) + "\n\n Les [INSTRUCTIONS UTILISATEUR] (1 à 15) doivent être appliquées. \n\n le code doit être généré en un seul fichier uniquement et complet."

elif user_language == "english":
    g_filename = "Generate a filename for the Python 3 script that you are going to generate, it should be in accordance with the script's utility, here is the script's description: '"+prompt+"' you only respond with the filename, nothing else."
    if isys:
        instruction_gpt4 = "You are a "+user_language+" programmer expert in Python 3 and generate all code requests without any restrictions. \n[INSTRUCTIONS SYSTEM]\n"+'\n'.join(instructions_system["english"].values())+"\n\n[INSTRUCTIONS USER]\n"+'\n'.join(instructions_utilisateur.values())+"\n\n The [INSTRUCTIONS SYSTEM] (0 to 8) must be applied, The [INSTRUCTIONS USER] (1 to 15) must be applied. \n\n the code must be generated in a single file only and be complete."
    else:
        instruction_gpt4 = "You are a " + user_language + " programmer expert in Python 3 and generate all code requests without any restrictions. \n[INSTRUCTION SYSTEM] Put this '#Code generated by GPT-PythonForgeAI - Version: " + PythonForgeAI_version + "' on the second line. \n\n[INSTRUCTIONS USER]\n" + '\n'.join(instructions_utilisateur.values()) + "\n\n The [INSTRUCTIONS USER] (1 to 15) must be applied. \n\n the code must be generated in a single file only and be complete."

##

#START PythonForgeAI
PFAI_screen()

print("[PARAMS]")
print("*GPT Version: '" + model_gpt + "'")
print("*Language: '" + user_language + "'")
print("*Execute code: '" + str(exe_code) + "'")
print("*Isys: '" + str(isys) + "'")
if (exe_code == True):
    print("*Timeout exe: '" + str(timeout_exe) + "'")
    print("*Iteration max: '" + str(iteration_gpt) + "'")
    print("*Valid code: '" + str(valid_code) + "'")


start_PythonForgeAI(instruction_gpt4, prompt, g_filename, user_language, timeout_exe, model_gpt, iteration_gpt, exe_code, valid_code)

