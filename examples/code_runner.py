import os
from typing import List
from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command, get_code_file_extension
from llm_sandbox.const import SupportedLanguage

def run_python_code():
    with SandboxSession(lang=SupportedLanguage.PYTHON, keep_template=True, verbose=True) as session:
        code = """
        print('Hello, World!')
        import numpy as np
        print(np.random.rand())
        """
        output = session.run(code)
        print(output)

        session.execute_command("pip install pandas")
        code = """
        import pandas as pd
        print(pd.__version__)
        """
        output = session.run(code)
        print(output)

def run_java_code():
    with SandboxSession(lang=SupportedLanguage.JAVA, keep_template=True, verbose=True) as session:
        code = """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
        """
        output = session.run(code)
        print(output)

def run_javascript_code():
    with SandboxSession(lang=SupportedLanguage.JAVASCRIPT, keep_template=True, verbose=True) as session:
        code = """
        console.log('Hello, World!')
        """
        output = session.run(code)
        print(output)

        session.execute_command("yarn add axios")
        code = """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
        """
        output = session.run(code)
        print(output)

def run_cpp_code():
    with SandboxSession(lang=SupportedLanguage.CPP, keep_template=True, verbose=True) as session:
        code = """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
        """
        output = session.run(code)
        print(output)

        code = """
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
        output = session.run(code)
        print(output)

if __name__ == '__main__':
    run_python_code()
    run_java_code()
    run_javascript_code()
    run_cpp_code()