from llm_sandbox import SandboxSession
from llm_sandbox.utils import get_libraries_installation_command, get_code_execution_command
from llm_sandbox.const import SupportedLanguage

def run_code(lang: str, code: str, libraries: list = None):
    with SandboxSession(lang=lang, keep_template=True, verbose=True) as session:
        if libraries:
            install_command = get_libraries_installation_command(lang, libraries)
            session.execute_command(install_command)

        if lang == SupportedLanguage.CPP:
            output = session.run(code)
            print(output)
            exec_commands = get_code_execution_command(lang, "main.cpp")
            for command in exec_commands:
                session.execute_command(command)
        else:
            output = session.run(code)
            print(output)

def run_python_code():
    run_code(SupportedLanguage.PYTHON, "print('Hello, World!')")
    run_code(SupportedLanguage.PYTHON, "import numpy as np\nprint(np.random.rand())", libraries=["numpy"])
    run_code(SupportedLanguage.PYTHON, "import pandas as pd\nprint(pd.__version__)", libraries=["pandas"])
    session.copy_to_runtime("README.md", "/sandbox/data.csv")

def run_java_code():
    run_code(SupportedLanguage.JAVA, """
        public class Main {
            public static void main(String[] args) {
                System.out.println("Hello, World!");
            }
        }
    """)

def run_javascript_code():
    run_code(SupportedLanguage.JAVASCRIPT, "console.log('Hello, World!')")
    run_code(SupportedLanguage.JAVASCRIPT, """
        const axios = require('axios');
        axios.get('https://jsonplaceholder.typicode.com/posts/1')
            .then(response => console.log(response.data));
    """, libraries=["axios"])

def run_cpp_code():
    run_code(SupportedLanguage.CPP, """
        #include <iostream>
        int main() {
            std::cout << "Hello, World!" << std::endl;
            return 0;
        }
    """)
    run_code(SupportedLanguage.CPP, """
        #include <iostream>
        #include <vector>
        int main() {
            std::vector<int> v = {1, 2, 3, 4, 5};
            for (int i : v) {
                std::cout << i << " ";
            }
            std::cout << std::endl;
            return 0;
        }
    """)
    run_code(SupportedLanguage.CPP, """
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
    """, libraries=["libstdc++"])

if __name__ == "__main__":
    run_cpp_code()