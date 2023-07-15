##
[![Python-Forge-AI-LOGO-250x250-c.png](https://i.postimg.cc/jdw7Hs9C/Python-Forge-AI-LOGO-250x250-c.png)](https://postimg.cc/crWCZNdN)  - Forge Python code solutions from problem descriptions with the power of AI -

## Presentation
**PythonForgeAI** is a simple code generation automation tool that uses artificial intelligence to solve specific problems. It acts as an "orchestra conductor", coordinating several actions to produce code that responds to a given prompt. PythonForgeAI uses OpenAI's GPT-4 language model to generate code in response to a specific prompt.

PythonForgeAI is capable of handling several aspects of the Python code development process, including error handling, code validation, and cost calculation. It can detect errors in the generated code and correct them by generating new versions of the code. It can also run the generated code to verify that it works as expected. If the code does not produce the expected result, it can regenerate it until you get code that works correctly. Finally, it calculates the number of "tokens" used to generate the code (which relates to the cost of using the OpenAI API) and can roughly estimate the total cost of generating the code.

This tool is designed to be a flexible and adaptable tool, with a variety of settings that you can adjust to meet your specific needs.

**Warning** This is only a first version, improvements and implementations are planned and under development. 'roadmap.txt'
            

## How it works
PythonForgeAI uses a simple and very direct approach, it works in several steps:
1. **Prompt**: The user provides a prompt describing the problem to be solved.
2. **Tasks generation**: It generates a list of tasks to be carried out to accomplish the project.
3. **Code generation**: PythonForgeAI uses OpenAI's GPT-4 language model to generate code in response to the prompt.
4. **Error handling**: If errors are detected in the generated code, PythonForgeAI corrects them by generating new versions of the code.
5. **Code validation**: PythonForgeAI runs the generated code to verify that it works as expected. If the code does not produce the expected result, PythonForgeAI regenerates it until you get code that works correctly.
6. **File creation**: It creates a file with a generated name that includes the generated code.
7. **Cost calculation**: It calculates the number of "tokens" used to generate the code and can estimate the total cost of generating the code.

## Use
To use PythonForgeAI, you must first install the necessary dependencies. Then you can proceed PythonForgeAI by providing it with a prompt describing the problem to be solved.
1. git clone https://github.com/E4rr0r4/PythonForgeAI.git
2. pip install -r requirements.txt
3. chmod PythonForgeAI.py (if needed, optional)

**In the PythonForgeAI.ini file**:
1. insert your OpenAI API key
2. choose the language 'english' or 'french' (for now)
3. insert your prompt as detailed as possible (on one line)

python PythonForgeAI.py

**Warning** if you ask PythonForgeAI to generate code with a particular library, check that you have previously installed the module.

## Licence
PythonForgeAI is licensed under GPL-3.0. This means that you are free to copy, modify and distribute the code, as long as you keep the same license for modified versions and acknowledge the original authors.

## Contact
If you have any questions or comments about PythonForgeAI, please don't hesitate to contact me.  viraxe4rr0r4@gmail.com
