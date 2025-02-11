import os
from typing import List
from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command, get_code_file_extension
from llm_sandbox.const import SupportedLanguage

def run_python_code(code: str, libraries: List[str] = None):
    output_dir = f'output_{SupportedLanguage.PYTHON}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with SandboxSession(lang=SupportedLanguage.PYTHON, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(SupportedLanguage.PYTHON, libraries)
            session.execute_command(install_command)

        output = session.run(code)
        print(output)

def run_java_code(code: str):
    output_dir = f'output_{SupportedLanguage.JAVA}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with SandboxSession(lang=SupportedLanguage.JAVA, keep_template=True, verbose=True) as session:
        output = session.run(code)
        print(output)

def run_javascript_code(code: str, libraries: List[str] = None):
    output_dir = f'output_{SupportedLanguage.JAVASCRIPT}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with SandboxSession(lang=SupportedLanguage.JAVASCRIPT, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(SupportedLanguage.JAVASCRIPT, libraries)
            session.execute_command(install_command)

        output = session.run(code)
        print(output)

def run_cpp_code(code: str, libraries: List[str] = None):
    output_dir = f'output_{SupportedLanguage.CPP}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with SandboxSession(lang=SupportedLanguage.CPP, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(SupportedLanguage.CPP, libraries)
            session.execute_command(install_command)

        output = session.run(code)
        print(output)

if __name__ == '__main__':
    python_code = """
    print('Hello, World!')
    import numpy as np
    print(np.random.rand())
    import pandas as pd
    print(pd.__version__)
    """
    run_python_code(python_code, libraries=['numpy', 'pandas'])

    java_code = """
    public class Main {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }
    """
    run_java_code(java_code)

    javascript_code = """
    console.log('Hello, World!')
    const axios = require('axios');
    axios.get('https://jsonplaceholder.typicode.com/posts/1')
        .then(response => console.log(response.data));
    """
    run_javascript_code(javascript_code, libraries=['axios'])

    cpp_code = """
    #include <iostream>
    int main() {
        std::cout << "Hello, World!" << std::endl;
        return 0;
    }
    """
    run_cpp_code(cpp_code)

    cpp_code_with_lib = """
    #include <iostream>
    #include <vector>
    #include <algorithm>
    int main() {
        std::vector<int> v = {1, 2, 3, 4, 5};
        std::reverse(v.begin(), v.end());
        for (int i : v) {
            std::cout << i << " ";
        }
        std::cout << std::endl;
        return 0;
    }
    """
    run_cpp_code(cpp_code_with_lib, libraries=['libstdc++'])